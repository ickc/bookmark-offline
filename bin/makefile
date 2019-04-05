SHELL := /bin/bash

# Note: bookmark.hdf5 should be kept as a cache

all: bookmark.docx

clean:
	rm -f ril_export.hdf5 bookmark.html
Clean: clean
	rm -f bookmark.docx

ril_export.hdf5: ril_export.html
	pocket_parse.py -o $@ $<

bookmark.hdf5: ril_export.hdf5
	get_html.py -o $@ $<

%.html: %.hdf5
	parse_html.py -o $@ $<

%.docx: %.html
	pandoc -o $@ $< -M title='My Bookmarks'
