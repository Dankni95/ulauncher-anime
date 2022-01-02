# [uLauncher](https://github.com/Ulauncher/Ulauncher) anime extension for linux

<p align="center">
   <img src="https://user-images.githubusercontent.com/71786017/147852497-269e49a5-f3ba-40ed-ae09-8053b7119ecb.gif" alt="animated" />
</p>



### Little tool written in python to watch anime using uLauncher (the better way to watch anime)
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
Open uLauncher preferences window -> extensions -> add extension and paste the following url:
`https://github.com/Dankni95/ulauncher-anime`


## Install Dependencies

#### [ Automatic dependecy install ] `cd ~/.local/share/ulauncher/extensions/com.github.dankni95.ulauncher-anime` and run `make deps` to install dependencies.
 
### 1. Other dependencies
Get Python from: https://www.python.org/downloads/

Get mpv from: https://mpv.io/installation/

Curl should be preinstalled, if not get it from here: https://curl.se/download.html

### 2. Python-Libs
[ Manual dependecy install ] To install `bs4`, `selenium`, `requests` and `webdriver-manager` open a terminal and go to repo root `cd ~/.local/share/ulauncher/extensions/com.github.dankni95.ulauncher-anime` and execute `pip install -r requirements.txt`

### 3. Webdriver (Needs Firefox/Chrome/Chromium)

Please have one of these browsers installed: Firefox/Chrome/Chromium 

## Start up 
Start uLauncher and type `ani`.
To search `ani s <your anime>`

## History
 `ani h ` shows next episode of previously watched anime.<br>
![image](https://user-images.githubusercontent.com/71786017/147886901-4c66d977-d7f0-4831-a252-05a8514642d2.png)



## Development
Git clone this repo.

In repo folder do `make link` to create symlink to ulauncher extensions folder.

Close uLauncher and run `make dev` and follow instructions in terminal.

You will get code that looks something like this:
```
 VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/com.github.dankni95.ulauncher-anime PYTHONPATH=/usr/lib/python3.9/site-packages /bin/python /home/daniel/.local/share/ulauncher/extensions/com.github.dankni95.ulauncher-anime/main.py
```
Paste it in new terminal window and run keyword `ani` in uLauncher. 
Happy coding!

This is one of my first python projects, in advance sorry for the spaghetti code!


# Credits
#### This extension uses https://github.com/sdaqo/anipy-cli 
#### This extension uses uLauncher as main driver https://github.com/Ulauncher/Ulauncher
