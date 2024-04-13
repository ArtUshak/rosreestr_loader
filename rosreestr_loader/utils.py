"""Utilitary functions for scripts."""
from typing import Dict, List


def check_is_list_of_dicts(x: object) -> List[Dict[object, object]]:
    """Return `x` if it is `List[Dict[object, object]]`, raise `ValueError`."""
    if not isinstance(x, list):
        raise ValueError()
    for element in x:
        if not isinstance(element, dict):
            raise ValueError()
    return x
