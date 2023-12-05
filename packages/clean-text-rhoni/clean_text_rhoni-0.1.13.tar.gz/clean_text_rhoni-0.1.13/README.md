# clean_text_rhoni

The `clean_text_rhoni` package provides tools to efficiently clean and transform text data. It offers a set of methods and functions for removing special characters, accents, and unnecessary spaces from text, as well as converting text to lowercase and snake case style.
This package is useful for preparing text data for natural language processing tasks, data analysis, and other applications where clean and normalized text is nedeed.

## Installation

```bash
$ pip install clean_text_rhoni
```

## Usage

This package has 2 main functions to clean a text:

`clean_text` function performs a complete text cleaning process on the input text. The cleaning operations include removing leading and trailing spaces, replacing multiple spaces with a single space, converting text to lowercase, removing accents, removing special characters, and removing the tilde from 'ñ'.

`clean_text_snake_case` function performs the same comprehensive text cleaning process as `clean_text`, and additionally transforms the cleaned text into snake case style by replacing spaces with underscores. This is useful for creating consistent and readable variable or column names.


```bash
from clean_text_rhoni import clean_text, clean_text_snake_case

sample_text = "%ábdc    efghí   %$ñ"

# clean_text()
# run a complete cleaning over a text

cleaned_text = clean_text(sample_text)
print(cleaned_text) # 'abdc efghi n'

# clean_text_snake_case()
# run a complete cleaning over a text and return the result in snake_case style

snake_case_cleaned_text = clean_text_snake_case(sample_text)
print(snake_case_cleaned_text) # abdc_efghi_n

```

You can also access the `BaseCleanText` class and use its methods separately:

```bash
from clean_text_rhoni import BaseCleanText

# create a class instance
instance_base_clean_text = BaseCleanText()

# call the chosen method
instance_base_clean_text.remove_accents("áéíóú") #'aeiou'

instance_base_clean_text.replace_underscores_by_spaces("hello_world") #'hello world'

```

The `BaseCleanText` class has the following methods:

* `transform_to_lowercase(text)`: Converts the input text to lowercase.

* `remove_leading_trailing_spaces(text)`: Removes leading and trailing white spaces from the input text.

* `replace_multiple_spaces(text)`: Removes multiple spaces in the input text and replaces them with a single space.

* `remove_special_characters(text)`: Removes special characters from the input text. Special characters are defined as characters that are neither alphanumeric nor whitespace characters. A regular expression is used to match and remove these characters.

*  `remove_accents(text)`: Removes accents from vowels in the input text. It replaces accented vowel characters (e.g., á, é, í) with their non-accented counterparts (e.g., a, e, i).

* `remove_n_tilde(text):` Removes the tilde from the character 'ñ' in the input text, replacing it with a regular 'n'.

* `replace_spaces_by_underscores(text)`: Replaces spaces with underscores in the input text.

*  `replace_underscores_by_spaces(text)`: Replaces underscores with spaces in the input text.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`clean_text_rhoni` was created by rhoni. It is licensed under the terms of the MIT license.

## Credits

`clean_text_rhoni` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
