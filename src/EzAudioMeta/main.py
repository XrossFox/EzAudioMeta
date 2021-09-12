from os import path, listdir
from re import error

import click
import magic
import audio.base_audio
import utilities.custom_exceptions
import utilities.optional_string_matchers
import consts as con

_op_str_matchers = utilities.optional_string_matchers.OptionalStringMatchers()


@click.command()
@click.option('--file', type=str)
@click.option('--files-directory', type=str, help=con.HELP_FILES_DIR)
@click.option('--from-file', type=str, help=con.HELP_FROM_FILE)
@click.option('--album', type=str)
@click.option('--albumartist', type=str)
@click.option('--artist', type=str)
@click.option('--comment', type=str)
@click.option('--compilation', type=int)
@click.option('--composer', type=str)
@click.option('--discnumber', type=int)
@click.option('--genre', type=str)
@click.option('--lyrics', type=str)
@click.option('--totaldiscs', type=int)
@click.option('--totaltracks', type=int)
@click.option('--tracknumber', type=int)
@click.option('--tracktitle', type=str)
@click.option('--year', type=int)
@click.option('--isrc', type=str)
@click.option('--parse-title-capitalize', type=str, help=con.PARSE_CAP_HELP)
@click.option('--parse-title-as-is', type=str, help=con.PARSE_ASIS_HELP)
@click.option('--parse-title-clean', type=str, help=con.PARSE_CLEAN_HELP)
@click.option('--parse-track-number', type=str, help=con.PARSE_TRACK_NUMBER)
def cli(file, files_directory, from_file, album, albumartist, artist, comment,
        compilation,
        composer, discnumber, genre, lyrics,
        totaldiscs, totaltracks,
        tracknumber, tracktitle, year, isrc, parse_title_capitalize,
        parse_title_as_is, parse_title_clean, parse_track_number):
    '''
    This CLI application receives an audio file and the tags that are to be
    setted/changed. Most tags are expected to be character
    strings, but some like 'tracknumber' are numbers. At least a file and a tag
    are expected to be set.
    '''
    try:

        tags = {
            "album": album,
            "albumartist": albumartist,
            "artist": artist,
            "comment": comment,
            "compilation": compilation,
            "composer": composer,
            "discnumber": discnumber,
            "genre": genre,
            "lyrics": lyrics,
            "totaldiscs": totaldiscs,
            "totaltracks": totaltracks,
            "tracknumber": tracknumber,
            "tracktitle": tracktitle,
            "year": year,
            "isrc": isrc,
        }

        # if loading tags from a text file, it parses the contents of the txt
        # and assigns the values to local vars
        # (by unpacking), also fills tags dict.
        if from_file is not None:
            (tags,
             file,
             files_directory,
             parse_title_capitalize,
             parse_title_as_is,
             parse_title_clean,
             parse_track_number) = parse_from_file(tags,
                                                   file,
                                                   files_directory,
                                                   from_file,
                                                   parse_title_capitalize,
                                                   parse_title_as_is,
                                                   parse_title_clean,
                                                   parse_track_number)

        actual_files = file_walker(files_directory, file)

        tags_to_set = tag_validator(parse_title_as_is, parse_title_capitalize,
                                    parse_title_clean, parse_track_number,
                                    **tags)

        wrapper_loop(actual_files, tags_to_set, parse_title_capitalize,
                     parse_title_as_is, parse_title_clean, parse_track_number)

    except utilities.custom_exceptions.ExpectedTermination as et:
        print(et)
        print("Now exiting")
        exit(0)

    except utilities.custom_exceptions.UnexpectedTermination as ut:
        print(ut)
        print("ERROR: NOW EXITING")
        exit(1)

    except Exception as e:
        print(e)
        print("UNCAUGHT EXCEPTION: NOW EXITING")
        exit(1)


def parse_from_file(tags: dict,
                    file: str,
                    files_directory: str,
                    from_file: str,
                    parse_title_capitalize: str,
                    parse_title_as_is: str,
                    parse_title_clean: str,
                    parse_track_number: str) -> tuple:
    '''
    Receives the tags dict, file vars and parse flags.
    Maps the values from the given text file.
    -----
    Returns: a tuple (tags, file, files_directory, parse_title_capitalize
    parse_title_as_is, title).
    '''

    file_validation(from_file=from_file)

    with open(from_file, 'r') as text_file:
        lines = text_file.readlines()

        for line in lines:

            # lines split in key tmp[0] - value tmp[1] pairs
            tmp = line.split("=", 1)

            # this is for regular tags only
            # they are added to tags dict
            if tmp[0] in tags.keys():
                tags[tmp[0]] = tmp[1].strip()

                try:
                    if tmp[0] in con.INT_TAGS:
                        tags[tmp[0]] = int(tags[tmp[0]])
                except Exception as e:
                    raise utilities.custom_exceptions.\
                        UnexpectedTermination("The following tag" +
                                              " is expected to" +
                                              f" be a number: {tmp[0]}") from e

            elif tmp[0] == "file":
                file = tmp[1].strip()

            elif tmp[0] == "files-directory":
                files_directory = tmp[1].strip()

            elif tmp[0] == "parse-title-capitalize":
                parse_title_capitalize = tmp[1].strip()

            elif tmp[0] == "parse-title-as-is":
                parse_title_as_is = tmp[1].strip()

            elif tmp[0] == "parse-title-clean":
                parse_title_clean = tmp[1].strip()

            elif tmp[0] == "parse-track-number":
                parse_track_number = tmp[1].strip()

    return(tags,
           file,
           files_directory,
           parse_title_capitalize,
           parse_title_as_is,
           parse_title_clean,
           parse_track_number)


def validate_tags_types(**tags_to_set):
    '''
    Validates that each actual tag is of the expected type
    '''
    for tag in tags_to_set:
        if tag in con.STR_TAGS and not isinstance(tags_to_set[tag], str):
            message = (f"'{tag}' is expected to be a sequence of characters.")
            raise utilities.custom_exceptions.UnexpectedTermination(message)
        elif tag in con.INT_TAGS and not isinstance(tags_to_set[tag], int):
            message = (f"'{tag}' is expected to be a sequence of numbers.")
            raise utilities.custom_exceptions.UnexpectedTermination(message)


def remove_empty_tags(**tags) -> dict:
    '''
    Returns a dict of the actual tags that are not None.
    '''
    tags_to_set = {}
    for key in tags:
        if tags[key] is not None:
            tags_to_set[key] = tags[key]
    return tags_to_set


def is_empty_or_has_parsers(parse_title_enabled: bool,
                            parse_track_number: bool, **tags) -> None:
    '''
    Checks that there is at least 1 tag set, title parser is enabled or
    else terminates the process with 0.
    '''

    all_none = True
    for key in tags:
        if tags[key] is not None:
            all_none = False

    if parse_title_enabled or parse_track_number:
        all_none = False

    if all_none:
        message = ("No tags specified.")
        raise utilities.custom_exceptions.ExpectedTermination(message)


def file_validation(file=None, files_directory=None, from_file=None) -> None:
    '''
    Validates that there is a file, a directory or a text file.
    '''

    if file is None and files_directory is None and from_file is None:
        message = ("No file, directory or text file specified.")
        raise utilities.custom_exceptions.ExpectedTermination(message)

    if file:
        if not path.exists(file):
            message = (f"> File not found: {file}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)
        if not path.isfile(file):
            message = (f"> Not a file: {file}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)
        f = magic.from_file(file, mime=True)
        if not f.startswith("audio/"):
            message = (f"> Not an audio file: {file}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)

    if files_directory:
        if not path.exists(files_directory):
            message = (f"> Dir not found: {files_directory}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)
        if not path.isdir(files_directory):
            message = (f"> Not a dir: {files_directory}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)

    if from_file:
        if not path.exists(from_file):
            message = (f"> File not found: {from_file}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)
        if not path.isfile(from_file):
            message = (f"> Not a file: {from_file}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)
        f = magic.from_file(from_file, mime=True)
        if not f == "text/plain":
            message = (f"> Not a text file: {from_file}")
            raise utilities.custom_exceptions.UnexpectedTermination(message)


def base_audio_wrapper(file, **tags_to_set):
    '''
    send and write tags to file.
    - Raises NotImplementedError and UnexpectedTermination if error when
    loading file.
    - Raises TypeError and UnexpectedTermination if error in type of value in
    tag.
    - Raises Exception and UnexpectedTermination.
    '''
    try:
        audio_file = audio.base_audio.BaseAudio()
        audio_file.load_track(file)
        audio_file.set_tags(**tags_to_set)
        audio_file.write_tags()
    except NotImplementedError as nie:
        message = (f"Error while loading file: {file}")
        raise utilities.custom_exceptions.UnexpectedTermination(message)\
            from nie
    except TypeError as te:
        raise utilities.custom_exceptions.UnexpectedTermination from te
    except Exception as e:
        raise utilities.custom_exceptions.UnexpectedTermination from e


def file_walker(files_directory: str, file: str) -> list:
    '''
    Receives a path to a directory and returns a list of it's files.
    If only a file is received, returns that file in a list.
    If no file is received, ValueError is raised.
    '''

    file_validation(file, files_directory)

    # look for all files in dir if valid
    if files_directory:
        actual_files = list(
                        filter(
                            lambda a: a.split(".")[-1] in con.VALID_EXTENSIONS,
                            listdir(files_directory))
                        )

        for i in range(len(actual_files)):
            actual_files[i] = files_directory + con.FILE_DELIMIT +\
             actual_files[i]
    # else just 1 file
    else:
        actual_files = [file]

    return actual_files


def tag_validator(parse_title_as_is: str,
                  parse_title_capitalize: str,
                  parse_title_clean: str,
                  parse_track_number: str,
                  **tags) -> dict:
    '''
    Validates that there is at least 1 tag set, or that there is a title parser
    enabled. Removes empty tags form dict, and validates that tags are of
    of proper type. Returns the setted tags.
    '''
    is_empty_or_has_parsers((parse_title_as_is
                             or parse_title_capitalize
                             or parse_title_clean),
                            parse_track_number, **tags)
    clean_tags = remove_empty_tags(**tags)

    validate_tags_types(**clean_tags)

    return clean_tags


def wrapper_loop(actual_files: list,
                 tags_to_set: dict,
                 parse_title_capitalize: str,
                 parse_title_as_is: str,
                 parse_title_clean: str,
                 parse_track_number: str
                 ):
    '''
    Starts the process.
    - Raises re.error amd ExpectedTermination if invalid regex.
    - Raises ValueError if parse_track_number parses a non-int.
    - Raises NotImplementedError and UnexpectedTermination if error when
    loading file.
    - Raises TypeError and UnexpectedTermination if error in type of value in
    tag.
    - Raises Exception and UnexpectedTermination.
    '''
    for a_file in actual_files:

        # If parse from title is set, then each time a track is received,
        # the file name will be parsed to extract the track title and
        # added to the tags to set dict. Since its called for all
        # tracks, it will always update before setting the tags to file.
        if parse_title_capitalize:
            try:
                tags_to_set["tracktitle"] =\
                    _op_str_matchers.\
                    extract_track_title_capitalize(a_file,
                                                   parse_title_capitalize)
            except error as er:
                raise utilities.custom_exceptions.ExpectedTermination(
                    f"Invalid Regex: {parse_title_capitalize}") from er
            except Exception as e:
                raise utilities.custom_exceptions.\
                    UnexpectedTermination() from e

        if parse_title_as_is:
            try:
                tags_to_set["tracktitle"] =\
                    _op_str_matchers.\
                    extract_track_title_as_is(a_file,
                                              parse_title_as_is)
            except error as er:
                raise utilities.custom_exceptions.ExpectedTermination(
                    f"Invalid Regex: {parse_title_as_is}") from er
            except Exception as e:
                raise utilities.custom_exceptions.\
                    UnexpectedTermination() from e

        if parse_title_clean:
            try:
                tags_to_set["tracktitle"] =\
                    _op_str_matchers.\
                    extract_track_title_cleanup_and_capitalize(
                        a_file,
                        parse_title_clean
                    )
            except error as er:
                raise utilities.custom_exceptions.ExpectedTermination(
                    f"Invalid Regex: {parse_title_clean}") from er
            except Exception as e:
                raise utilities.custom_exceptions.\
                    UnexpectedTermination() from e

        if parse_track_number:
            try:
                tags_to_set["tracknumber"] =\
                    _op_str_matchers.\
                    extract_track_number(a_file,
                                         parse_track_number)
            except error as er:
                raise utilities.custom_exceptions.ExpectedTermination(
                    f"Invalid Regex: {parse_track_number}") from er
            except TypeError as te:
                raise utilities.custom_exceptions.UnexpectedTermination(
                    "Tried to parse a string of characters for 'tracktitle'"
                ) from te
            except Exception as e:
                raise utilities.custom_exceptions.\
                    UnexpectedTermination() from e

        base_audio_wrapper(a_file, **tags_to_set)


if __name__ == "__main__":
    cli()
