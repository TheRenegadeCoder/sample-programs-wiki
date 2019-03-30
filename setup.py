import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generate_wiki",
    version="1.1.1",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="A wiki generation package for the Sample Programs repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/sample-programs-wiki-generator",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": [
            'wikig = generate_wiki.generate_wiki:main',
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)
