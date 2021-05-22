import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generate_docs",
    version="2.2.0",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="A docs generation package for the Sample Programs repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/sample-programs-docs-generator",
    packages=setuptools.find_packages(),
    install_requires=[
        "PyYAML~=5.4.1"
    ],
    entry_points={
        "console_scripts": [
            'wikig = generate_docs.generator:main_wiki',
            'wikir = generate_docs.generator:main_readmes',
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)
