lyrics-dl
=========

Features
--------

* Enter any artist and song name when prompted and lyrics will be printed to standard output
* Give an mp3 file as an attribute, and find lyrics using the mp3's metadata
* Save the obtained lyrics into the mp3's metadata

Support for other formats coming soon!

Installation
------------

* Via pip : ``pip install lyrics-dl``

Alternatively :-

1. Clone the repo
2. Enter the downloaded repo's root directory : ``cd lyrics-dl``
3. Install the required modules and its dependencies by running ``pip install -r requirements.txt`` (You may want to consider using a virtual environment)
4. Install lyrics-dl by running ``pip install .`` or ``python setup.py install``

Usage
-----

* Type ``lyrics-dl`` to receive prompt for artist and song name
* Type ``lyrics-dl <filenames>`` to obtain lyrics for mp3 files

**Note : Check lyrics-dl --help for in-depth instructions**
