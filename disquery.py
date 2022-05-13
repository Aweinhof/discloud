import discord
import sys
import os


client = discord.Client()

# Litle function to easily quit the program
async def quit_prog():
    await client.close()


async def main_execution(channel):
    await test_index_file(channel)

    if(sys.argv[1] == 'upload'):
        await upload_execution(channel)
    elif(sys.argv[1] == 'download'):
        await download_execution(channel)
    else:
        print(" [-] Bad argument : " + sys.argv[1])
        print("     --> first argument must be 'upload' or 'download'")
        return


async def upload_execution(channel):
    check = await check_files()

    if(check):

        # here we have to refetch the index_file_id, needed if we just created an index file
        with open("discloud.conf", 'r') as f:
            token = f.readline()            # token of the discord bot
            channel_id = f.readline()       # id of the channel that is used
            index_file_id = f.readline()    # id of the message that contains the index file

        #=================== treatment : send file and update index file  ===================

        file_name = sys.argv[2]
        index_fetched = await fetch_index()

        # TODO : send files and add line to the index file
        if(index_fetched):
            pass

        else:
            print(" [-] Error : could not fetch the index file...")
            return


        await send_and_del_index(channel)

        #====================================================================================



async def download_execution(channel):
    return


async def add_file_bdd(channel):
    return


async def fetch_index(channel):
    return


async def send_and_del_index(channel):
    return


async def check_files():
    for i in range(3, len(sys.argv)):
        file_exist = os.path.exists(sys.argv[i])
        if not file_exist:
            print(" [-] file not exist !")
            await quit_prog()
            return False

        size = os.path.getsize(sys.argv[i])
        if(size > 8000000):
            print(' [-] Size of file is', int(size/1000000), 'Mb, must not exceed 8 Mb.')
            await quit_prog()
            return False

    return True


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
    index_file_id = index_msg.id
    os.remove('index.csv')
    with open('discloud.conf', 'a') as f:
        f.write(str(index_file_id))

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

