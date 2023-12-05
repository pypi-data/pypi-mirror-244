"""Module with base class clean text
"""
import re


class BaseCleanText:
    """A utility class to clean and manipulate text
    """

    def transform_to_lowercase(self, text):
        """Convert the input text to lowercase.

        Examples
        --------
        >>> transform_to_lowercase("Hello World")
        "hello world"
        """
        return text.lower()

    def remove_leading_trailing_spaces(self, text):
        """Remove leading and trailing whitespaces from the input text.

        Examples
        --------
        >>> remove_leading_trailing_spaces("  hello world  ")
        "hello world"
        """
        return text.strip()

    def replace_multiple_spaces(self, text):
        """Remove multiple spaces in the input text and replace them with a single space.

        Examples
        --------
        >>> replace_multiple_spaces("hello   world")
        "hello world"
        """
        return re.sub(' +', ' ', text)

    def remove_special_characters(self, text):
        """Remove special characters from the input text.

        Examples
        --------
        >>> remove_special_characters("Hola! cómo estás?")
        "Hola cómo estás"

        Notes
        -----
        Special characters are characters that are neither word characters (alphanumeric and underscore)
        nor whitespace characters.
        """
        return re.sub(r'[^\w\s]', '', text)

    def remove_accents(self, text):
        """Remove accents from vowels in the input text.

        Examples
        --------
        >>> remove_accents("café")
        "cafe"
        """
        return re.sub(r'([á-úÁ-Ú])', self.__check_vowel, text)

    def __check_vowel(self, text):
        """Checks if there is any vowel with accents
        """
        accent_map = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
        }
        char = text.group()
        return accent_map.get(char, char)

    def remove_n_tilde(self, text):
        """Remove the tilde from the n in the input text.

        Examples
        --------
        >>> remove_n_tilde("mañana")
        "manana"
        """
        return re.sub(r'ñ', 'n', text)

    def replace_spaces_by_underscores(self, text):
        """
        Replace spaces with underscores in the input text.

        Examples
        --------
        >>> replace_spaces_by_underscores("hello world")
        "hello_world"
        """
        return re.sub(r'\s', '_', text)

    def replace_underscores_by_spaces(self, text):
        """Replace underscores with spaces in the input text.

        Examples
        --------
        >>> replace_underscores_by_spaces("hello_world")
        "hello world"
        """
        return re.sub('_', ' ', text)
