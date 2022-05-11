import discord
import sys
import os


client = discord.Client()


async def main_execution(channel):
    await test_index_file(channel)

    buffer = 0
    for i in range(1, len(sys.argv), 2):
        i += buffer

        if sys.argv[i] == "-m":
            message = await channel.send("got a -m ! : " + sys.argv[i+1])
            print(" [+] sent message id : " + str(message.id))

        elif sys.argv[i] == "-f":
            await channel.send(file=discord.File(sys.argv[i+1]))

        else:
            print(" [-] Bad argument : " + sys.argv[i])
            buffer-=1


# If an index file message id is found in the discloud.conf,
# it does nothing, but if none is found, it will make a new one
# in the channel and seve the message id in the .conf file (third line)
# =================================================================================
async def test_index_file(channel):
    if(index_file_id == ""):
        print(" [~] index file message id not found : creating a new index file")
        await create_index_file(channel)

    else:
        print(" [+] index file message id found")



async def create_index_file(channel):
    with open('index.csv', 'w') as f:
        pass

    index_msg = await channel.send(file=discord.File('index.csv'))
    os.remove('index.csv')
    with open('discloud.conf', 'a') as f:
        f.write(str(index_msg.id))

# =================================================================================


@client.event
async def on_ready():
    print(" [+] Logged in as {0.user}".format(client))
    channel = client.get_channel(int(channel_id))

    await main_execution(channel) 

    await client.close()


########################################## MAIN ##########################################

# variables 

with open("discloud.conf", 'r') as f:
    token = f.readline()            # token of the discord bot
    channel_id = f.readline()       # id of the channel that is used
    index_file_id = f.readline()    # id of the message that contains the index file


client.run(token)

exit()

