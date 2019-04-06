#!/usr/bin/env python

import argparse
from functools import partial
from pathlib import Path

from requests_futures.sessions import FuturesSession
import pandas as pd
import numpy as np

# see https://stackoverflow.com/a/50039149
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (110000, 110000))

__version__ = '0.3'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def get_html(response, verbose=False):
    try:
        result = response.result()
        if verbose:
            print('Response from {} has status code {}.'.format(result.url, result.status_code))
        assert result.status_code // 100 == 2
        return result.text
    except:
        if verbose:
            print('Error occured for {}'.format(response))
        return None


def get_htmls(urls, max_workers=8, verbose=False, timeout=60):
    session = FuturesSession(max_workers=max_workers)
    if verbose:
        n = len(urls)
        print('Submitting {} jobs...'.format(n))
    responses = [session.get(url, headers=HEADERS, timeout=timeout) for url in urls]
    if verbose:
        print('Executing {} jobs...'.format(n))
    # if verbose, run a for loop to show progress explicitly
    if verbose:
        result = []
        for i, response in enumerate(responses):
            print('{} done, {} to go...'.format(i, n - i))
            result.append(get_html(response, verbose=verbose))
        return result
    else:
        return [get_html(response, verbose=verbose) for response in responses]


def get_htmls_archive(urls, max_workers=8, verbose=False, timeout=60):
    urls = ['https://web.archive.org/web/' + url for url in urls]
    return get_htmls(urls, max_workers=max_workers, verbose=verbose, timeout=timeout)


def main(path, output, verbose, worker, timeout):
    df = pd.read_hdf(path)

    # if output already existed, updates:
    if Path(output).is_file():
        df_old = pd.read_hdf(output)

        # merging dfs
        df_merged = df.merge(df_old[['html']], how='outer', left_index=True, right_index=True)

        df = df_merged

        na_idx = df.html.isna()
        n = np.count_nonzero(na_idx)

        print('{} out of {} urls are new, fetching...'.format(n, df.shape[0]))
        # fetch html
        n_workers = worker if worker else n
        df.loc[na_idx, 'html'] = get_htmls(df[na_idx].index, max_workers=n_workers, verbose=verbose, timeout=timeout)
    else:
        n = df.shape[0]
        print('{} urls to fetch...'.format(n))
        n_workers = worker if worker else n
        df['html'] = get_htmls(df.index, max_workers=n_workers, verbose=verbose, timeout=timeout)

    # no response
    na_idx = df.html.isna()
    n = np.count_nonzero(na_idx)
    print('{} out of {} urls cannot be fetched, try fetching from archive.org...'.format(n, df.shape[0]))
    df.loc[na_idx, 'archive'] = True
    n_workers = worker if worker else n
    df.loc[na_idx, 'html'] = get_htmls_archive(df[na_idx].index, max_workers=n_workers, verbose=verbose, timeout=timeout)

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
    parser.add_argument('-p', '--worker', type=int,
        help='No. of workers used. If not specified, use as many as needed.')
    parser.add_argument('-t', '--timeout', type=float, default=60.,
        help='Timeout specified for requests. Default: 60.')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument('-V', '--verbose', action='store_true',
        help='verbose to stdout.')

    args = parser.parse_args()

    main(args.input, args.output, args.verbose, args.worker, args.timeout)


if __name__ == "__main__":
    cli()
