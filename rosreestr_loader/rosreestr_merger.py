#!/bin/env python3
# -*- coding: utf-8 -*-
"""Script to merge address lists loaded by `rosreestr_loader`."""
import json
import os
import pathlib
from typing import Dict, TextIO

import click

from utils import check_is_list_of_dicts


@click.command()
@click.argument(
    'input_directory',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.argument(
    'output_file',
    type=click.File(mode='wt')
)
def merge_addresses(
    input_directory: str, output_file: TextIO
) -> None:
    """Merge JSON files with addresses by `objectCn` field."""
    input_directory_path = pathlib.Path(input_directory)

    result: Dict[str, Dict[object, object]] = {}
    duplicate_entries = 0

    with (
        click.progressbar(list(os.scandir(input_directory_path)))
    ) as input_directory_entries:
        for input_directory_entry in input_directory_entries:
            if not (
                input_directory_entry.is_file()
                and input_directory_entry.name.startswith('addresses-')
            ):
                continue
            with open(input_directory_entry.path, 'rt') as input_file:
                input_file_data = check_is_list_of_dicts(json.load(input_file))
                for address_data in input_file_data:
                    address_cn = address_data['objectCn']
                    if address_cn in result:
                        duplicate_entries += 1
                    else:
                        result[address_cn] = address_data

    json.dump(result, output_file, ensure_ascii=False)
    click.echo(f'Processed {len(result)} entries,'
               f' found {duplicate_entries} duplicates')


if __name__ == '__main__':
    merge_addresses()
