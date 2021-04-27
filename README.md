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
  --files-directory TEXT
  --from-file TEXT
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
#### Single file as an example: 
```bash
py main.py --file "track 01.mp3" --tracktitle "Perreando hasta el suelo"
--tracknumber "12" --album "Lucifer Se Fue De Rumba"
```
#### Directory as an example:
```bash
py main.py --files-directory "path/to/files" --artist "la wea masoquista" --album "lucifer se fue de rumba" --genre "electro cumbia progresiva" --year 1966
```
Note: Files are file system dependant, so if you are in windows: `path\to\file` and in linux: `path/to/file`. This script does distinguish between OSes (Windows and Linux so far)

#### Using --from-file:
This options lets you load the options from a text file, line by line, something like this:
```bash
file=value
files-directory=value
album=value
albumartist=value
artist=value
```
Please note that you shouldn't use `file` and `files-directory` together. Also note that all options are missing the `--` at the beginning, and there is an `=` for separation.

You should call the script like this: 
```bash
py main.py --from-file "path/to/your/text/file.txt"
```