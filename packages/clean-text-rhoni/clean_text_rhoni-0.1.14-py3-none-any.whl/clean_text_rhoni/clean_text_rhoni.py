"""Main module.

Import the BaseCleanText class with base functions to clean and normalize text,
and build derived functions that combines cleaning processes.
"""
from clean_text_rhoni.base_clean_text import BaseCleanText


def clean_text(text):
    """Perform a complete text cleaning process on the input text.

    This function performs a series of text cleaning operations,
    including:
    1. Removing leading and trailing spaces.
    2. Removing multiple spaces and replacing them with a single space.
    3. Converting the text to lowercase.
    4. Removing accents from vowels.
    5. Removing special characters.
    6. Removing tilde from ñ.

    Parameters
    ----------
    text: str
        The input text to be cleaned.

    Returns
    -------
    text: str
        The cleaned text after applying all cleaning operations.

    Examples
    --------
    >>> clean_text("   Hola Sofía!,   cómo estás?   ")
    "hola sofia como estas"
    """
    clean_text_utils = BaseCleanText()
    text = clean_text_utils.remove_leading_trailing_spaces(text)
    text = clean_text_utils.replace_multiple_spaces(text)
    text = clean_text_utils.transform_to_lowercase(text)
    text = clean_text_utils.remove_accents(text)
    text = clean_text_utils.remove_special_characters(text)
    text = clean_text_utils.remove_n_tilde(text)
    return text


def clean_text_snake_case(text):
    """Perform a complete text cleaning process on the input text and transform it to snake case

    This function performs a series of text cleaning operations,
    including:
    1. Removing leading and trailing space.
    2. Removing multiple spaces and replacing them with a single space.
    3. Converting the text to lowercase.
    4. Removing accents from vowels.
    5. Removing special characters.
    6. Removing tilde from ñ.
    7. Replacing spaces by underscores

    Parameters
    ----------
    text: str
        The input text to be cleaned.

    Returns
    -------
    text: str
        The cleaned text after applying all cleaning operations.

    Examples
    --------
    >>> clean_text("   Hola Sofía!,   cómo estás?   ")
    "hola_sofia_como_estas"
    """
    text = clean_text(text=text)
    clean_text_utils = BaseCleanText()
    text = clean_text_utils.replace_spaces_by_underscores(text)
    return text
