#!/usr/bin/env python

import argparse
from pathlib import Path

import grequests
import pandas as pd
import numpy as np

__version__ = '0.2'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def get_htmls(urls):
    return [None if response is None else response.text for response in grequests.map(grequests.get(url, headers=HEADERS) for url in urls)]


def get_htmls_archive(urls):
    return [None if response is None else response.text for response in grequests.map(grequests.get('https://web.archive.org/web/' + url, headers=HEADERS) for url in urls)]


def main(path, output):
    df = pd.read_hdf(path)

    # if output already existed, updates:
    if Path(output).is_file():
        df_old = pd.read_hdf(output)

        # merging dfs
        df_merged = df.merge(df_old[['html']], how='outer', left_index=True, right_index=True)

        df = df_merged

        na_idx = df.html.isna()

        print('{} out of {} urls are new, fetching...'.format(np.count_nonzero(na_idx), df.shape[0]))
        # fetch html
        df.loc[na_idx, 'html'] = get_htmls(df[na_idx].index)
    else:
        print('{} urls to fetch...'.format(df.shape[0]))
        df['html'] = get_htmls(df.index)

    # no response
    na_idx = df.html.isna()
    print('{} out of {} urls cannot be fetched, try fetching from archive.org...'.format(np.count_nonzero(na_idx), df.shape[0]))
    df.loc[na_idx, 'archive'] = True
    df.loc[na_idx, 'html'] = get_htmls_archive(df[na_idx].index)

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
