from unittest import TestCase
from pathlib import Path

from ezaudiometa.modules import base_audio


class TestBaseAudio(TestCase):

    def setUp(self) -> None:
        self.current_directory = str(Path(__file__).parent.absolute())
        self.path_to_test_files = str(self.current_directory) + "\\test_files"

    def test_load_track(self) -> None:
        '''
        When an audio file path is specified, the file loader should:
        1. Load the audio file.
        2. All tags should be available be visible.
        '''
        audio_file = self.path_to_test_files + "\\audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        self.assertEqual(ba_audio.get_tag("title"), "gloomy sky")
        self.assertEqual(ba_audio.get_tag("tracknumber"), "1")


