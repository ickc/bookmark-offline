SHELL := /bin/bash

# data
## sources
sourceHTML := $(wildcard data/*.html)
sourceCSV := $(wildcard data/*.csv)
targetCSV := $(patsubst %.html,%.csv,$(sourceHTML))
LIST := $(patsubst %.html,%.list,$(sourceHTML)) $(patsubst %.csv,%.list,$(sourceCSV))

# generate from pocketExport
data: $(targetCSV) $(LIST)
clean:
	rm -f $(targetCSV) $(LIST)

# Initial Preparation #################################################

# download from Pocket/Instapaper
download:
	python -mwebbrowser https://getpocket.com/export
	python -mwebbrowser https://www.instapaper.com/user

# Scripting ###########################################################

# $(targetCSV)
%.csv: %.html
	printf "%s\n" "URL,Title,Tags" > $@
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*tags="\([^"]*\)">\([^<]*\).*$$/"\1"/' > data/URL.list
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*tags="\([^"]*\)">\([^<]*\).*$$/"\2"/' > data/Tags.list
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*tags="\([^"]*\)">\([^<]*\).*$$/\3/' > data/Title.list
	sed -i -e 's/"/'\''/g' -e 's/^\(.*\)$$/"\1"/g' data/Title.list
	paste data/URL.list data/Title.list data/Tags.list | sed 's/	/,/g' | sort >> $@
	rm data/URL.list data/Title.list data/Tags.list
# $(LIST)
%.list: %.csv
	tail -n +2 $< | sed -e 's/^"\([^"]*\)".*$$/\1/g' -e 's/^h\([^,]*\),.*$$/h\1/g' -e 's/^https/http/g' | sort > $@
