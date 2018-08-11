# The Sample Programs Wiki Generator

Currently, the Sample Programs Wiki Generator repo houses the `generate-wiki.py` script which
we use in the Sample Programs repository to generate our wiki documentation. The script
is automated by a Travis CI build in the Sample Programs repo.

If you would like to propose a change, feel free to leverage the issues tab or make a pull request.

## How It Works

The `generate-wiki.py` script works by analyzing the information in the Sample Programs
repository and storing that information in objects. These objects are then used to
generate various wiki pages in Markdown. 

## What is Automated

Currently, the script generates 27 pages: one alphabet catalog and 26 alphabet pages. The alphabet
catalog contains a table with links to each alphabet page as well as meta data like the number
of scripts and languages per letter as well as the totals for the entire repo. Each alphabet page
contains a table which lists each language for that particular letter as well as meta data
like the number of scripts per language and links to articles and issues.
