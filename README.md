# uLauncher anime extension for linux

### Little tool written in python to watch anime using Ulauncher (the better way to watch anime)
### Scrapes: https://gogoanime.wiki

[Still in development]

# Dependencies:
- `Python 3.0`

- `BeautifulSoup`

- `requests`

- `selenium`

- `Firefox/Chrome/Chromium`

- `cURL`

- `mpv`
 

# Install
Open ulauncher preferences window -> extensions -> add extension and paste the following url:


## Install Dependencies

#### [Note] Just do `make deps` to install.
 
### 1. Other dependencies
Get Python from: https://www.python.org/downloads/

Get mpv from: https://mpv.io/installation/

Curl should be preinstalled on Windows, Linux and macOS if not get it from here: https://curl.se/download.html

### 2. Python-Libs
You can manually install dependencies:

To install `bs4`, `selenium`, `requests` and `webdriver-manager` open a terminal in the root-folder and execute `pip install -r requirements.txt`

### 3. Webdriver (Needs Firefox/Chrome/Chromium)

Please have one of these browsers installed: Firefox/Chrome/Chromium 

Installation:

### 2. Other dependencies
Get Python from: https://www.python.org/downloads/

Get mpv from: https://mpv.io/installation/

Curl should be preinstalled, if not get it from here: https://curl.se/download.html

### 3. Python-Libs

To install `bs4`, `selenium` and `requests` open a terminal in the root-folder and execute `pip install -r requirements.txt`

## Start up 
Start ulauncher and type `ani`.


## Development
Git clone this repo.

In repo folder do `make link` to create symlink to ulauncher extensions folder.

Close ulauncher and run `make dev` and follow instructions in terminal.

You will get code that looks something like this:
```
 VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/com.github.dankni95.ulauncher-anime PYTHONPATH=/usr/lib/python3.9/site-packages /bin/python /home/daniel/.local/share/ulauncher/extensions/com.github.dankni95.ulauncher-anime/main.py
```
Paste it in new terminal window and run keyword `ani`. 


# Credits
#### This extension uses https://github.com/sdaqo/anipy-cli 
