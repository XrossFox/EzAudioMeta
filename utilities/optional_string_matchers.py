from re import search
from re import sub


class OptionalStringMatchers:

    _articles = ["a", "an", "the"]
    _coord_conjuncts = ["for", "and", "nor", "but", "or", "yet", "so"]
    _prepositions = [
                        "amid",
                        "anti",
                        "as",
                        "at",
                        "but",
                        "by",
                        "down",
                        "for",
                        "from",
                        "in",
                        "into",
                        "like",
                        "near",
                        "of",
                        "off",
                        "on",
                        "onto",
                        "over",
                        "past",
                        "per",
                        "plus",
                        "save",
                        "than",
                        "to",
                        "up",
                        "upon",
                        "via",
                        "with",
    ]

    def extract_track_title_as_is(self, file_name: str, pattern: str) -> str:
        '''
        Receives the name of the track and returns the substring that
        matches the regex expression as is, no further processing is done.
        '''
        title = search(pattern, file_name).group(0)
        title = title.strip()
        return title

    def extract_track_title_capitalize(self, file_name: str,
                                       pattern: str) -> str:
        '''
        Receives the name og the track and returns the substring that
        matches the regex expression and the it is capitalized following the
        Title Capitalization rules. Words not capitalized are: articles,
        coordinate junctions and proposotions that are less than 5 letters
        long.
        '''
        track_title = search(pattern, file_name).group(0)
        list_words = track_title.split(" ")

        # if first or last: capitalize, if in lists: to lower, else: capitalize
        for i in range(len(list_words)):

            if i == 0:
                list_words[i] = self._capitalize_first(list_words[i])
                continue

            elif i == (len(list_words) - 1):
                list_words[i] = self._capitalize_first(list_words[i])
                continue

            elif (list_words[i].lower() in self._articles or
                  list_words[i].lower() in self._coord_conjuncts or
                  list_words[i].lower() in self._prepositions):
                list_words[i] = list_words[i].lower()
                continue

            list_words[i] = self._capitalize_first(list_words[i])

        title = " ".join(list_words)
        title = title.strip()
        return title

    def _capitalize_first(self, string: str) -> str:
        '''
        Receives a string. Transforms all letters to lower, then
        converts the first letter found to upper case. If no letter is found,
        the string is returned as is. If a "-" is present, the string is split,
        and each word capitalized and then re-joined.
        '''
        if "-" in string:
            sub_strings = string.split("-")
            capitalized = [self._capitalize_first(i) for i in sub_strings]
            return "-".join(capitalized)

        if "_" in string:
            sub_strings = string.split("_")
            capitalized = [self._capitalize_first(i) for i in sub_strings]
            return "_".join(capitalized)

        string = string.lower()
        for i in range(len(string)):
            if string[i].isalpha():
                return string.replace(string[i], string[i].upper(), 1)
        return string

    def extract_track_title_cleanup_and_capitalize(self, file_name: str,
                                                   pattern: str) -> str:
        '''
        Receives a string, replaces all '-' and '_', trailing or duplicate
        white spaces for single white spaces, and trims leading and trainling
        spaces. Then applies regular title capitalization.
        '''
        pattern_remover = "(_+|-+| {2,})"
        clean_string = sub(pattern_remover, " ", file_name)
        clean_string = self.extract_track_title_capitalize(clean_string,
                                                           pattern)
        clean_string = clean_string.strip()
        return clean_string

    def extract_track_number(self, file_name: str, pattern: str) -> int:
        '''
        Receives the name of the file, looks for a number that matches
        the given pattern, extracts the str and parses it into an int.
        If no valid match is found, returns 0.
        -----
        Raises a TypeError if tha matching object cannot be parsed to int.\n
        Raises an Exception if something else happens.
        '''
        track_number = 0

        match = search(pattern, file_name)
        if match:
            try:

                track_number = int(match.group(0))

            except TypeError as e:
                msg = "Encountered an exception when trying to convert the" +\
                      " track number to a number: "
                raise TypeError(msg) from e
            except Exception as e:
                msg = "Something went wrong when extracting track number:"
                raise Exception(msg) from e

        return track_number
