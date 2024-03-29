#!/usr/bin/python3

import discord
import sys
import os
import time


intents = discord.Intents.default()

#client = discord.Client(restTimeOffset=0)
client = discord.Client(intents=intents)

# Litle function to easily quit the program
async def quit_prog():
    await client.close()


async def main_execution(channel):
    await test_index_file(channel)

    if(len(sys.argv) == 1):
        await show_files(channel)

    elif sys.argv[1] == 'category' or sys.argv[1] == 'c' or sys.argv[1] == 'categ' or sys.argv[1] == 'Category':
        await show_categories(channel)

    elif(sys.argv[1] == 'upload_query'):
        if len(sys.argv) < 3:
            print(" [-] Bad argument : " + sys.argv[1])
            print("     --> upload_query argument must be followed by other arguments")
            return
        else:
            await upload_query_execution(channel)

    elif(sys.argv[1] == 'download' or sys.argv[1] == 'd'):
        if len(sys.argv) < 3:
            print(" [-] Bad argument : " + sys.argv[1])
            print("     --> download argument must be followed by the file name you want to download")
            return
        else:
            await download_execution(channel)

    elif(sys.argv[1] == 'reset'):
        await reset(False, channel)

    elif(sys.argv[1] == 'hardreset'):
        await reset(True, channel)
    else:
        if not await show_by_category(channel):
            print(" [-] Bad argument : " + sys.argv[1])
            print("     --> first argument must be 'upload', 'download' or either a category")
            return

async def show_by_category(channel):
    index = await get_index_list(channel)
    index_lines = []
    for i in range(len(index)):
        if(index[i].split(',')[2] == sys.argv[1]):
            index_lines.append(index[i])

    if len(index_lines) == 0:
        return False
    else:
        await show_files_by_category(index_lines)        
        return True


async def show_files_by_category(list_of_lines):
    name_size = 30
    category_size = 20
    date_size = 16
    filesize_size = 10

    async def add_line(file_n, categ_n, size_n, date_n):
        space_name_before = int(((name_size - len(file_n))/2))
        space_name_after = (name_size - len(file_n)) - space_name_before
    
        space_categ_before = int(((category_size - len(categ_n))/2))
        space_categ_after = (category_size - len(categ_n)) - space_categ_before

        space_date_before = int(((date_size - len(date_n))/2))
        space_date_after = (date_size - len(date_n)) - space_date_before

        space_size_before = int(((filesize_size - len(size_n))/2))
        space_size_after = (filesize_size - len(size_n)) - space_size_before

        print("# " + 
            space_name_before*" " + file_n + space_name_after*" " + 
            " # " + 
            space_categ_before*" " + categ_n + space_categ_after*" " + 
            " # " + 
            space_size_before*" " + size_n + space_size_after*" " +
            " # " +
            space_date_before*" " + date_n + space_date_after*" " + 
            " #")

    print("#############" + (name_size + category_size + filesize_size + date_size)*"#")
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")

    await add_line("Filename", "Category", "Size", "Date")
        
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")
    print("#############" + (name_size + category_size + filesize_size + date_size)*"#")
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")

    for line in list_of_lines:
        filename = line.split(",")[0]
        categ = line.split(",")[2]
        date = line.split(",")[1]
        size = line.split(",")[3].replace("-", " ")
        await add_line(filename, categ, size, date)
    
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")
    print("#############" + (name_size + category_size + filesize_size + date_size)*"#")


def upload_execution():
    os.system('mkdir tempcontainer')
    size = getSize(sys.argv[2])
    filename = sys.argv[2].split('/')[-1]

    # ------- old command that worked on linux -------
    #splitquery = "split " + sys.argv[2] + " -b 8M -d tempcontainer/" + filename

    # ------- new that should work on both linux and MacOS -------
    splitquery = "split -b 8m " + sys.argv[2] + " tempcontainer/"

    os.system(splitquery)
    
    uploadquery = complete_path + " upload_query " + filename + " " + size
    for file in sorted(os.listdir('tempcontainer')):
        uploadquery += " tempcontainer/" + file

    os.system(uploadquery)
    os.system('rm -r tempcontainer')


def getSize(filename):
    size = os.path.getsize(filename)
    res = ""

    if size < 1000:
        # b
        res = str(size) + "-b"

    elif size < 1000000:
        # Kb
        res = str(size // 1000) + "-Kb"

    elif size < 1000000000:
        # Mb
        res = str(size // 1000000) + "-Mb"

    else:
        # Gb
        res = str(size // 1000000000) + "-Gb"

    return res


async def reset(is_hard, channel):
    confirmed = await confirm_msg(is_hard)

    if is_hard and confirmed:
        await update_index_f_msg_id("/", channel)

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
        print(" [+] Done.")


    elif confirmed:
        await update_index_f_msg_id("/", channel)
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


async def get_index_list(channel):
    files_list = list()
    await fetch_index(channel)
    with open("index.csv", 'r') as ifile:
        for line in ifile:
            files_list.append(line.replace('\n', ''))

    os.system('rm index.csv')
    return files_list


async def show_files(channel):
    name_size = 30
    category_size = 20
    date_size = 16
    filesize_size = 10

    async def add_line(file_n, categ_n, size_n, date_n):
        space_name_before = int(((name_size - len(file_n))/2))
        space_name_after = (name_size - len(file_n)) - space_name_before
    
        space_categ_before = int(((category_size - len(categ_n))/2))
        space_categ_after = (category_size - len(categ_n)) - space_categ_before

        space_date_before = int(((date_size - len(date_n))/2))
        space_date_after = (date_size - len(date_n)) - space_date_before

        space_size_before = int(((filesize_size - len(size_n))/2))
        space_size_after = (filesize_size - len(size_n)) - space_size_before

        print("# " + 
            space_name_before*" " + file_n + space_name_after*" " + 
            " # " + 
            space_categ_before*" " + categ_n + space_categ_after*" " + 
            " # " + 
            space_size_before*" " + size_n + space_size_after*" " +
            " # " +
            space_date_before*" " + date_n + space_date_after*" " + 
            " #")

    print("#############" + (name_size + category_size + filesize_size + date_size)*"#")
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")

    await add_line("Filename", "Category", "Size", "Date")
        
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")
    print("#############" + (name_size + category_size + filesize_size + date_size)*"#")
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")

    await fetch_index(channel)
    with open("index.csv", 'r') as ifile:
        for line in ifile:
            filename = line.split(",")[0]
            categ = line.split(",")[2]
            date = line.split(",")[1]
            size = line.split(",")[3].replace("-", " ")
            await add_line(filename, categ, size, date)
    
    print("# " + name_size*" " + " # " + category_size*" " + " # " + filesize_size*" " + " # " + date_size*" " + " #")
    print("#############" + (name_size + category_size + filesize_size + date_size)*"#")

    os.system('rm index.csv')


async def show_categories(channel):
    categ_size = 20

    async def add_line(categ):
        space_before = int((categ_size - len(categ))/2)
        space_after = categ_size - space_before - len(categ)
        print("# " + space_before*" " + categ + space_after*" " + " #")

    print("####" + categ_size*"#")
    print("# " + categ_size*" " + " #")
    await add_line("Categories")
    print("# " + categ_size*" " + " #")
    print("####" + categ_size*"#")
    print("# " + categ_size*" " + " #")

    await fetch_index(channel)
    categories = set()
    with open("index.csv", 'r') as ifile:
        for line in ifile:
            categories.add( line.split(",")[2] )
    if not categories.isdisjoint({''}):
        categories.remove('')

    for cat in categories:
        await add_line(cat)

    print("# " + categ_size*" " + " #")
    print("####" + categ_size*"#")


async def upload_query_execution(channel):
    check = await check_files()

    if(check):
        ca = '////////'
        
        while ca == '////////':
            ca = input(" [~] Category (ENTR for none) : ")
            if ca == 'c' \
                or ca == 'categ' \
                or ca == 'category' \
                or ca == 'Category' \
                or ca == 'upload' \
                or ca == 'download' \
                or ca == 'u' \
                or ca == 'c' \
                or ca == 'C' \
                or ca == 'd' \
                or ca == 'U' \
                or ca == 'D':
                    ca = '////////'
                    print("\n [-] Please use another category name")
            elif len(ca.split(' ')) > 1 \
                or len(ca.split(',')) > 1 \
                or len(ca.split('.')) > 1 \
                or len(ca.split(':')) > 1 \
                or len(ca.split('"')) > 1 \
                or len(ca.split("'")) > 1 \
                or len(ca.split('@')) > 1:
                    ca = '////////'
                    print("\n [-] Please avoid the use of spaces and special characters")
            print("\n")
        

        file_name = sys.argv[2]
        index_fetched = await fetch_index(channel)

        # send files, safe msg indexes and add line to the index file
        if(index_fetched):

            line_to_add = file_name + "," + time.strftime("%D %H:%M") + "," + ca + "," + sys.argv[3]
            amount_files = len(sys.argv) - 4
            print(" [~] Sending files 0/" + str(amount_files) + " : 0 %", end='\r')
            for param_nb in range(4, len(sys.argv)):
                msg = await channel.send(file=discord.File(sys.argv[param_nb]))
                line_to_add += ("," + str(msg.id))

                advancement = str(int(((param_nb-2) / amount_files) * 100))
                print(" [~] Sending files " + str(param_nb-2) + "/" + str(amount_files) + " : " + advancement + " %", end='\r')
            print(" [~] Sending files " + str(amount_files) + "/" + str(amount_files) + " : 100 %" + "\n")

            
            with open('index.csv', 'a') as index_file:
                index_file.write(line_to_add + "\n")

            await send_and_del_index(channel)

            print(" [+] Added line to index file : " + line_to_add)
            print(' [+] Done.')

        else:
            print(" [-] Error : could not fetch the index file...")
            return


        #====================================================================================


async def update_index_f_msg_id(new_msg_id, channel):
    with open(complete_path.replace("discloud.py", "discloud.conf"), 'r') as f:
        token = f.readline()            # token of the discord bot
        channel_id = f.readline()       # id of the channel that is used
        index_id = f.readline()         # id of the message that contains the index file

    index_msg = await channel.fetch_message(index_id)
    await index_msg.edit(content=new_msg_id)


async def update_pointermsg_id(new_msg_id):
    a_file = open(complete_path.replace("discloud.py", "discloud.conf"), "r")
    list_of_lines = a_file.readlines()
    list_of_lines[2] = str(new_msg_id) + "\n"

    a_file = open(complete_path.replace("discloud.py", "discloud.conf"), "w")
    a_file.writelines(list_of_lines)
    a_file.close()


async def download_execution(channel):
    index = await get_index_list(channel)
    index_line = ""
    for i in range(len(index)):
        j = len(index) - 1 - i
        if(index[j].split(',')[0] == sys.argv[2]):
            index_line = index[j]
            break

    if(index_line == ""):
        print(" [-] Given file not found in the index file.")
    else:
        print(" [+] File found, last version taken.")
        os.system('mkdir tempcontainer')
        i = 0
        amount_files = len(index_line.split(',')) - 4
        print(" [~] Downloading files 1/" + str(amount_files) +" : 0 %", end='\r')

        for msg_id in index_line.split(',')[4:]:
            msg = await channel.fetch_message(int(msg_id))
            for attach in msg.attachments:
                #filename = sys.argv[2] + str(i)
                amount0 = 7 - len(str(i))
                filename = amount0 * "0" + str(i)
                await attach.save(f"tempcontainer/{filename}")
                i += 1
                advancement = str(int((i / amount_files) * 100))
                print(" [~] Downloading files " + str(i) + "/" + str(amount_files) + " : " + advancement + " %", end='\r')

        print(" [~] Downloading files " + str(i) + "/" + str(amount_files) + " : " + advancement + " %")
        print(" [~] Restitution of the original file...")
        #catquery = "cat tempcontainer/" + sys.argv[2] + "* > " + sys.argv[2]
        catquery = "cat tempcontainer/* > " + sys.argv[2]
        os.system(catquery)
        os.system('rm -r tempcontainer')

    return


async def fetch_index(channel):
    # here we have to refetch the index_file_id, needed if we just created an index file
    with open(complete_path.replace("discloud.py", "discloud.conf"), 'r') as f:
        token = f.readline()            # token of the discord bot
        channel_id = f.readline()       # id of the channel that is used
        index_id = f.readline()    # id of the message that contains the index file

    index_msg = await channel.fetch_message(index_id)
    index_f_msg_index = index_msg.content   # this is the index of the msg that contains the index file
    index_f_msg = await channel.fetch_message(index_f_msg_index)

    for attach in index_f_msg.attachments:
        await attach.save(f"./index.csv")
    
    if (os.path.exists("index.csv")):
        return True
    else:
        return False


async def send_and_del_index(channel):
    msg = await channel.send(file=discord.File("index.csv"))
    await update_index_f_msg_id(msg.id, channel)
    os.system('rm index.csv')
    print(' [+] Successfully sent the new index file.')


async def check_files():
    for i in range(4, len(sys.argv)):
        file_exist = os.path.exists(sys.argv[i])
        if not file_exist:
            print(" [-] file not exist !")
            await quit_prog()
            return False

        size = os.path.getsize(sys.argv[i])
        if(size > 8388608):
            print(' [-] Size of file is', int(size/1048576), 'Mb, must not exceed 8 Mb.')
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
        try:
            container_msg = await channel.fetch_message(int(index_file_id))
            indexmsg_id = container_msg.content
            if indexmsg_id == "/":
                raise Exception("")
            await channel.fetch_message(int(indexmsg_id))
        except:
            print(" [~] could not find either the indexfile pointer msg or the indexfile msg")
            print(" [~]     --> creating a new index file")
            await create_index_file(channel)
        else:
            print(" [+] index file message id found : " + index_file_id)




async def create_index_file(channel):
    with open('index.csv', 'w') as f:
        pass

    index_msg = await channel.send(file=discord.File('index.csv'))
    index_file_id = index_msg.id

    pointer_msg = await channel.send(int(index_file_id))
    pointer_msg_id = pointer_msg.id

    os.remove('index.csv')
    await update_pointermsg_id(pointer_msg_id)
    #await update_index_f_msg_id(index_file_id, channel)


# =================================================================================


@client.event
async def on_ready():
    print(" [+] Logged in as {0.user}".format(client))
    channel = client.get_channel(int(channel_id))

    await main_execution(channel) 

    await client.close()


########################################## MAIN ##########################################

complete_path = os.path.realpath(__file__)

# variables 
with open(complete_path.replace("discloud.py", "discloud.conf"), 'r') as f:
    token = f.readline()            # token of the discord bot
    channel_id = f.readline()       # id of the channel that is used
    index_file_id = f.readline()    # id of the message that contains the index file

if(len(sys.argv) > 1 and (sys.argv[1] == 'upload' or sys.argv[1] == 'u')):
    if len(sys.argv) != 3:
        print(" [-] Bad argument : must specify a file after upload")
        print("     --> upload argument must be followed by only one argument")
        exit()
    elif not os.path.exists(sys.argv[2]):
        print(" [-] Bad argument : " + sys.argv[2])
        print("     --> file doesn't exists")
        exit()
    else:
        upload_execution()
        exit()


print(token)
client.run(token)

exit()

