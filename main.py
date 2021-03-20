import click
from audio import base_audio


@click.command()
@click.option('--file', type=str)
@click.option('--album', type=str)
@click.option('--albumartist', type=str)
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
def cli(file, album, albumartist, comment, compilation,
        composer, discnumber, genre, lyrics,
        totaldiscs, totaltracks,
        tracknumber, tracktitle, year, isrc):
    '''
    This CLI application receives an audio file and the tags that are to be
    setted/changed. Most tags are expected to be character
    strings, but some like 'tracknumber' are numbers. At least a file and a tag
    are expected to be set.
    '''
    if file is None:
        print("No file specified.")
        return

    tags = {
        "album": album,
        "albumartist": albumartist,
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
    all_none = True

    for key in tags:
        if tags[key] is not None:
            all_none = False

    if all_none:
        print("No tags specified.")
        return

    tags_to_set = {}
    for key in tags:
        if tags[key] is not None:
            tags_to_set[key] = tags[key]

    audio_file = base_audio.BaseAudio()
    audio_file.load_track(file)
    audio_file.set_tags(**tags_to_set)
    audio_file.write_tags()


if __name__ == "__main__":
    cli()
