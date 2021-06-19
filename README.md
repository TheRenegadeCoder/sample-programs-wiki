# The Sample Programs Docs Generator

Previously known as the Sample Programs Wiki Generator, the Sample Programs Docs 
Generator repo houses the `generator.py` script which we use in the Sample Programs 
repository to generate our documentation. The script is automated by a GitHub Actions 
build in the Sample Programs repo.

If you would like to propose a change, feel free to leverage the issues tab or make 
a pull request.

## How It Works

The `generator.py` script works by analyzing the information in the Sample Programs 
repository and storing that information in objects. These objects are then used to 
generate various documentation pages in Markdown. 

## What is Automated

Currently, the script does two things:

- It maintains our entire [Sample Programs wiki](https://github.com/TheRenegadeCoder/sample-programs/wiki)
- It maintains all of our READMEs in the Sample Programs repo

In terms of wiki automation, it generates 27 pages: 1 alphabet catalog and 26 alphabet pages.

The alphabet catalog contains a table with links to each alphabet page as well as 
metadata like the number of scripts and languages per letter. In addition, the 
alphabet catalog contains the total number of scripts and languages for the entire repo.

Each alphabet page contains a table which lists each language for that particular letter 
as well as metadata like the number of scripts per language as well as linking to articles 
and issues.

## How to Run

At this time, the wiki generator is hardcoded for the Sample Programs repo. In order to 
run it, you can install it as a package using `pip`:

`pip install generate_docs`

After that, you'll need a copy of the Sample Programs repo:

`git clone https://github.com/TheRenegadeCoder/sample-programs.git`

Finally, you can build the wiki using the following command:

`wikig /path/to/sample-programs/repo/archive`

Likewise, you can build the READMEs using the following command:

`wikir /path/to/sample-programs/repo/archive`

Alternatively, you can clone this repo to run the `generate_wiki.py` script directly:

`python generator.py /path/to/sample-programs/repo/archive`

Both solutions are designed to handle repo exploration from the `/archive/` directory. 
If successful, you should begin to see print statements for the various links under test 
for The Renegade Coder. When finished, you'll have a `/wiki/` directory next to your script
which contains the wiki. Likewise, all the READMEs should be updated.

At this point, you can push the wiki directly to the Sample Programs wiki.

Recently, as of 2.3.0, this script has been expanded to support projects outside
of the Sample Programs repo. For example, this code now supports the automated
generation of the How to Python repo as follows:

`wikih`

That's it!

