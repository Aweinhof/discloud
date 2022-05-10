import discord

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("Received a message : closing")
    await client.close()



########################################## MAIN ##########################################

with open("discloud.conf", 'r') as f:
    token = f.read()

client.run(token)

exit()
