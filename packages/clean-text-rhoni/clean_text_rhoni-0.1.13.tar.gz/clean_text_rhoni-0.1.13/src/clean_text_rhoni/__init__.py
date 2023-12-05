# read version from installed package
from importlib.metadata import version
__version__ = version("clean_text_rhoni")

# populate package namespace
from clean_text_rhoni.base_clean_text import BaseCleanText
from clean_text_rhoni.clean_text_rhoni import clean_text, clean_text_snake_case
