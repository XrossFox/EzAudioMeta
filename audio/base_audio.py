from music_tag import load_file


class BaseAudio:

    def __init__(self) -> None:
        self._current_file = None
        self.str_tags = [
                    "album",
                    "albumartist",
                    "artist",
                    "artwork",
                    "comment",
                    "composer",
                    "genre",
                    "lyrics",
                    "tracktitle",
                    "isrc",
                    "title",
        ]
        self.int_tags = [
                    "compilation",
                    "discnumber",
                    "totaldiscs",
                    "totaltracks",
                    "tracknumber",
                    "year",
        ]

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
        ---
        The following tags are expected to be str:
        album
        albumartist
        artist
        artwork
        comment
        composer
        genre
        lyrics
        tracktitle | title
        isrc
        ---
        The following tags are expected to be int:
        compilation
        discnumber
        totaldiscs
        totaltracks
        tracknumber
        year
        '''
        if tag_name in self.str_tags and not isinstance(tag_value, str):
            raise TypeError(f"{tag_name} is expected to be of type str")
        if tag_name in self.int_tags and not isinstance(tag_value, int):
            raise TypeError(f"{tag_name} is expected to be of type int")

        self._current_file[tag_name] = tag_value

    def set_tags(self, **kwargs_tags) -> None:
        '''
        Sets the desired collection of tags receives as key word parameters.
        tags supported:
        -----
        album
        albumartist
        artist
        artwork
        comment
        compilation
        composer
        discnumber
        genre
        lyrics
        totaldiscs
        totaltracks
        tracknumber
        tracktitle
        year
        isrc
        -----
        '''
        for key in kwargs_tags:
            self.set_tag(key, kwargs_tags[key])

    def write_tags(self):
        '''
        Writes the actual tags to the file.
        '''
        self._current_file.save()