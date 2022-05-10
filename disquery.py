import discord
import sys


client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    channel = client.get_channel(int(channel_id))

    for i in range(1, len(sys.argv[1:]), 2):

        if sys.argv[i] == "-m":
            await channel.send("got a -m ! : " + sys.argv[i+1])
        elif sys.argv[i] == "-f":
            await channel.send(file=discord.File(sys.argv[i+1]))
        else:
            print("wrong arg")

    await client.close()


########################################## MAIN ##########################################

with open("discloud.conf", 'r') as f:
    token = f.readline()
    channel_id = f.readline()




client.run(token)

exit()

