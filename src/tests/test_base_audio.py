from unittest import TestCase
from pathlib import Path
from sys import platform
import mutagen

from EzAudioMeta.audio import base_audio


class TestBaseAudio(TestCase):

    def setUp(self) -> None:
        self.current_directory = str(Path(__file__).parent.absolute())
        if platform.startswith("win32"):
            self.file_delimit = "\\"
        elif platform.startswith("linux"):
            self.file_delimit = "/"
        self.path_to_test_files = str(self.current_directory) + self.file_delimit + "test_files"
        self.reset_default_tags()

    def test_load_track(self) -> None:
        '''
        When an audio file path is specified, the file loader should:
        1. Load the audio file.
        2. All tags should be available be visible.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
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
        with self.assertRaises(Exception):
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
            audio_file = self.path_to_test_files + self.file_delimit + "audio_file_3.mp3"
            ba_audio = base_audio.BaseAudio()
            ba_audio.load_track(audio_file)

    def test_load_track_invalid_file_type(self) -> None:
        '''
        When a file path that is not an audio file is passed:
        1. Pass a file path to a non-audio file.
        2. Mutagen should handle this error, so a NotImplementedError
        is expected.
        '''
        with self.assertRaises(NotImplementedError):
            audio_file = self.path_to_test_files + self.file_delimit + "test_file_picture.jpg"
            ba_audio = base_audio.BaseAudio()
            ba_audio.load_track(audio_file)

    def test_get_tag(self) -> None:
        '''
        When querying for existing tags:
        1. A valid tag according to music-tag:
        https://pypi.org/project/music-tag/
        2. The tag from audio file 1 should have the title tag
        setted, so it should return the actual title of the file.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        self.assertEqual(ba_audio.get_tag("title"), "gloomy sky")

    def test_get_tag_non_setted_tag(self) -> None:
        '''
        When querying for an existing tag that is empty:
        1. A valid tag according to music-tag:
        https://pypi.org/project/music-tag/
        2. The tag from audio file 1 should not have the album artis tag
        setted, so it should return None.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        self.assertEqual(ba_audio.get_tag("albumartist"), None)

    def test_get_tag_invalid_tag(self) -> None:
        '''
        When querying for a tag that does not exist:
        1. An invalid tag according to music-tag:
        https://pypi.org/project/music-tag/
        2. try ti get a tag that does not exist, a KeyError exceprion
        is expected.
        '''
        with self.assertRaises(KeyError):
            audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
            ba_audio = base_audio.BaseAudio()
            ba_audio.load_track(audio_file)
            self.assertEqual(ba_audio.get_tag("Wolololo!"), None)

    def test_set_tag(self) -> None:
        '''
        When setting an existing valid tag:
        1. Pass a valid audio file.
        2. Change title tag.
        3. Re-read the file and check for changes. Title should have
        been resetted.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        new_title = "new_title"
        ba_audio.set_tag("title", new_title)
        ba_audio.write_tags()

        ba_audio_after_write = base_audio.BaseAudio()
        ba_audio_after_write.load_track(audio_file)
        self.assertEqual(ba_audio_after_write.get_tag("title"), new_title)

    def test_set_tag_invalid_tag(self) -> None:
        '''
        When setting an existing invalid tag:
        1. Pass a valid audio file.
        2. Try to change an invalid tag.
        3. KeyError exception is expected.
        '''
        with self.assertRaises(KeyError):
            audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
            ba_audio = base_audio.BaseAudio()
            ba_audio.load_track(audio_file)
            ba_audio.set_tag("Wolololo!", "this is invalid, my dude")

    def test_set_tag_empty_tag(self) -> None:
        '''
        When setting an empty valid tag:
        1. Pass a valid audio file.
        2. Change albumartist tag.
        3. Re-read the file and check for changes. Album artist should have
        been setted.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        new_title = "some album artist"
        ba_audio.set_tag("albumartist", new_title)
        ba_audio.write_tags()

        ba_audio_after_write = base_audio.BaseAudio()
        ba_audio_after_write.load_track(audio_file)
        self.assertEqual(ba_audio_after_write.get_tag("albumartist"),
                         new_title)

    def test_set_tag_expected_str(self) -> None:
        '''
        When trying to set a tag that is expected to be a str as a different
        type:
        1. Pass a valid audio file.
        2. Try to set title as an int.
        3. TypeError exception expected.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        with self.assertRaises(TypeError):
            ba_audio.set_tag('title', 15)

    def test_set_tag_expected_int(self) -> None:
        '''
        When trying to set a tag that is expected to be an int as a different
        type:
        1. Pass a valid audio file.
        2. Try to set tracknumber as a str.
        3. TypeError exception expected.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        with self.assertRaises(TypeError):
            ba_audio.set_tag('tracknumber', "15")

    def test_set_tags(self) -> None:
        '''
        When attempting to set multiple tags:
        1. Pass a dictionary with the tags as keys, and values as the
        tag values to be setted.
        2. All tags should be setted.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)

        tags = {
            "album": "dis is my album",
            "albumartist": "my artist",
            "comment": "hai domo",
            "compilation": 1,
            "composer": "Johan Switcheroo",
            "discnumber": 1,
            "genre": "Progressive Electro-Cumbia",
            "lyrics": "OwO",
            "totaldiscs": 2,
            "totaltracks": 38,
            "tracknumber": 5,
            "tracktitle": "Perreo Intenso Progresivo: Parte I",
            "year": 1999,
            "isrc": "The hell is this",
        }

        ba_audio.set_tags(**tags)
        ba_audio.write_tags()

        ba_audio_after_write = base_audio.BaseAudio()
        ba_audio_after_write.load_track(audio_file)
        for key in tags:
            self.assertEqual(ba_audio_after_write.get_tag(key), tags[key])

    def test_set_tags_subset(self) -> None:
        '''
        When attempting to set multiple tags, but not all:
        1. Pass a dictionary with the tags as keys, and values as the
        tag values to be setted.
        2. Subset tags should be setted.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)

        tags = {
            "album": "dis is my album",
            "albumartist": "my artist",
            "comment": "hai domo",
            "compilation": 1,
            "tracktitle": "Perreo Intenso Progresivo: Parte I",
            "year": 1999,
            "isrc": "The hell is this",
        }

        ba_audio.set_tags(**tags)
        ba_audio.write_tags()

        ba_audio_after_write = base_audio.BaseAudio()
        ba_audio_after_write.load_track(audio_file)
        for key in tags:
            self.assertEqual(ba_audio_after_write.get_tag(key), tags[key])

    def test_set_tags_subset_invalid_tag(self) -> None:
        '''
        When attempting to set multiple tags, but one is an invalid tag:
        1. Pass a dictionary with the tags as keys, and values as the
        tag values to be setted.
        2. Subset tags should be setted.
        3. KeyError exception expected.
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)

        tags = {
            "album": "dis is my album",
            "albumartist": "my artist",
            "commmmment": "hai domo",
            "compilation": 1,
            "tracktitle": "Perreo Intenso Progresivo: Parte I",
            "year": 1999,
            "isrc": "The hell is this",
        }

        with self.assertRaises(KeyError):
            ba_audio.set_tags(**tags)
            for key in tags:
                self.assertEqual(ba_audio.get_tag(key), tags[key])

    def test_set_tags_delegate_except_to_set_tag(self) -> None:
        '''
        When attempting to set tags of the wrong type, the exception handling
        should be delegated to set_tag method.
        1. Pass a dictionary with the tags as keys, and values as the
        tag values to be setted.
        2. Set an int tag as an str.
        3. Set an int
        '''
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)

        tags = {
            "album": 16,
        }

        with self.assertRaises(TypeError):
            ba_audio.set_tags(**tags)
            for key in tags:
                self.assertEqual(ba_audio.get_tag(key), tags[key])

    def reset_default_tags(self) -> None:
        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_1.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        ba_audio.set_tag("artist", "Dee Yan-Key")
        ba_audio.set_tag("album", "little night thoughts")
        ba_audio.set_tag("albumartist", "")
        ba_audio.set_tag("genre", "electroswing")
        ba_audio.set_tag("year", 2019)
        ba_audio.set_tag("tracknumber", 1)
        ba_audio.set_tag("title", "gloomy sky")
        ba_audio.write_tags()

        audio_file = self.path_to_test_files + self.file_delimit + "audio_file_2.mp3"
        ba_audio = base_audio.BaseAudio()
        ba_audio.load_track(audio_file)
        ba_audio.set_tag("artist", "Siddhartha Corsus")
        ba_audio.set_tag("album", "Fragments of Light")
        ba_audio.set_tag("tracknumber", 1)
        ba_audio.set_tag("title",
                         "Let Go of Time (and Time Will Let Go of You)")
        ba_audio.write_tags()

    def tearDown(self) -> None:
        self.reset_default_tags()
