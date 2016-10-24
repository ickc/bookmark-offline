SHELL := /bin/bash

pocketExport := $(wildcard data/*.html)
database := $(patsubst %.html,%.txt,$(pocketExport))

data: $(database)

# update submodule
update:
	git submodule update --recursive --remote

%.txt: %.html
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*$$/\1/' > $@
