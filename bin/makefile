SHELL := /bin/bash

# Note: html.hdf5 should be kept as a cache

all: html.docx

clean:
	rm -f ril_export.hdf5 html.html
Clean: clean
	rm -f html.docx

ril_export.hdf5: ril_export.html
	pocket_parse.py -o $@ $<

html.hdf5: ril_export.hdf5
	get_html.py -o $@ $<

%.html: %.hdf5
	parse_html.py -o $@ $<

%.docx: %.html
	pandoc -o $@ $< -M title='My Bookmarks'
