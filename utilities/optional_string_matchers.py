from re import search


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
        return search(pattern, file_name).group(0)

    def extract_track_title_title_capitalize(self, file_name: str,
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

        return " ".join(list_words)

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

        string = string.lower()
        for i in range(len(string)):
            if string[i].isalpha():
                return string.replace(string[i], string[i].upper(), 1)
        return string
