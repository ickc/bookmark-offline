SHELL := /bin/bash

pocketExport := $(wildcard data/*.html)
database := $(patsubst %.html,%.txt,$(pocketExport))

data: $(database)

# update submodule
update:
	git submodule update --recursive --remote

%.txt: %.html
	grep -i href $< | sed 's/^.*href="\([^"]*\)".*$$/\1/' > $@

marky.rb: submodule/marky.rb
	rsync $< $@
	chmod +x $@

offline: $(database) marky.rb
	mkdir -p offline
	while IFS='' read -r line || [[ -n "$$line" ]];\
	do\
		./marky.rb -o offline "$$line";\
	done < $<
