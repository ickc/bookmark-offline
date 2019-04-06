#!/usr/bin/env python

import argparse
import os
from json import JSONDecodeError

import pandas as pd
from readability import Document
import panflute as pf
import pypandoc

from dautil.util import map_parallel

__version__ = '0.1'

def increase_header_level(elem, doc):
    if type(elem) == pf.Header:
        elem.level += 1


def Image_to_Link(elem, doc):
    if type(elem) == pf.Image:
        text = elem.content
        url = elem.url
        return pf.Link(*text, url=url)


def html_filter(url, text):
    try:
        # readability
        doc = Document(text)
        title = doc.short_title()
        html_sum = doc.summary(html_partial=True)
        # pandoc
        try:
            try:
                doc = pf.convert_text(html_sum, input_format='html-native_divs-native_spans', standalone=True)
            # strange error, pandoc and pypandoc can take this without problem.
            except OSError as e:
                print('Error {} from panflute encountered when processing {}, fallback to pypandoc.'.format(e, url))
                doc = pf.convert_text(pypandoc.convert_text(html_sum, 'json', 'html-native_divs-native_spans'), input_format='json', standalone=True)
            except JSONDecodeError as e:
                print('Error {} from panflute encountered when processing {}, fallback to pypandoc.'.format(e, url))
                doc = pf.convert_text(pypandoc.convert_text(html_sum, 'html', 'html-native_divs-native_spans'), input_format='html-native_divs-native_spans', standalone=True)

            doc = pf.run_filters((increase_header_level, Image_to_Link), doc=doc)

            temp = pf.convert_text('''# {}\n\n[Source]({})'''.format(title, url))

            for item in temp[::-1]:
                doc.content.insert(0, item)

            return pf.convert_text(doc, input_format='panflute', output_format='html')
        except:
            print('Cannot handle error from panflute, stop using pandoc filter on {}.'.format(url))
            return '<h1>{}</h1><p><a href="{}">Source</a></p>{}'.format(title, url, html_sum)
    except Exception as e:
        print('Cannot handle error {}. Skip processing {}.'.format(e, url))
        return ''


def main(path, output):
    df = pd.read_hdf(path)

    non_na_idx = ~df.html.isna()

    results = map_parallel(html_filter, df[non_na_idx].index, df.loc[non_na_idx, 'html'], mode='multiprocessing', processes=20)

    with open(output, 'w') as f:
        f.writelines(results)


def cli():
    parser = argparse.ArgumentParser(description="Parse and cleanup HTML from HDF5.")

    parser.add_argument('input', help='Input HDF5 containing a column of html and index of url.')
    parser.add_argument('-o', '--output', help='Output HTML.')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()

    main(args.input, args.output)


if __name__ == "__main__":
    cli()
