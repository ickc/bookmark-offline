# Pocket Export

## How to Use

Requirement:

- Pocket account, 
- `marky.rb` from [Marky the Markdownifier, reintroductions - BrettTerpstra.com](http://brettterpstra.com/2012/06/20/marky-the-markdownifier-reintroductions/), and any gem marky requires. Put marky.rb in this repository.

- Download [database from Pocket](https://getpocket.com/export)
- cd into this repository
- run `./extract-html.sh ril_export.html`
- run `./html2md.sh ril_export.txt`

All url will be downloaded and converted into markdown in a folder named `offline`.