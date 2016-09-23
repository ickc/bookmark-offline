#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
	marky.rb -o offline "$line"
done < "$1"