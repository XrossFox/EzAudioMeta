# EzAudioMeta
WIP

Python Script that allows you to re-name meta data fields from audio files in a
directory.

## The usage so far:

Requirements:
- Python 3.9.1: Maaaaybe it might work in lower versions, but can't guarantee
anything. I made use of f-strings where i could, so i'd recommend Python 3.6 at
the very least-
- mutagen 1.45.1 (and it's dependencies)
- Click 7.1.2.

### Usage:
`py main.py --file path/to/audio/file [options]`

### Options:
Each option represents a tag to be set. All tags must be either text or a
number. Note that numbers can also be parsed from text, so if you pass
tracknumber tag as "15", it will work just fine. For safety, all text should be
encased between double quotes.
```bash
  --file TEXT
  --album TEXT
  --albumartist TEXT
  --artist TEXT
  --comment TEXT
  --compilation INTEGER
  --composer TEXT
  --discnumber INTEGER
  --genre TEXT
  --lyrics TEXT
  --totaldiscs INTEGER
  --totaltracks INTEGER
  --tracknumber INTEGER
  --tracktitle TEXT
  --year INTEGER
  --isrc TEXT
  --help                 Show this message and exit.
```
As an example: 
```bash
py main.py --file "track 01.mp3" --tracktitle "Perreando hasta el suelo"
--tracknumber "12" --album "Lucifer Se Fue De Rumba"
```
