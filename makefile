SHELL := /bin/bash

pocketExport := $(wildcard data/*.html)
CSV := $(patsubst %.html,%.csv,$(pocketExport))
database := $(patsubst %.html,%.txt,$(pocketExport))

data: $(database) $(CSV)
init: download marky.rb update

# Initial Preparation #################################################

# update submodule
update:
	git submodule update --recursive --remote

# download Pocket's export
download:
	python -mwebbrowser https://getpocket.com/export

# prepare marky.rb from submodule
marky.rb: submodule/marky.rb
	rsync $< $@
	chmod +x $@

# Scripting ###########################################################

# convert Pocket's export to a database
%.csv: %.html
	printf "%s\n" "URL,Tags" > $@
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*tags="\([^"]*\)".*$$/"\1","\2"/' | sort >> $@
%.txt: %.html
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*$$/\1/' | sort > $@

# use marky to download all links as a markdown file
offline: $(database) marky.rb
	mkdir -p offline
	while IFS='' read -r line || [[ -n "$$line" ]];\
	do\
		./marky.rb -o offline "$$line";\
	done < $<
