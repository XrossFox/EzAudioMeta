from music_tag import load_file


class BaseAudio:

    def __init__(self) -> None:
        self._current_file = None

    def load_track(self, file_path) -> None:
        '''
        Loads an audio file.
        '''
        self._current_file = load_file(file_path)

    def get_tag(self, tag_name) -> object:
        '''
        Returns the first value of the specified tag
        as a string or an integer (like track number or year).
        '''
        tag = self._current_file[tag_name]
        return tag.first

    def set_tag(self, tag_name, tag_value) -> None:
        '''
        Sets the tag of the audio file.
        tag_name -- The name of the tag to set.
        tag_value -- The new value for the tag.
        '''
        self._current_file[tag_name] = tag_value
