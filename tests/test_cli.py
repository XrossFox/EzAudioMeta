import unittest
from pathlib import Path
from sys import platform
from random import randrange

from click.testing import CliRunner

from audio import base_audio
from main import cli


class TestCli(unittest.TestCase):

    def setUp(self) -> None:
        self.current_directory = str(Path(__file__).parent.absolute())
        if platform.startswith("win32"):
            self.file_delimit = "\\"
        elif platform.startswith("linux"):
            self.file_delimit = "/"
        self.path_to_test_files = \
            str(self.current_directory) + self.file_delimit + "test_files"

        self.reset_default_tags()

    def tearDown(self) -> None:
        self.reset_default_tags()

    def test_run_cli_no_audio_file(self):
        '''
        When attempting to run the CLI without a specified audio file:
        1. invoke the cli without file parameter.
        2. Error code 0 expected.
        3. Message: "No file or directory specified.\n"
        '''
        runner = CliRunner()
        result = runner.invoke(cli)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "No file or directory specified.\n")

    def test_run_cli_invalid_file(self):
        '''
        When attempting to run the CLI without a specified audio file:
        1. invoke the cli with a directory instead of a file.
        2. Error code 1 expected.
        3. Message: "The specified File is not an actual File >:P"
        '''
        audio_directory = self.path_to_test_files
        runner = CliRunner()
        new_title = "Perreando con Lucifer"
        result = runner.invoke(cli, ["--file", audio_directory,
                                     "--tracktitle", new_title])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output, "The specified File is not an"
                                        + " actual File >:P\n")

    def test_run_cli_file_does_not_exist(self):
        '''
        When attempting to run the CLI without a specified audio file:
        1. invoke the cli with a file that does not exist.
        2. Error code 1 expected.
        3. Message: "Your File does not actually exists :c"
        '''
        audio_directory = \
            self.path_to_test_files + self.file_delimit + "Rumba Generica.mp3"

        runner = CliRunner()
        new_title = "Perreando con Lucifer"
        result = runner.invoke(cli, ["--file", audio_directory,
                                     "--tracktitle", new_title])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output, "Your file does not actually"
                                        + " exists :c\n")

    def test_run_cli_no_tag(self):
        '''
        When attempting to run the CLI without any tag specified.
        1. Invoke clu with valid file.
        2. Error code 0 expected.
        3. Message: "No tags specified.\n#
        '''
        audio_file = \
            self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        runner = CliRunner()
        result = runner.invoke(cli, ["--file", audio_file])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "No tags specified.\n")

    def test_run_cli_set_tracktitle(self):
        '''
        When attempting to tun the CLI and set tracktitle tag:
        1. Pass a valid audio file.
        2. set the 'tracktitle' tag.
        3. check for changes.
        '''
        audio_file = \
            self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        runner = CliRunner()
        new_title = "Perreando con Lucifer"
        result = runner.invoke(cli, ["--file", audio_file,
                                     "--tracktitle", new_title])
        self.assertEqual(result.exit_code, 0)

        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        self.assertEqual(ba_audio.get_tag("tracktitle"), new_title)

    def test_run_cli_set_tracktitle_and_album_and_genre(self):
        '''
        When attempting to tun the CLI and set tracktitle tag:
        1. Pass a valid audio file.
        2. set the 'tracktitle', 'album', and 'genre' tags.
        3. check for changes.
        '''
        audio_file = \
            self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        runner = CliRunner()
        new_title = "Perreando con Lucifer"
        new_album = "Satanas se Fue de Rumba"
        new_genre = "Techno-Cumbia Norteña Progresiva"
        result = runner.invoke(cli, ["--file", audio_file,
                                     "--tracktitle", new_title,
                                     "--album", new_album,
                                     "--genre", new_genre])
        self.assertEqual(result.exit_code, 0)

        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        self.assertEqual(ba_audio.get_tag("tracktitle"), new_title)
        self.assertEqual(ba_audio.get_tag("album"), new_album)
        self.assertEqual(ba_audio.get_tag("genre"), new_genre)
        audio_file = \
            self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        runner = CliRunner()
        new_title = "Perreando con Lucifer"
        result = runner.invoke(cli, ["--file", audio_file,
                                     "--tracktitle", new_title])
        self.assertEqual(result.exit_code, 0)

    def test_run_cli_str_option_is_not_str(self):
        '''
        When attempting to set an str option as a non str:
        1. Pass a valid audio file.
        2. set 'tracktitle' as an int.
        3. the cli should throw a message: '<option-name> expected to be
        str'
        '''
        audio_file = \
            self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        runner = CliRunner()
        new_title = 15
        result = runner.invoke(cli, ["--file", audio_file,
                                     "--tracktitle", new_title])
        self.assertEqual(result.exit_code, 1)
        expected = "'tracktitle' is expected to be a sequence of characters.\n"
        self.assertEqual(result.output, expected)

    def test_run_cli_all_files(self):
        '''
        When attempting to change the meta tags of all valid audio files in
        a directory:
        1. Pass a valid directory.
        2. Attempt to change the artist of all files.
        3. Check for changes.
        '''

        audio_files_path = self.path_to_test_files
        audio_file_1 = \
            self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        audio_file_2 = \
            self.path_to_test_files + self.file_delimit + "audio_file_2.mp3"
        new_artist = "Lucifer"

        runner = CliRunner()
        result = runner.invoke(cli, ["--files-directory", audio_files_path,
                                     "--artist", new_artist
                                     ])

        self.assertEqual(result.exit_code, 0)
        audio = base_audio.BaseAudio()
        audio.load_track(audio_file_1)
        self.assertEqual(audio.get_tag("artist"), new_artist)
        audio.load_track(audio_file_2)
        self.assertEqual(audio.get_tag("artist"), new_artist)

    def test_run_cli_from_text_file_single_file(self):
        '''
        When attempting to set tags to a single file from a text file
        1. Load a text file with the expected tags.
        2. The syntax should be ass follows:
        option=value
        option=value
        3. All options remain the same, just without the first two hyphens at
        the beginning,
        so --file becomes file and --files-directory becomes files-directory.
        4. Only one option per line.
        '''
        tags_and_values = {
            "artist": "Los Luciferinos",
            "album": "Rumbeando en el Noveno Infierno",
            "tracktitle": "El Perreo de Lilith",
            "file": self.path_to_test_files + self.file_delimit +
            "audio_file_1.mp3",
            "year": 1984
        }

        options = self.to_options(**tags_and_values)

        test_file_txt = self.write_to_test_text_file(*options)

        runner = CliRunner()
        result = runner.invoke(cli, ["--from-file", test_file_txt])

        self.assertEqual(result.exit_code, 0)

        audio = base_audio.BaseAudio()
        audio.load_track(tags_and_values["file"])

        for key in tags_and_values:

            if key == "file":
                continue

            self.assertEqual(audio.get_tag(key), tags_and_values[key])

    def test_run_cli_from_text_file_multiple_files(self):
        '''
        When attempting to set tags to multiple files in a directory from
        a text file
        1. Load a text file with the expected tags. Pointing to
        a directory with multiple audio files.
        2. The syntax should be as follows:
        option=value
        option=value
        3. All options remain the same, just without the first two hyphens at
        the beginning,
        so --file becomes file and --files-directory becomes files-directory.
        4. Only one option per line.
        '''
        tags_and_values = {
            "artist": "Los Luciferinos",
            "album": "Rumbeando en el Noveno Infierno",
            "files-directory": self.path_to_test_files,
            "year": 1984
        }

        options = self.to_options(**tags_and_values)

        test_file_txt = self.write_to_test_text_file(*options)

        runner = CliRunner()
        result = runner.invoke(cli, ["--from-file", test_file_txt])

        self.assertEqual(result.exit_code, 0)

        audio = base_audio.BaseAudio()
        audio.load_track(tags_and_values["files-directory"] +
                         self.file_delimit +
                         "audio_file_1.mp3")

        for key in tags_and_values:

            if key == "files-directory":
                continue

            self.assertEqual(audio.get_tag(key), tags_and_values[key])

        audio.load_track(tags_and_values["files-directory"] +
                         self.file_delimit +
                         "audio_file_2.mp3")

        for key in tags_and_values:

            if key == "files-directory":
                continue

            self.assertEqual(audio.get_tag(key), tags_and_values[key])

    def test_run_cli_from_text_file_doesnt_exist(self):
        '''
        When attempting to load tags from a file, with a missing text file.
        1. Attempt to load a text file that is not valid.
        2. An exception should be raised.
        '''

        runner = CliRunner()
        inv = "invalid"
        result = runner.invoke(cli, ["--from-file", inv])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output, f"{inv} doesn't exist\n")

    def test_run_cli_from_text_file_file_is_not_file(self):
        '''
        When attempting to load tags from a file, with a missing text file.
        1. Attempt to load a text file that is not valid.
        2. An exception should be raised.
        '''
        runner = CliRunner()
        inv = self.path_to_test_files
        result = runner.invoke(cli, ["--from-file", inv])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.output, f"{inv} is not a valid file\n")

    def to_options(self, **tags_and_values) -> list:
        '''
        Receives a dictionary of 'tag: value' pair and creates a list from
        it. The list is parsed as follows: tag=value\\n. This list
        is meant to be written to the test file using
        write_to_test_text_file().
        '''
        options = list()
        for key in tags_and_values:

            options.append(key + "=" + str(tags_and_values[key])+"\n")

        return options

    def write_to_test_text_file(self, *lines_to_write) -> str:
        """
        Receives a list of arguments of strings that are gong to be written
        to a text file. Returns the absolute path to the text file generated.
        The text file is named in the following pattern:
        test_text_file_<random_number>.txt\n
        The random number is between 1 and 10,000.
        """
        test_file_path = self.path_to_test_files + self.file_delimit + \
            "test_text_file_" + \
            str(randrange(1, 10000)) + ".txt"

        with open(test_file_path, mode="w") as test_file:
            test_file.writelines(lines_to_write)

        return test_file_path

    def reset_default_tags(self) -> None:
        audio_file = \
            self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        ba_audio.set_tag("artist", "Dee Yan-Key")
        ba_audio.set_tag("album", "little night thoughts")
        ba_audio.set_tag("genre", "electroswing")
        ba_audio.set_tag("year", 2019)
        ba_audio.set_tag("tracknumber", 1)
        ba_audio.set_tag("title", "gloomy sky")
        ba_audio.write_tags()

        audio_file = \
            self.path_to_test_files + self.file_delimit + "audio_file_2.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        ba_audio.set_tag("artist", "Siddhartha Corsus")
        ba_audio.set_tag("album", "Fragments of Light")
        ba_audio.set_tag("tracknumber", 1)
        ba_audio.set_tag("title",
                         "Let Go of Time (and Time Will Let Go of You)")
        ba_audio.write_tags()
