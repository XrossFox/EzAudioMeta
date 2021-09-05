# EzAudioMeta
[![Build Status](https://travis-ci.com/XrossFox/EzAudioMeta.svg?branch=main)](https://travis-ci.com/XrossFox/EzAudioMeta)
[![Build Status](https://travis-ci.com/XrossFox/EzAudioMeta.svg?branch=dev)](https://travis-ci.com/XrossFox/EzAudioMeta)

Python Script that allows you to re-name meta data fields from audio files in a
directory.

## Requirements:

- Python 3.9.1: It may work in lower versions, but i can't guarantee
anything. I made use of f-strings wherever i could, so i'd recommend Python 3.6 at
the very least.
- music-tag 0.4.2 (and it's dependencies)
- click 7.1.2
- python-magic==0.4.24
- python-magic-bin==0.4.14 (WINDOWS USERS ONLY)
- libmagic (NON-WINDOWS USERS ONLY, [CHECK HERE](https://github.com/ahupp/python-magic)

## Usage:

### For direct usage:

`py main.py --file path/to/audio/file [options]`

### Installing from pip:

`pip install EzAudioMeta`


`ezaudio --file path/to/audio/file [options]`

### Options:
Each option represents a tag to be set. All tags must be either text or a
number. Note that numbers can also be parsed from text, so if you pass
tracknumber tag as "15", it will work just fine. For safety, all text should be
encased between double quotes.
```bash
  --file TEXT
  --files-directory TEXT         Note: overrides --file option
  --from-file TEXT               Note: overrides --file and --files-directory
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
  --parse-title-capitalize TEXT  Parses the 'tracktitle' from the actual file
                                 name. The track title is capitalized as a
                                 title. You must provide a valid regex
                                 expresion. Ej. (?<=\d\d\s).+(?=\.flac).

  --parse-title-as-is TEXT       Parses the 'tracktitle' from the actual file
                                 name. The track title is left as is with no
                                 capitalization or processing. You must
                                 provide a valid regex expresion. Ej.
                                 (?<=\d\d\s).+(?=\.flac).

  --parse-title-clean TEXT       Parses the 'tracktitle' from the actual file
                                 name. The track title has all '-', '_' and
                                 multiple whitespaces removed and trimmed, and
                                 then it´s 'title capitalized'. You must provide a
                                 valid regex expresion. Ej.
                                 (?<=\d\d\s).+(?=\.flac).

  --parse-track-number TEXT      Parses the 'tracknumber' from the actual file
                                 name. You must provide a valid regex
                                 expresion. Ej. \d+(?=.+\.mp3).
  --help                 Show this message and exit.
```
### Single file as an example: 
```bash
ezaudio --file "track 01.mp3" --tracktitle "Track Title"
--tracknumber "12" --album "Album Name"
```
### Directory as an example:
```bash
ezaudio --files-directory "path/to/files" --artist "Artist" --album "Album Name" --genre "Genre" --year 1966
```
Note: Files are file system dependant, so if you are in windows: `path\to\file` and in linux: `path/to/file`. This script does distinguish between OSes (Windows and Linux so far)

### Using --from-file:
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
ezaudio --from-file "path/to/your/text/file.txt"
```

### Parsing track titles from file name using Regex.
EzAudioMeta allows you to parse the 'tracktitle' tag from the actual file name using regular expressions. Usage is as follows 
```bash
ezaudio --from-file "path/to/your/text/file.txt" --parse-title-capitalize "(?<=\d\d\s).+(?=\.flac)"
```
Given an audio file `01 my_track_title.flac`, the expected result should be:

- `--parse-title-capitalize`: My_Track_Title
- `--parse-title-as-is`: my_track_title
- `--parse-title-clean`: My Track Title

### Parsing track number from file using regex.
You can also get the track number from the audio file using regex:
```bash
ezaudio --file "path\to\39_audio_test_file_3.mp3" --parse-track-number "\d+(?=.+\1.mp3)"
```
track number gets tagged as 39.
If no match is found, 0 is assigned by default.
