from sys import platform

# String-type tags
STR_TAGS = ["album", "albumartist", "comment", "composer", "genre",
            "lyrics", "tracktitle", "isrc", "artist"]

# Int-type tags
INT_TAGS = ["compilation", "discnumber", "totaldiscs", "totaltracks",
            "tracknumber", "year", ]

# Valid audio file extensions
VALID_EXTENSIONS = ["aac", "aiff", "dsf", "flac", "m4a", "mp3",
                    "ogg", "opus", "wav", "wv"]

# Platform file system delimiter
if platform.startswith("win32"):
    FILE_DELIMIT = "\\"
elif platform.startswith("linux"):
    FILE_DELIMIT = "/"

# Help strings
PARSE_CAP_HELP = "Parses the 'tracktitle' from the actual file name." +\
    " The track title is capitalized as a title." +\
    " You must provide a valid regex expresion." +\
    " Ej. (?<=\\d\\d\\s).+(?=\\.flac)."
PARSE_ASIS_HELP = "Parses the 'tracktitle' from the actual file name." +\
    " The track title is left as is with no capitalization or processing." +\
    " You must provide a valid regex expresion." +\
    " Ej. (?<=\\d\\d\\s).+(?=\\.flac)."
PARSE_CLEAN_HELP = "Parses the 'tracktitle' from the actual file name." +\
    " The track title has all '-', '_' and multiple whitespaces " +\
    "removed and trimmed, and then it´s 'title capitalized'." +\
    " You must provide a valid regex expresion." +\
    " Ej. (?<=\\d\\d\\s).+(?=\\.flac)."
PARSE_TRACK_NUMBER = "Parses the 'tracknumber' from the actual file name." +\
    " You must provide a valid regex expresion." +\
    " Ej. \\d+(?=.+\\.mp3)."
HELP_FILES_DIR = "Note: overrides --file option"
HELP_FROM_FILE = "Note: overrides --file and --files-directory"