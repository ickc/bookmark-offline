SHELL := /bin/bash

pocketExport := $(wildcard data/*.html)
database := $(patsubst %.html,%.txt,$(pocketExport))

data: $(database)
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
%.txt: %.html
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*$$/\1/' > $@

# use marky to download all links as a markdown file
offline: $(database) marky.rb
	mkdir -p offline
	while IFS='' read -r line || [[ -n "$$line" ]];\
	do\
		./marky.rb -o offline "$$line";\
	done < $<
