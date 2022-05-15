# discloud

A MacOS / Linux program that uses a discord conversation to store stuff.
discloud.py will interact with discord and execute the queries thanks to a bot. It needs to have a discloud.conf file and also to have disclord.py installed (pip3 install discord.py).

## discloud.py

```bash
./disquery.py [mode] [options]
```
### mode

- reset : resets the index file but the data will still be avaible on the discord channel. Recommended option if you are not sure that you can lose all your data.
- hardreset : resets everything definitively. Right option if you want to restart at 0 and you for sure want to delete the whole data.
- upload : uploads a file to discord.
- download : fetch data from discord.

### options

#### upload mode

First argument after "upload", must be the name you give to the uploading file. Other arguments are all the paths of the parsed data files.

#### download mode

nothing yet...


## index.csv

The index file will register all the files that are present in the channel and are fetchable.
Each line is a file. Here is the format of a line :

```
[file_name],[msg_id_part_1],[msg_id_part_2],...,[msg_id_part_n]
```

Note that the discord size limit for a file is about 8 Mb.
For example a file named 'pythonlogo.png' that takes 20 Mb could be respresented as folowing :

```
pythonlogo.png,1111111111,1111111112,1111111113
```

The files contained in messages 1111111111 and 1111111112 would be about 8 Mb while the last one would be 4 Mb.
Those files can then be fetched by disquery.py, after what discloud.sh will be able to reconstruct the complete file.


## discloud.conf

```
[discord bot token]
[channel_id]
[message id of the index.csv file]
```

