import unittest

from utilities.optional_string_matchers import OptionalStringMatchers


class TestOptionalStringMatchers(unittest.TestCase):

    def test_extract_track_title_as_is_using_regex(self) -> None:
        '''
        1. Given an audio file name.
        2. And given a Regex expression.
        3. Return the track title from file name as is, that matches the regex.
        '''
        osm = OptionalStringMatchers()
        file_name = "03 Of Lillies And Remains.flac"
        pattern = "(?<=[0-9]\\s).+(?=\\.flac)"
        expected = "Of Lillies And Remains"
        track_title = osm.extract_track_title_as_is(file_name, pattern)
        self.assertEquals(expected, track_title)

    def test_extract_track_title_title_case_1(self) -> None:
        pass
        '''
        1. Given an audio file name with a weird mix of case alternation.
        2. And given a Regex expression.
        3. Return the track title from the file name by using title
        capitalization.
        '''
        osm = OptionalStringMatchers()

        file_name = "03 Of lILLIes AND remains.flac"
        pattern = "(?<=[0-9]\\s).+(?=\\.flac)"
        expected = "Of Lillies and Remains"

        track_title = osm.extract_track_title_title_capitalize(file_name,
                                                               pattern)

        self.assertEquals(expected, track_title)

    def test_extract_track_title_title_case_2(self) -> None:
        pass
        '''
        1. Given an audio file name with a weird mix of case alternation.
        2. And given a Regex expression.
        3. Return the track title from the file name by using title
        capitalization.
        '''
        osm = OptionalStringMatchers()
        file_name = "07.The Ballad Of Resurrection" +\
                    " Joe And Rosa Whore (Ilsa She-Wolf Of Hollywood]).flac"

        pattern = "(?<=[0-9]\\.).+(?=\\.flac)"

        expected = "The Ballad of Resurrection" +\
                   " Joe and Rosa Whore (Ilsa She-Wolf of Hollywood])"

        track_title = osm.extract_track_title_title_capitalize(file_name,
                                                               pattern)

        self.assertEquals(expected, track_title)

    def test_extract_track_title_title_case_3(self) -> None:
        pass
        '''
        1. Given an audio file name with a weird mix of case alternation.
        2. And given a Regex expression.
        3. Return the track title from the file name by using title
        capitalization.
        '''
        osm = OptionalStringMatchers()
        file_name = "10.Return Of The Phantom Stranger" +\
                    " (Tuesday Night At The Chop Shop Mix).flac"

        pattern = "(?<=[0-9]\\.).+(?=\\.flac)"
        expected = "Return of the Phantom Stranger" +\
                   " (Tuesday Night at the Chop Shop Mix)"

        track_title = osm.extract_track_title_title_capitalize(file_name,
                                                               pattern)

        self.assertEquals(expected, track_title)

    def test_extract_track_title_as_is_1(self) -> None:
        '''
        1. Given an audio file name.
        2. And given a Regex expression.
        3. Return the track title from the file name as is.
        '''
        osm = OptionalStringMatchers()
        file_name = "10.return of the phantom stranger" +\
                    " (tuesday night at the chop shop mix).flac"

        expected = "return of the phantom stranger " +\
                   "(tuesday night at the chop shop mix)"

        pattern = "(?<=[0-9]\\.).+(?=\\.flac)"

        track_title = osm.extract_track_title_as_is(file_name, pattern)

        self.assertEqual(expected, track_title)
