from typing import Dict

import stringcase
from pluralizer import Pluralizer


def pluralize(word):
    return Pluralizer().plural(word)


def camelize(data: str | Dict[str, str]) -> str | Dict[str, str]:
    if isinstance(data, str):
        return stringcase.camelcase(data)
    elif isinstance(data, dict):
        return {stringcase.camelcase(key): value for key, value in data.items()}
    else:
        raise ValueError("Input data should be a string or dictionary")


def snakefy(data: str | Dict[str, str]) -> str | Dict[str, str]:
    if isinstance(data, str):
        return stringcase.snakecase(data)
    elif isinstance(data, dict):
        return {stringcase.snakecase(key): value for key, value in data.items()}
    else:
        raise ValueError("Input data should be a string or dictionary")
