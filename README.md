# discloud

A MacOS / Linux (not yet MacOS) program that uses a discord conversation to store stuff.
discloud.py will interact with discord and execute the queries thanks to a bot. It needs to have a discloud.conf file and also to have disclord.py installed (pip3 install discord.py).

Comming soon :
- The size of each file when you list them
- an init mode to easily setup a discloud.conf file

## discloud.py
```bash
./disquery.py
```

To list all files stored with date and category, or

```bash
./disquery.py [category]
```

To list all the files of the specified category, or either

```bash
./disquery.py [mode] [options]
```
### mode

- reset : resets the index file but the data will still be avaible on the discord channel. Recommended option if you are not sure that you can lose all your data.
- hardreset : resets everything definitively. Right option if you want to restart at 0 and you for sure want to delete the whole data.

- upload | u : uploads a file to discord.
- download | d : fetch data from discord.

- category | Category | categ | c : gives a list of all the used categories.

### options

Options are only required for these modes :

#### upload mode

The only argument with "upload" must be the path of the file to upload.

#### download mode

Argument after download must be the name of the file you want to download.

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
Those files would then be fetched, after what discloud.py will be able to reconstruct the complete file.


## discloud.conf

```
[discord bot token]
[channel_id]
[message id of the index.csv file]
```

Only the discord bot token and channel id need to be set. The bot will automatically create a new index file.

In order to use this script, you will have to make your own discord application with a bot [here](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications) and get your bot token, put it in your discord server. The channel id is the id of the channel you want to use as data base. You can fetch it by right clicking the channel -> Copy ID (dev mode has to be enabled).
