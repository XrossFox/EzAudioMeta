import unittest
from pathlib import Path
from click.testing import CliRunner

from audio import base_audio
from main import cli


class TestCli(unittest.TestCase):

    def setUp(self) -> None:
        self.current_directory = str(Path(__file__).parent.absolute())
        self.path_to_test_files = str(self.current_directory) + "\\test_files"

    def tearDown(self) -> None:
        self.reset_default_tags()

    def test_run_cli_no_audio_file(self):
        '''
        When attempting to run the CLI without a specified audio file:
        1. invoke the cli without file parameter.
        2. Error code 0 expected.
        3. Message: "No file specified.\n"
        '''
        runner = CliRunner()
        result = runner.invoke(cli)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "No file specified.\n")

    def test_run_cli_no_tag(self):
        '''
        When attempting to run the CLI without any tag specified.
        1. Invoke clu with valid file.
        2. Error code 0 expected.
        3. Message: "No tags specified.\n#
        '''
        audio_file = self.path_to_test_files + "\\audio_file_1.mp3"
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
        audio_file = self.path_to_test_files + "\\audio_file_1.mp3"
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
        audio_file = self.path_to_test_files + "\\audio_file_1.mp3"
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
        audio_file = self.path_to_test_files + "\\audio_file_1.mp3"
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
        audio_file = self.path_to_test_files + "\\audio_file_1.mp3"
        runner = CliRunner()
        new_title = 15
        result = runner.invoke(cli, ["--file", audio_file,
                                     "--tracktitle", new_title])
        self.assertEqual(result.exit_code, 0)
        expected = "'tracktitle' is expected to be a sequence of characters.\n"
        self.assertEqual(result.output, expected)

    def reset_default_tags(self) -> None:
        audio_file = self.path_to_test_files + "\\audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        ba_audio.set_tag("artist", "Dee Yan-Key")
        ba_audio.set_tag("album", "little night thoughts")
        ba_audio.set_tag("genre", "electroswing")
        ba_audio.set_tag("year", 2019)
        ba_audio.set_tag("tracknumber", 1)
        ba_audio.set_tag("title", "gloomy sky")
        ba_audio.write_tags()

        audio_file = self.path_to_test_files + "\\audio_file_2.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        ba_audio.set_tag("artist", "Siddhartha Corsus")
        ba_audio.set_tag("album", "Fragments of Light")
        ba_audio.set_tag("tracknumber", 1)
        ba_audio.set_tag("title",
                         "Let Go of Time (and Time Will Let Go of You)")
        ba_audio.write_tags()
