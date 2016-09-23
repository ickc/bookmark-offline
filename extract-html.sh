#!/bin/bash

# get paths and extension
PATHNAME="$@"
PATHNAMEWOEXT=${PATHNAME%.*}
EXT=${PATHNAME##*.}
DIRECTORY=${PATHNAME%/*}
# ext="${EXT,,}" #This does not work on Mac's default, old version of, bash.


grep -i href "$PATHNAME" | sed 's/^.*href="\([^"]*\)".*$/\1/' > "$PATHNAMEWOEXT.txt"
