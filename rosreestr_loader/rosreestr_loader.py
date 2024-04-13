#!/bin/env python3
# -*- coding: utf-8 -*-
"""Script to load addresses data from rosreestr.ru API."""
import copy
import json
import pathlib
from typing import Dict, Iterator, List, Tuple

import click
import requests

from utils import check_is_list_of_dicts

API_URL_BASE = 'https://rosreestr.ru/api/online/fir_objects'
API_URL_ADDRESS_WILDCARD = API_URL_BASE + '/{id_str}*'
API_LIMIT = 200


def get_id_str(cadastre_id: List[int]) -> str:
    """Get cadastre ID string from digit list."""
    result: str = ''
    for i in range(len(cadastre_id)):
        if i in [2, 4, 11]:
            result += ':'
        result += str(cadastre_id[i])
    return result


def try_request(id_start: List[int]) -> List[Dict[object, object]]:
    """Perform request to API."""
    id_str: str = get_id_str(id_start)
    request_url: str = API_URL_ADDRESS_WILDCARD.format(id_str=id_str)
    click.echo(f'Loading {request_url}')
    r = requests.get(request_url)
    if r.status_code == 204:
        return []
    return check_is_list_of_dicts(r.json())


def load_subaddresses(
    id_start: List[int], limit: int,
    min_id_start_length: int
) -> Iterator[Tuple[List[int], List[Dict[object, object]]]]:
    """
    Load addresses with cadastre IDs starting from `id_start`.

    If API request returns count of elements equal to or more than `limit`,
    more narrow requests will be performed, for example:

    ```
    # limit is 200
    # request to 50:12*    returned 200 elements # use more narrow requests
    # request to 50:12:0*  returned 200 elements # use more narrow requests
    # request to 50:12:00* returned  15 elements
    # request to 50:12:01* returned  15 elements
    # request to 50:12:02* returned  17 elements
    # request to 50:12:03* returned  56 elements
    # request to 50:12:04* returned  15 elements
    # request to 50:12:05* returned  49 elements
    # request to 50:12:06* returned  37 elements
    # request to 50:12:07* returned  98 elements
    # request to 50:12:08* returned 154 elements
    # request to 50:12:09* returned 193 elements
    # request to 50:12:1*  returned 172 elements
    # request to 50:12:2*  returned  51  elements
    # ...
    ```
    """
    current_id_start: List[int] = copy.copy(id_start)

    while True:
        result: List[Dict[str, object]] = try_request(current_id_start)

        if len(result) < limit:
            if len(result) > 0:
                yield current_id_start, result
            current_id_start[-1] += 1
            while current_id_start[-1] == 10:
                current_id_start.pop(-1)
                if len(current_id_start) <= min_id_start_length:
                    return
                current_id_start[-1] += 1
        else:
            current_id_start.append(0)


@click.command()
@click.argument('start_id', type=click.STRING)
@click.argument(
    'output_directory',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def load_addresses(
    start_id: str, output_directory: str,
) -> None:
    """Load addresses with cadastre IDs beginning from given number."""
    start_id_data = list(map(int, start_id))
    for digit in start_id_data:
        if (digit < 0) or (digit > 9):
            raise ValueError('start_id')

    output_directory_path = pathlib.Path(output_directory)
    for current_id_start, addresses in load_subaddresses(
        start_id_data, API_LIMIT, 4
    ):
        output_file_path: pathlib.Path =\
            output_directory_path.joinpath(
                'addresses-{}.json'.format(
                    ''.join(list(map(str, current_id_start)))
                )
            )
        with open(output_file_path, 'wt') as output_file:
            json.dump(addresses, output_file, ensure_ascii=False)


if __name__ == '__main__':
    load_addresses()
