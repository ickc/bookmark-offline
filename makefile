SHELL := /bin/bash

# data
## probably ril_export.html
pocketExport := $(wildcard data/*.html)
## probably ril_export.csv
CSV := $(patsubst %.html,%.csv,$(pocketExport))
## probably ril_export.txt
urlList := $(patsubst %.html,%.txt,$(pocketExport))
## offline.txt
pathToOffline := data/offline
urlDownloaded := $(pathToOffline).txt
### downloaded MD by Marky
MD := $(wildcard $(pathToOffline)/*.md)
## online.txt
pathToOnline := data/online
urlToBeDownload := $(pathToOnline).txt
# Convert all URL in URI
TXT := $(wildcard data/*.txt)
URI := $(patsubst %.txt,%.uri,$(TXT))

# prepare pocketExport, marky.rb
init: download update marky.rb
# generate from pocketExport
data: $(CSV) $(urlList) $(urlDownloaded) $(urlToBeDownload)
uri: $(URI)

# Initial Preparation #################################################

# download Pocket's export
download:
	python -mwebbrowser https://getpocket.com/export

# update submodule
update:
	git submodule update --recursive --remote

# prepare marky.rb from submodule
marky.rb: submodule/marky.rb
	rsync $< $@
	chmod +x $@

# Scripting ###########################################################

# Instapaper
instapaper: data/instapaper-export-sort.csv data/ril_export-instapaper.csv
## from Instapaper
data/instapaper-export-sort.csv: data/instapaper-export.csv
	printf "%s\n" "URL,Title,Selection,Folder" > temp
	tail -n +2 $< | sort >> temp
	mv temp $@
## from Pocket
%-instapaper.csv: %.html
	printf "%s\n" "URL,Title,Selection,Folder" > $@
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*tags="\([^"]*\)".*$$/"\1"/' > data/URL.list
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*tags="\([^"]*\)".*$$/"\2"/' > data/Tags.list
	sed -i 's/,/:/g' data/Tags.list
	paste data/URL.list data/Tags.list | sed 's/	/,,,/g' >> $@
	rm data/URL.list data/Tags.list

# convert Pocket's export to a database
## $(CSV): 1st column: URL: 2nd column: Tags
%.csv: %.html
	printf "%s\n" "URL,Tags" > $@
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*tags="\([^"]*\)".*$$/"\1","\2"/' | sort >> $@
## $(urlList): a list of URLs only
%.txt: %.html
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*$$/\1/' | sort > $@

# $(MD): use marky to download all links as markdown files
offline: $(urlToBeDownload) marky.rb
	mkdir -p $(pathToOffline)
	< $< xargs -i -n1 -P128 ./marky.rb -o $(pathToOffline) {}

# obtain a list of downloaded URLs
$(urlDownloaded):
	find $(pathToOffline) -iname '*.md' | xargs -i -n1 -P8 bash -c 'head -n 1 "$$0" | grep -oP "\[Source\]\(\K([^ ]*)"' {} | sort > $@

$(urlToBeDownload): $(urlList) $(urlDownloaded)
	comm -23 $^ > $@

%.uri: %.txt
	: > $@
	while IFS='' read -r line || [[ -n "$$line" ]];\
	do\
		echo "$$line" | perl -MURI::file -e 'print URI::file->new(<STDIN>)."\n"' | sed 's/^\.\///' >> $@ &\
	done < $<
