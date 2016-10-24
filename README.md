# Pocket Export

## How to Use

Requirement:

- Pocket account, 
- `marky.rb` from [Marky the Markdownifier, reintroductions - BrettTerpstra.com](http://brettterpstra.com/2012/06/20/marky-the-markdownifier-reintroductions/), and any gem marky requires.
	- Put `marky.rb` in subfolder `submodule/`. If you use git, `marky.rb` is already added as a submodule.

- Download [database from Pocket](https://getpocket.com/export) and put in `data/`.
- cd into this repository
- run `make data`
- run `./html2md.sh ril_export.txt`

All url will be downloaded and converted into markdown in a folder named `offline`.
