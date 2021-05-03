#! /usr/bin/env python

import argparse
import csv
import sys


def main(args):
    """
    Filter CSV file aainst a plain text file of allowed values for a column.
    """
    outfile = args.outfile
    match_set = set([])
    for line in args.filter_file:
        match_set.add(line.strip())
    with open(args.csv, "r") as f:
        input_data = csv.reader(f)
        output = csv.writer(outfile)
        header = next(input_data)
        col_pos = None
        for n, value in enumerate(header):
            if value == args.column:
                col_pos = n
                break
        assert col_pos is not None, "No matching column, `{}` found.".format(
            args.column
        )
        output.writerow(header)
        for row in input_data:
            if accept_row(row, match_set, col_pos):
                output.writerow(row)


def accept_row(row, match_set, col_pos):
    """
    Should the row be accepted?
    """
    value = row[col_pos]
    return value in match_set


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Filter CSV files.")
    parser.add_argument("csv", action="store", help="The CSV file to filter.")
    parser.add_argument(
        "filter_file",
        action="store",
        type=argparse.FileType("r"),
        help="A file containing values to match, one per line.",
    )
    parser.add_argument(
        "column", action="store", help="The column name to match values against."
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="The output CSV file.",
    )
    args = parser.parse_args()
    main(args)
