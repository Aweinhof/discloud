# discloud

A MacOS / Linux program that uses a discord conversation to store stuff.
discloud.sh is the file that will treat the user's request while disquery.py will interact with discord and execute the queries thanks to a bot


## discloud.sh

Not much to tell here yet...


## disquery.py

```bash
Python3 disquery.py [mode] [options]
```
### mode
- upload : uploads data to discord
- download : fetch data from discord

### options
#### upload mode
- -m [message] : send a message to discord channel specified in the config file
- -f [file_path] : send a file to discord channel

#### download mode
nothing yet...


## discloud.conf

```
[discord bot token]
[channel_id]
```

