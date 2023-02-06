# TgYTDownload bot
Telegram bot for downloading videos from YouTube

## Features:
- Downloading single video by YouTube link
- Downloading whole playlist
- Downloading subtitles and convert it to .srt format (for MPC - Media Player Classic) 
- MP4 format and resolution 720p or lower (can be changed in source code)

## Usage:
Bot accepts private messages with link to YT video or YT playlist, then he send action "writing..." to show the work started.
At starting download will be sent message: 

    Starting !video file name! 
    Resolution: !max available and allowed resolution!

At finishing download:
    
    Done !video file name!
    
When the list has been downloaded:
    
    List done

## Installation
Setup requirements:
```
pip install -r requirements.txt
```
Run:
```
python tgytdownload_bot.py "D:\\YouTube" "<your tg bot token>"
```