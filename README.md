# sorter
For sorting files etc.


## Installation

1. `python3 -m venv .venv` - creates a virtual environment.
1. `source .venv/bin/activate` - activates the virtual environment.
1. `deactivate` - deactivates the virtual environment.

1. `pip freeze > requirements.txt` - creates a requirements.txt file.
1. `pip install -r requirements.txt` - installs the required packages.

## TODO:

1. Create a .venv

## Functions We Want.

1. Delete .exe files after X days.
1. Clear Trash after X days.
1. Sort based on filetype + text, before just sorting by filetype.
1. Save every downloaded torrent qbittorent data to a file. To keep track of all downloads.
1. Make it work with qbittorrent so we wont sort if it's downloading/seeding.
1. Make it check with qbittorrent even when it's not running? So wont sort a uncompled download.