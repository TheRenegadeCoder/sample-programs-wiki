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

Currently, the script generates 27 pages: 1 alphabet catalog and 26 alphabet pages. 

The alphabet catalog contains a table with links to each alphabet page as well as meta data like the number
of scripts and languages per letter. In addition, the alphabet catalog contains the total number of scripts
and languages for the entire repo. 

Each alphabet page contains a table which lists each language for that particular letter as well as meta data
like the number of scripts per language and links to articles and issues.

## How to Run

At this time, the wiki generator is hardcoded for the Sample Programs repo. In order to run it,
you'll need a copy of the Sample Programs repo:

`git clone https://github.com/TheRenegadeCoder/sample-programs.git`

Then, you'll want to run the `generate-wiki.py` script as follows:

`python generate-wiki.py /path/to/sample-programs/repo/archive`

The solution is designed to then handle repo exploration from the `/archive/` directory. If successful, you should
begin to see print statements for the various links under test for The Renegade Coder. When finished, you'll
have a `/wiki/` directory next to your script which contains the wiki.

At this point, you can push the wiki directly to the Sample Programs wiki.
