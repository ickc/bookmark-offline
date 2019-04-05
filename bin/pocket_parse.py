#!/usr/bin/env python

import argparse
import pandas as pd
from bs4 import BeautifulSoup

__version__ = '0.1'


def main(input, output):

    with open(input, 'r') as f:
        soup = BeautifulSoup(f.read())

    results = soup.find_all('a')
    del soup

    df = pd.DataFrame((result.attrs for result in results))

    df.to_hdf(
        output,
        'df',
        format='table',
        complevel=9,
        fletcher32=True
    )


def cli():
    parser = argparse.ArgumentParser(description="Convert Pocket export HTML format to DataFrame.")

    parser.add_argument('input', help='Input ril_export.html from Pocket.')
    parser.add_argument('-o', '--output', help='Output HDF5.')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()

    main(args.input, args.output)


if __name__ == "__main__":
    cli()
