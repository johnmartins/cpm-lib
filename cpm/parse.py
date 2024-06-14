from cpm.exceptions import *
from cpm.models import DSM


def parse_csv(filepath, delimiter='auto', encoding='utf8'):

    if delimiter == 'auto':
        with open(filepath, 'r') as file:
            delimiter = detect_delimiter(file.read())

    # Identify number of rows, and separate header row
    num_cols = 0
    column_names = []
    with open(filepath, 'r') as file:
        for line in file:
            column_names.append(line.split(delimiter)[0])
            num_cols += 1

    # We do not want the first column in the header
    column_names.pop(0)

    data = []

    with open(filepath, 'r') as file:
        for i, line in enumerate(file):
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
                        data[i - 1].append(None)

    dsm = DSM(matrix=data, columns=column_names)

    return dsm


def detect_delimiter(text, look_ahead=1000):
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

