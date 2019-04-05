#!/usr/bin/env python

import argparse
from pathlib import Path

import requests
import pandas as pd
import numpy as np

from dautil.util import map_parallel

__version__ = '0.1'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def get_html(url):
    try:
        return requests.get(url, headers=HEADERS).text
    except:
        print('Cannot retrieve content from {}'.format(url))
        return None


def main(path, output):
    df = pd.read_hdf(path)

    # if output already existed, updates:
    if Path(output).is_file():
        df_old = pd.read_hdf(output)

        # merging dfs
        df_merged = df.merge(df_old[['html']], how='outer', left_index=True, right_index=True)

        na_idx = df_merged.html.isna()

        # fetch html
        df_merged.loc[na_idx, 'html'] = map_parallel(get_html, df_merged[na_idx].index, mode='multithreading', processes=1000)

        df = df_merged
    else:
        df['html'] = df.index.map(get_html)
        df['html'] = map_parallel(get_html, df.index, mode='multithreading', processes=1000)

    df.to_hdf(
        output,
        'df',
        format='table',
        complevel=9,
        fletcher32=True
    )


def cli():
    parser = argparse.ArgumentParser(description="Save url content in HDF5.")

    parser.add_argument('input', help='Input urls in HDF5.')
    parser.add_argument('-o', '--output', help='Output HDF5. Update file if exists.')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()

    main(args.input, args.output)


if __name__ == "__main__":
    cli()
