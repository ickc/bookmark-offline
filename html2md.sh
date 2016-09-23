#!/bin/bash

# get paths and extension
PATHNAME="$@"
PATHNAMEWOEXT=${PATHNAME%.*}
EXT=${PATHNAME##*.}
DIRECTORY=${PATHNAME%/*}
# ext="${EXT,,}" #This does not work on Mac's default, old version of, bash.

while IFS='' read -r line || [[ -n "$line" ]]; do
	marky.rb -o offline "$line"
done < "$1"