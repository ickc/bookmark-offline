SHELL := /bin/bash

# data
## sources
sourceHTML := $(wildcard data/*.html)
sourceCSV := $(wildcard data/*.csv)
# Pocket's source in HTML converted to CSV
targetCSV := $(patsubst %.html,%.csv,$(sourceHTML))
# a list of URLs from CSV
LIST := $(patsubst %.html,%.list,$(sourceHTML)) $(patsubst %.csv,%.list,$(sourceCSV))
# curl the URL and see where it is redirected to
REDIRECT := $(patsubst %.list,%.redirect,$(LIST))
# ignore the HTTPS in the redirected results for sorting
HTTPREDIRECT := $(patsubst %.list,%.httpredirect,$(LIST))
# list the domain only
DOMAIN := $(patsubst %.list,%.domain,$(LIST))

# generate from pocketExport
data: $(targetCSV) $(LIST) $(REDIRECT) $(HTTPREDIRECT) $(DOMAIN)
clean:
	rm -f $(targetCSV) $(LIST) $(REDIRECT) $(HTTPREDIRECT) $(DOMAIN)

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
# $(REDIRECT)
%.redirect: %.list
	: > $@
	< $< xargs -i -n1 -P128 sh -c 'curl -w "%{url_effective}\n" -I -L -s -S $$0 -o /dev/null >> $@' {} || true
	< $@ sort | uniq > $*.temp
	mv $*.temp $@
# $(HTTPREDIRECT)
%.httpredirect: %.redirect
	sed 's/^https/http/g' $< | sort | uniq > $@
# $(DOMAIN)
%.domain: %.redirect
	sed 's/^[^/]*:\/\/\([^/]\+\).*$$/\1/g' $< | sort | uniq > $@
