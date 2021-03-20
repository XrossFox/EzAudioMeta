import click
from audio import base_audio


@click.command()
@click.option('--file', type=str)
@click.option('--album', type=str)
@click.option('--albumartist', type=str)
@click.option('--comment', type=str)
@click.option('--compilation', type=int)
@click.option('--composer', type=str)
@click.option('--discnumber', type=str)
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
    strings, but some like 'tracknumber' are numbers.
    '''
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
    print(tags)


if __name__ == "__main__":
    cli()
