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
