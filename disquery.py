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
    elif(sys.argv[1] == 'reset'):
        await reset(False, channel)
    elif(sys.argv[1] == 'hardreset'):
        await reset(True, channel)
    else:
        print(" [-] Bad argument : " + sys.argv[1])
        print("     --> first argument must be 'upload' or 'download'")
        return


async def reset(is_hard, channel):
    confirmed = await confirm_msg(is_hard)

    if is_hard and confirmed:
        counter = 0
        li = await channel.history(limit=1).flatten()
        last_msg = li[0] if len(li) else None
        print(" [~] Deleted " + str(counter) + " messages.", end="\r")

        while last_msg != None:
            await last_msg.delete()
            counter += 1
            print(" [~] Deleted " + str(counter) + " messages.", end="\r")
            li = await channel.history(limit=1).flatten()
            last_msg = li[0] if len(li) else None

        print("\n [+] Successfully cleared the index file.")
        await update_index_f_msg_id("")
        print(" [+] Done.")


    elif confirmed:
        await update_index_f_msg_id("")
        print(" [+] Successfully cleared the index file.")
        print(" [+] Done.")


async def confirm_msg(is_hard):
    if is_hard:
        print(" /!\ ")
        print(" /!\ You are about to reset the whole database.")
        print(" /!\ This means that the data will be lost forever.")
        print(" /!\ ")
        res = input(" /!\ Type 'confirm' if you want to continue : ")
        print()
        if res == ("confirm"):
            return True
    else:
        print(" /!\ ")
        print(" /!\ You are about to reset the index file.")
        print(" /!\ This means that you will still be able to get back the data manualy.")
        print(" /!\ ")
        res = input(" /!\ Do you want to continue ? y/n : ")
        print()
        if res == "y" or res == "yes" or res == "Y" or res == "YES":
            return True
    return False


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
        index_fetched = await fetch_index(channel, index_file_id)

        # send files, safe msg indexes and add line to the index file
        if(index_fetched):

            line_to_add = file_name
            for param_nb in range(3, len(sys.argv)):
                msg = await channel.send(file=discord.File(sys.argv[param_nb]))
                line_to_add += ("," + str(msg.id))

            print(" [+] Added line to index file : " + line_to_add)


            with open('index.csv', 'a') as index_file:
                index_file.write(line_to_add + "\n")

            await send_and_del_index(channel)

            print(' [+] Done.')

        else:
            print(" [-] Error : could not fetch the index file...")
            return


        #====================================================================================


async def update_index_f_msg_id(new_msg_id):
    a_file = open("discloud.conf", "r")
    list_of_lines = a_file.readlines()
    list_of_lines[2] = str(new_msg_id) + "\n"

    a_file = open("discloud.conf", "w")
    a_file.writelines(list_of_lines)
    a_file.close()


async def download_execution(channel):
    return


async def add_file_bdd(channel):
    return


async def fetch_index(channel, index_id):
    index_f_msg = await channel.fetch_message(index_id)
    for attach in index_f_msg.attachments:
        await attach.save(f"./index.csv")
    
    if (os.path.exists("index.csv")):
        return True
    else:
        return False


async def send_and_del_index(channel):
    msg = await channel.send(file=discord.File("index.csv"))
    await update_index_f_msg_id(msg.id)
    os.system('rm index.csv')
    print(' [+] Successfully sent the new index file.')


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
    if(index_file_id == "" or index_file_id == "\n"):
        print(" [~] index file message id not found : creating a new index file")
        await create_index_file(channel)

    else:
        print(" [+] index file message id found : " + index_file_id)



async def create_index_file(channel):
    with open('index.csv', 'w') as f:
        pass

    index_msg = await channel.send(file=discord.File('index.csv'))
    index_file_id = index_msg.id
    os.remove('index.csv')
    await update_index_f_msg_id(index_file_id)
    #with open('discloud.conf', 'a') as f:
    #    f.write(str(index_file_id))

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

