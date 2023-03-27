# discloud

A MacOS / Linux program that uses a discord conversation channel to store stuff.
discloud.py will interact with discord and execute the queries thanks to a bot. It needs to have a discloud.conf file and also to have disclord.py installed (pip3 install discord.py).

Comming soon :
- an init mode to easily setup a discloud.conf file

## discloud.py

note : replace "./discloud.py" by the name you gave to the symlink (explained in the setup part)

```bash
./disquery.py
```

To list all files stored with date, size and category, or

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


## Setup

As said before, you will have to install discord.py :

```bash
pip3 install discord.py
```


Now cd into the directory you want to store the program in, clone the program in and cd into the new folder :

```bash
git clone https://github.com/Aweinhof/discloud.git
cd discloud
```


You will have to allow the prog to run as root, to avoid errors when saving files :
```bash
sudo chmod u+s discloud.py
```

The last step is to make a sym link to your prog in the /usr/local/bin directory (or any other $PATH's directory). This will make your prog executable from any directory. Besides that, you can also give it a short name (for example "dsc", but give it whatever you want) :

```bash
sudo ln -s "$PWD/discloud.py" /usr/local/bin/dsc
```

You should now be able to execute it with "dsc" anywhere in your file system

note : make sure that the name you give to your prog isn't an existing prog. To check that, execute the name in a terminal and make sure it tells you "command not found".


## index.csv

The index file will register all the files that are present in the channel and are fetchable.
Each line is a file. Here is the format of a line :

```
[file_name],[date],[category],[size],[msg_id_part_1],[msg_id_part_2],...,[msg_id_part_n]
```

Note that the discord size limit for a file is about 8 Mb.
For example a file named 'pythonlogo.png' that takes 20 Mb could be respresented as folowing :

```
pythonlogo.png,00/00/00 00:00,myimage,20-Mb,1111111111,1111111112,1111111113
```

The files contained in messages 1111111111 and 1111111112 would be about 8 Mb while the last one would be 4 Mb.
Those files would then be fetched, after what discloud.py will be able to reconstruct the complete file.


## discloud.conf

```
[discord bot token]
[channel_id]
[msg id of the msg that points to the index.csv file msg]
```

The reason I have to use a message as a pointer to another message that contains the index file is that the discloud.conf file needs to be fix in order to hold the state of the program on different machines. In fact, if discould.conf changes on a pc, it doesn't on the others. That's why discloud.conf points statically to a message that points dynamically to the index file. 

Only the discord bot token and channel id need to be set. The bot will automatically create a new index file.

In order to use this script, you will have to make your own discord application with a bot [here](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications) and get your bot token, put it in your discord server. The channel id is the id of the channel you want to use as data base. You can fetch it by right clicking the channel -> Copy ID (dev mode has to be enabled).


## Troubleshooting

If you're on MacOS and have python 3.6 or above, you might encounter an error due to a missing certificate. To solve this, go to your Application folder in your finder, open the python folder, and double click "Install Certificates.command" file.
