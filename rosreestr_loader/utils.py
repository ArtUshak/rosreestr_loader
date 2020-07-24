"""Utilitary functions for scripts."""
from typing import Any, Dict, List


def check_is_list_of_dicts(x: Any) -> List[Dict[Any, Any]]:
    """Return `x` if it is `List[Dict[Any, Any]]`, raise `ValueError`."""
    if not isinstance(x, list):
        raise ValueError()
    for element in x:
        if not isinstance(element, dict):
            raise ValueError()
    return x
