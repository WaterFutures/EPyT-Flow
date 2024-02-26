# Developers' Guide

## Design Paradigma

Objects should be immutable whenever possible -- this allows us to avoid unintended side effects. Never trust user's input -- check all passed arguments carefully.

Code must work with all current Python versions from 3.9 to 3.12. Also, code must work on all major platforms: Windows, Linux, and Mac OSX.

## Code Style Guide

- Please follow the suggestions made by [Pylint](https://github.com/pylint-dev/pylint) and [Flake8](https://github.com/pycqa/flake8/) -- violations require good justification!

- Docstrings must be written in Numpy-docstring style.

- Naming convention for variables and methods is to use ```lower_case_with_underscores``` and ```CapitalizedWords``` for class names.

- Use typehints.

## Tests

- Tests are implemented using [pytest](https://pytest.org
) and stored in [tests/](tests/).

- Any implemented feature must come with corresponding tests.

- [Nox](https://nox.thea.codes/en/stable/) is used to test different Python versions -- see [noxfile.py](noxfile.py).