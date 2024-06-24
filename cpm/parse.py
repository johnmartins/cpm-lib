from typing import TextIO, Union
from cpm.exceptions import *
from cpm.models import DSM
from os import listdir
import re


def parse_csv_dir(dir_path: str, pattern: str =  None,  delimiter: str = 'auto',
                  encoding: str = 'utf-8', instigator: str = 'column') -> list[DSM]:
    """
    Parse a directory of CSVs. A pattern for what the filename needs to include can be used
    as an inclusivity-filter.
    :param path:
    :param pattern:
    :param delimiter:
    :param encoding:
    :param instigator:
    :return:
    """
    dsm_array = []
    p = None
    if pattern is not None:
        p = re.compile(pattern, re.DOTALL)

    for filename in listdir(dir_path):
        if p and p.match(filename) is None:
            continue
        filepath = dir_path + '/' + filename
        print(filepath)
        dsm_array.append(parse_csv(filepath))

    return dsm_array


def parse_csv(file: Union[str, TextIO], delimiter: str = 'auto', encoding: str = 'utf-8', instigator: str = 'column'):
    """
    Parse CSV to DSM
    :param file: Targeted CSV file or file-like object
    :param delimiter: CSV delimiter. Defaults to auto-detection.
    :param encoding: text-encoding. Defaults to utf-8
    :param instigator: Determines directionality of DSM. Defaults to columns instigating rows.
    :return: DSM
    """
    
    content = _read_file(file, encoding)
    
    if delimiter == 'auto':
        delimiter = detect_delimiter(content)

    # Identify number of rows, and separate header row
    num_cols = 0
    column_names = []
    lines = _get_file_lines(file, encoding)
    for line in lines:
        column_names.append(line.split(delimiter)[0])
        num_cols += 1

    # We do not want the first column in the header
    column_names.pop(0)

    data = []

    for i, line in enumerate(lines):
        if i == 0:
            continue
        data.append([])
        for j, col in enumerate(line.split(delimiter)):
            if j == 0:
                continue
            if col == "":
                data[i-1].append(None)
            else:
                try:
                    data[i-1].append(float(col))
                except ValueError:
                    data[i-1].append(None)

    dsm = DSM(matrix=data, columns=column_names, instigator=instigator)

    return dsm


def _read_file(file, encoding):
    if isinstance(file, str):
        with open(file, 'r', encoding=encoding) as f:
            return f.read()
    elif hasattr(file, 'read'):
        position = file.tell()
        content = file.read()
        file.seek(position)
        return content
    else:
        raise ValueError("Invalid file input. Must be a filepath or a file-like object.")


def _get_file_lines(file, encoding):
    if isinstance(file, str):
        with open(file, 'r', encoding=encoding) as f:
            return f.readlines()
    elif hasattr(file, 'read'):
        position = file.tell()
        file.seek(0)
        lines = file.readlines()
        file.seek(position)
        return lines
    else:
        raise ValueError("Invalid file input. Must be a filepath or a file-like object.")


def detect_delimiter(text, look_ahead=1000):
    """
    Attempts to determine CSV delmiter based on a certain amount of sample characters
    :param text: text from CSV file
    :param look_ahead: number of samples from CSV-file used to guess the delimiter
    :return:
    """
    symbol_map = dict({
        ",": 0,
        ";": 0,
        "\t": 0,
    })

    keys = symbol_map.keys()
    key_set = set(keys)

    for index, sign in enumerate(text):
        if sign in key_set:
            symbol_map[sign] += 1

        # Don't waste time going through the entire file if it is large
        if look_ahead <= index:
            break

    best_matches = 0
    best_delimiter = None
    for key in key_set:
        if symbol_map[key] > best_matches:
            best_delimiter = key
            best_matches = symbol_map[key]

    if best_delimiter is None:
        raise AutoDelimiterError('None of the default delimiters matched the file. Is the file empty?')

    return best_delimiter
