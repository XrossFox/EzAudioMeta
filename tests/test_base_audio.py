from unittest import TestCase
from pathlib import Path

import mutagen

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
        self.assertEqual(ba_audio.get_tag("tracknumber"), 1)

    def test_load_track_invalid_path_as_non_str(self) -> None:
        '''
        When an audio file path is not a string, an exceptionm must be raised:
        1. Pass a non str path.
        2. TypeError expected.
        '''
        audio_file = 45
        with self.assertRaises(TypeError):
            ba_audio = base_audio.BaseAudio()
            ba_audio.load_track(audio_file)

    def test_load_track_invalid_path(self) -> None:
        '''
        When an audio file path is a string, but the actual file is not a valid
        file.
        1. Pass a file path as a string, must not be a valid file (a
        file that doesn't exist)
        2. FileNotFoundError expected (also MutagenError).
        '''
        with self.assertRaises((FileNotFoundError, mutagen.MutagenError)):
            audio_file = self.path_to_test_files + "\\audio_file_3.mp3"
            ba_audio = base_audio.BaseAudio()
            ba_audio.load_track(audio_file)

    def test_load_track_invalid_file_type(self) -> None:
        '''
        When a file path that is not a an audio file is passed:
        1. Pass a file path to a non-audio file.
        2. Mutagen should handle this error, so a NotImplementedError
        is expected.
        '''
        with self.assertRaises(NotImplementedError):
            audio_file = self.path_to_test_files + "\\test_file_picture.jpg"
            ba_audio = base_audio.BaseAudio()
            ba_audio.load_track(audio_file)
