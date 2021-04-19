from os import path, listdir
from sys import platform
import click
from audio import base_audio

str_tags = ["album", "albumartist", "comment", "composer", "genre",
            "lyrics", "tracktitle", "isrc", "artist"]

valid_extensions = ["aac", "aiff", "dsf", "flac", "m4a", "mp3", "ogg", "opus","wav", "wv"]

if platform.startswith("win32"):
    file_delimit = "\\"
elif platform.startswith("linux"):
    file_delimit = "/"


@click.command()
@click.option('--file', type=str)
@click.option('--files-directory', type=str)
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
def cli(file, files_directory, album, albumartist, artist, comment,
        compilation,
        composer, discnumber, genre, lyrics,
        totaldiscs, totaltracks,
        tracknumber, tracktitle, year, isrc):
    '''
    This CLI application receives an audio file and the tags that are to be
    setted/changed. Most tags are expected to be character
    strings, but some like 'tracknumber' are numbers. At least a file and a tag
    are expected to be set.
    '''

    file_validation(file, files_directory)

    # look for all files in dir if valid
    if files_directory and not file:
        actual_files = list(filter(lambda a: a.split(".")[-1] in valid_extensions,listdir(files_directory)))
        for i in range(len(actual_files)):
            actual_files[i] = files_directory + file_delimit + actual_files[i]
    # else just 1 file
    else:
        actual_files = [file]

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

    tags_validation(**tags)

    tags_to_set = actual_tags(**tags)

    validate_tags_types(**tags_to_set)

    for a_file in actual_files:
        base_audio_wrapper(a_file, **tags_to_set)

def validate_tags_types(**tags_to_set):
    '''
    Validates that each actual tag is of the expected type
    '''
    for tag in tags_to_set:
        if tag in str_tags and not isinstance(tags_to_set[tag], str):
            print(f"'{tag}' is expected to be a sequence of characters.")
            exit(1)


def actual_tags(**tags) -> dict:
    '''
    Returns a dict of the actual tags that are not None.
    '''
    tags_to_set = {}
    for key in tags:
        if tags[key] is not None:
            tags_to_set[key] = tags[key]
    return tags_to_set


def tags_validation(**tags):
    '''
    Checks that there is at least 1 tag set
    '''

    all_none = True
    for key in tags:
        if tags[key] is not None:
            all_none = False

    if all_none:
        print("No tags specified.")
        exit(0)


def file_validation(file=None, files_directory=None) -> None:
    '''
    Validates that there is a file or a directory passed.
    '''

    if file is None and files_directory is None:
        print("No file or directory specified.")
        exit(0)

    if file:
        if not path.exists(file):
            print("Your file does not actually exists :c")
            exit(1)
        if not path.isfile(file):
            print("The specified File is not an actual File >:P")
            exit(1)

    if files_directory:
        if not path.exists(files_directory):
            print("Your directory does not actually exists :c")
            exit(1)
        if not path.isdir(files_directory):
            print("The specified directory is not an actual directory >:P")
            exit(1)


def base_audio_wrapper(file, **tags_to_set):
    '''
    send and write tags to file
    '''
    audio_file = base_audio.BaseAudio()
    audio_file.load_track(file)
    audio_file.set_tags(**tags_to_set)
    audio_file.write_tags()


if __name__ == "__main__":
    cli()
