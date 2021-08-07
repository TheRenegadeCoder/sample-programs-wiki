import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generate_docs",
    version="2.6.1",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="A docs generation package for the Sample Programs repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/sample-programs-docs-generator",
    packages=setuptools.find_packages(),
    install_requires=[
        "feedparser~=6.0.6",
        "beautifulsoup4~=4.9.3",
        "requests~=2.25.1",
        "SnakeMD~=0.7.0",
        "subete~=0.5.1"
    ],
    entry_points={
        "console_scripts": [
            'wikig = generate_docs.generator:main_wiki',
            'wikir = generate_docs.generator:main_readmes',
            'wikih = generate_docs.generator:main_how_to'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)
