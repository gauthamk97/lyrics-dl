getlyrics
=========

getlyrics is a tool that scrapes the lyrics to your favorite songs off of AZLyrics

Features
--------

* Enter any artist and song name when prompted and lyrics will be printed to standard output
* Give an mp3 file as an attribute, and find lyrics using the mp3's metadata
* Save the obtained lyrics into the mp3's metadata

Support for other formats coming soon!

Installation
------------

1. Clone the repo
2. Enter the downloaded repo's root directory : ``cd getlyrics``
3. Install the required modules and its dependencies by running ``pip install -r requirements.txt`` (You may want to consider using a virtual environment)
4. Install getlyrics by running ``pip install .`` or ``python setup.py install``

Usage
-----

* Type ``getlyrics`` to receive prompt for artist and song name
* Type ``getlyrics <filenames>`` to obtain lyrics for mp3 files

**Note : Check getlyrics --help for more details**
