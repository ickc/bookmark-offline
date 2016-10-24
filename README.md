# Pocket Export

## How to Use

Requirement:

- Pocket account: Download [database from Pocket](https://getpocket.com/export) and put in `data/`.

- cd into this repository

- `marky.rb` from [Marky the Markdownifier, reintroductions - BrettTerpstra.com](http://brettterpstra.com/2012/06/20/marky-the-markdownifier-reintroductions/)

	- Put `marky.rb` in the current folder and make it executable by `chmod +x marky.rb`.

		- If you use git, `marky.rb` is already added as a submodule, and you can run `make marky.rb` to make it executable.

	- Install any gem marky requires, *e.g.* `gem install iconv`.

- run `make data`

- run `make offline`

All url will be downloaded and converted into markdown in a folder named `offline`.
