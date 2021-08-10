import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jisho",
    version="0.1.1",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="A wiki generation package for the Sample Programs repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/sample-programs-wiki",
    packages=setuptools.find_packages(),
    install_requires=[
        "SnakeMD>=0.7",
        "subete>=0.6"
    ],
    entry_points={
        "console_scripts": [
            'jisho = jisho.wiki:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
