This document describes how to use the scripts and utilities in this directory to download labelled play-by-play clips 
from stats.nba.com

These tools have been tested on OS X. They *probably* work on Linux and Unix-like layers on Windows (WSL, Cygwin).

The following steps worked well as of September 2018, but may need some tweaks if the NBA website changes dramatically in the future.

## Step 0: Prerequisites
We'll be using Python 3, Node.js, and some built-in Unix utilities. You'll also need to download [ChromeDriver](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver) 
for your specific platform.

## Step 1: Get the game IDs for the relevant games

The easiest way I found to do this for all games is to go to the [schedule page](https://stats.nba.com/schedule/#!?Month=1&PD=N) NBA website, scroll down
until the screen has scores for as many (finished) games as you want, right-click and *Save page as* `<file name>.htm`.
If you look at the HTML file, you'll notice that completed games have an associated tag with a link to the game's play-by-play or box-score page - usually something like 
`... href="/game/0011800012/playbyplay/ ... "`. The number in that link is the game ID - we'll use grep to extract all the ids on the page into a file called game_ids:

```bash
grep -oh "game\/[0-9]*\/playbyplay\/" games_2017_18.htm | tr -d 'game/playbyplay' > game_ids
```

## Step 2: Download play descriptions for games

```bash
mkdir plays
node get_game_events.js
```
This script iterates through the games in the `game_ids` file, and creates a file for each game in the `plays` directory we just created.
Each of these files will consist of plays in the following format:
```
Play 1 description (ex - Curry three point shot ...)
Link to the play on stats.nba.com
...
```

## Step 3. Download the videos of all plays in one or more games
NBA.com makes this a pain in the ass to do purely programatically, so we use Selenium to create a bunch of real browser sessions.

Around line 90 of `selenium_video_downloader.js`, specify the path to the game play file (from step 2) from which you want to
download videos. You can also specify how many plays to download in total:

```js
// Specify game file with play info, and how many plays to download.
const filePath = 'path_to_plays_file';
const numPlaysToDownload = 100;
```

Then simply run:
```
node selenium_video_downloader.js
```

This should fire up a bunch of Chrome windows which navigate to the page with the video for each play, click on the video to
 get it to play, and then save it.
 
 ## [Optional] Step 4. Sort the videos into directories by play type
 Near the top of `sort_videos.py`, specify the paths to your source and destination directories:

 ```python
UNSORTED_VIDS_DIR = '/path/to/dir/containing/unsorted/video/files'     # ex - '/Users/username/Desktop/all_videos'
DEST_DIR = '/path/where/you/want/sorted/folders/to/go'                 # ex - '/Users/username/Desktop/sorted_videos'
 ```
 
 Then run:
 ```
 python sort_videos.py
 ```

