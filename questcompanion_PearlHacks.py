import random
import discord
import csv
import json
import csv
import asyncio
import datetime

# from discord.ext import commands
# Settings
bot_token = "Add TOKEN here"

client = discord.Client()

prefix = '!'
welcome_to_quest_image = "http://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/crossed-swords.png" #to be changed

errormessage_colour = 0xafa7e8
quotemessage_colour = 0x731c5a
rainbow_colours = [0xf54842, 0xf58f1b, 0xf5dc3b, 0x88ed5c, 0x12b86d, 0x4bc6db, 0x6c58c4, 0x9a1eb3, 0xd41360]
deletemessage_colour = 0x0dba2d
check_sure_archive_colour = 0xafa7e8
helpcommand = "!help"
BotName = "QuestCompanion"


images = ['DETOX.jpg', '5.jpg', '6.jpg', '7.jpg', 'boticon.gif', 'questcompanion_banner.png']
quotes = []
with open('quotes_QC.txt', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    quotes = list(reader)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


async def initiate_questcompanion(thisguild):
    categorychannels, voicechannels, textchannels = await get_existing_channelnames(thisguild)

    # Create any of the categories that do not exist yet
    if "Active-Quests" not in categorychannels:
        await thisguild.create_category(name="Active-Quests")

    if "Archived-Quests" not in categorychannels:
        await thisguild.create_category(name="Archived-Quests")

    if "New-Quests" not in categorychannels:
        newchallenges = await thisguild.create_category(name="New-Quests")
        await thisguild.create_text_channel(name="Create-Quests", category=newchallenges)

    if "Notice-Board" not in categorychannels:
        noticeboard = await thisguild.create_category(name="Notice-Board")
        await thisguild.create_text_channel(name="Welcome", category=noticeboard)
        await thisguild.create_text_channel(name="Rules", category=noticeboard)
        await thisguild.create_text_channel(name="Roles", category=noticeboard)
        await thisguild.create_text_channel(name="Change Log", category=noticeboard)

    return


async def get_existing_channelnames(thisguild):
    # Check which category channels already exist in the guild
    allchannels = thisguild.channels
    categorychannels = []
    voicechannels = []
    textchannels = []
    for channel in allchannels:
        if channel.type[0] == 'category':
            categorychannels.append(channel.name)
        if channel.type[0] == 'voice':
            voicechannels.append([channel.name, channel.category.name])
        if channel.type[0] == 'text':
            try:
                category_of_channel = channel.category.name
            except:
                category_of_channel = 'none'
            textchannels.append([channel.name, category_of_channel])
    return categorychannels, voicechannels, textchannels


async def get_categoryinstance(thisguild, instancename):
    # Get a category instance to use to move/create a channel in the correct category
    allchannels = thisguild.channels

    for channel in allchannels:
        if channel.type[0] == 'category':
            if channel.name == instancename:
                return channel


async def find_welcome_channel():
    # define channel to send welcome message in
    allchannels = client.get_guild().channels

    for channel in allchannels:
        if channel.type[0] == 'text':
            if channel.name == 'welcome':
                return channel

@client.event
async def on_member_join(member):
    print(f'{member} has joined in Discord!')
    #channel = await find_welcome_channel()
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    membername = member.name
    await channel.send(
        "Hello, " + membername + "! Welcome to " + BotName + "! Type !help to see a list of commands you can tell me to do. Good luck on your quests!"
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #Gives help message with all available commands
    if message.content.startswith(prefix + 'help'):
        embedded_message = await help()
        await message.channel.send(embed = embedded_message)

    # Create Categories and starting channel(s) automatically
    if message.content.startswith(prefix + 'initiate'):
        thisguild = message.guild
        await initiate_questcompanion(thisguild)

    # Archive active challenge by moving the channel to archive category
    if message.content.startswith(prefix + 'archive quest'):
        await archive_challenge(message)

    # Undo archiving of a challenge by moving the channel to active category
    if message.content.startswith(prefix + 'unarchive quest'):
        await unarchive_challenge(message)

    #create a challenge
    if message.content.startswith(prefix + 'create'):
        messagetext = message.content
        message_elements = messagetext.split(' ', maxsplit = 1)
        channelName = message_elements[1]
        await create(message, channelName)

    #delete a quest
    if message.content.startswith(prefix + 'delete quest channel'):
        await delete_channel(message)

    if message.content.startswith(prefix + 'hello'):
        await message.channel.send("Hey " + str(message.author))

    if message.content.startswith(prefix + 'image'):
        await message.channel.send(file=discord.File(random.choice(images)))

    if message.content.startswith(prefix + 'thanks'):
        emoji = '\N{THUMBS UP SIGN}'
        # or '\U0001f44d' or '👍'
        await message.add_reaction(emoji)

    if message.content.startswith(prefix + 'inspire me'):
        await get_quote(message)

    if message.content.startswith(prefix + 'who'):
        await get_list_of_users_in_quest(message)

    if message.content.startswith(prefix + 'remindat'):
        messagetext = message.content
        await message.channel.send("Reminder is set")
        message_elements = messagetext.split(' ',maxsplit=2)
        scheduled_time = message_elements[1]
        if(len(message_elements)>2):
            reminder_msg = message_elements[2]
        else:
            reminder_msg = "Reminder Alert: Have a good day"
        await set_reminder(message,scheduled_time,reminder_msg)

@client.event
async def on_reaction_add(reaction, user):
    #dont respond to bots
    if user.bot == True:
        return
    originalmessageID = reaction.message.id
    originalmessageChannel = reaction.message.channel
    originalmessageAuthorName = reaction.message.author.name
    reactionemoji = reaction.emoji

    if reaction.message.content.startswith('!create'):
        if reactionemoji == '👍':
            reaction_to_create = "You have indicated you want to join a quest, " + user.name
            reaction_to_create_title = "Your request to join a Quest has been received"
            embed_reaction_tocreate = discord.Embed(title=reaction_to_create_title, description=reaction_to_create,
                                               color=errormessage_colour)
            await originalmessageChannel.send(embed =embed_reaction_tocreate)
            ID_questchannel = await add_member_to_quest(originalmessageID, user.name)


            reaction_inquest= "Welcome to this quest, " + user.name + ". " + BotName + " wishes you good luck on your journey to grow! Remember, the first step is to try!\nFor more inspiration, try !inspire me"
            reaction_inquesttitle = "Welcome to your new Quest"
            reaction_joinedquest = discord.Embed(title=reaction_inquesttitle, description=reaction_inquest,
                                               color=quotemessage_colour)
            reaction_joinedquest.set_image(url=welcome_to_quest_image)

            for channel in reaction.message.guild.channels:
                if channel.id == int(ID_questchannel):
                    postmessage_inchannel = channel
            await postmessage_inchannel.send(embed = reaction_joinedquest)
    else:
        return

##Functions
async def get_quote(message):
    global quotes
    # Get random quote
    random_n = random.randint(0, len(quotes))
    totalquote =  ''.join(quotes[random_n - 1])
    splitquote = totalquote.split('--')
    thisquote = splitquote[0]
    thisauthor = splitquote[1]
    random.shuffle(rainbow_colours)
    quote_colour = rainbow_colours[0]
    embed_quote = discord.Embed(title=str(thisquote), description=thisauthor, color=quote_colour)
    await message.channel.send(embed=embed_quote)


async def archive_challenge(message):
    thisguild = message.guild
    thischannel = message.channel
    requester_ID = message.author.id
    channelCreatorID = await get_creator_quest(str(thischannel.id))

    if thischannel.category.name != "Active-Quests":
        error_message_archive = "This is not an active quest, sorry!\nUse " + helpcommand + " for more information on how " + BotName + " functions!"
        error_message_archive_title = "Error: Cannot be archived"
        embed_errormessage = discord.Embed(title=error_message_archive_title, description=error_message_archive,
                                           color=errormessage_colour)
        await message.channel.send(embed=embed_errormessage)
    else:
        # check if they have the right to do this
        permission_to_do = 0
        if message.author.guild_permissions.manage_channels:
            permission_to_do = 1
        elif requester_ID == int(channelCreatorID):
            permission_to_do = 1

        #if permission, do thing
        if permission_to_do == 1:
            archive_category = await get_categoryinstance(thisguild, "Archived-Quests")
            await thischannel.edit(category=archive_category)
        else:
            error_message= "Sorry, you do not have the required permissions to adapt this quest. Only administrators and the creator of a quest channel can archive/unarchive/delete it. See" + helpcommand + " for more information on how " + BotName + " functions!"
            error_message_title = "Error: Not allowed"
            embed_errormessage = discord.Embed(title=error_message_title, description=error_message,
                                               color=errormessage_colour)
            await message.channel.send(embed=embed_errormessage)


async def unarchive_challenge(message):
    thisguild = message.guild
    thischannel = message.channel
    requester_ID = message.author.id
    channelCreatorID = await get_creator_quest(str(thischannel.id))

    if thischannel.category.name != "Archived-Quests":
        error_message_archive = "This is not an archived quest, sorry!\nUse " + helpcommand + " for more information on how " + BotName + " functions!"
        error_message_archive_title = "Error: Cannot be activated"
        embed_errormessage = discord.Embed(title=error_message_archive_title, description=error_message_archive,
                                           color=errormessage_colour)
        await message.channel.send(embed=embed_errormessage)
    else:
        # check if they have the right to do this
        permission_to_do = 0
        if message.author.guild_permissions.manage_channels:
            permission_to_do = 1
        elif requester_ID == int(channelCreatorID):
            permission_to_do = 1

        # if permission, do thing
        if permission_to_do == 1:
            archive_category = await get_categoryinstance(thisguild, "Active-Quests")
            await thischannel.edit(category=archive_category)
        else:
            error_message = "Sorry, you do not have the required permissions to adapt this quest. Only administrators and the creator of a quest channel can archive/unarchive/delete it. See" + helpcommand + " for more information on how " + BotName + " functions!"
            error_message_title = "Error: Not allowed"
            embed_errormessage = discord.Embed(title=error_message_title, description=error_message,
                                               color=errormessage_colour)
            await message.channel.send(embed=embed_errormessage)

#To create a channel
async def create(message, channelName):
    guild = message.guild

    #check if this is in the create channel
    if message.channel.name != "create-quests":
        error_message_createquest = "Please only use !create in the create-quests channel. This will allow other adventurers to read about your quest and join forces! Remember: together, we are stronger!"
        error_message_createquest_title = "Error: Incorrect channel!"
        embed_errormessage = discord.Embed(title=error_message_createquest_title, description=error_message_createquest,
                                           color=errormessage_colour)
        await message.channel.send(embed = embed_errormessage)
        return
    else:
        categoryinstance = await get_categoryinstance(guild, "Active-Quests")

        questchannel = await guild.create_text_channel(name='{}'.format(channelName), category= categoryinstance)

        guildID = str(guild.id)
        questchannelID = str(questchannel.id)
        creationMessageID = str(message.id)
        creatorID = str(message.author.id)
        creatorName = str(message.author)
        questdb_message = await add_new_quest(channelName, guildID, questchannelID, creationMessageID,creatorName, creatorID)

        mbed = discord.Embed(
            title='Success: ' + channelName + ' Quest Activated',
            description=questdb_message
        )
        await message.channel.send(embed=mbed)

        ##React to Original post
        emoji = '\N{THUMBS UP SIGN}'
        # or '\U0001f44d' or '👍'
        await message.add_reaction(emoji)

async def delete_channel(message):
    channelName = message.channel.name
    thischannel = message.channel
    requester_ID = message.author.id
    channelCreatorID = await get_creator_quest(str(thischannel.id))

    # check if they have the right to do this
    permission_to_do = 0
    if message.author.guild_permissions.manage_channels:
        permission_to_do = 1
    elif requester_ID == int(channelCreatorID):
        permission_to_do = 1

    # if permission, do thing
    if permission_to_do == 1:
        try:
            await message.channel.delete()
            success_delete = "Channel " + channelName + " deleted succesfully by " + str(message.author) + "!"
            success_delete_title = "Success: channel deleted"
            embed_deletemessage = discord.Embed(title=success_delete_title, description=success_delete,
                                               color=deletemessage_colour)
            for channel in message.guild.channels:
                if channel.name == "change-log":
                    postmessage_inchannel = channel
            await postmessage_inchannel.send(embed=embed_deletemessage)

        except:
            error_message_delete = "Sorry, something went wrong..."
            error_message_delete_title = "Error: Cannot be deleted"
            embed_errormessage = discord.Embed(title=error_message_delete_title, description=error_message_delete,
                                               color=errormessage_colour)
            await message.channel.send(embed=embed_errormessage)
    else:
        error_message_delete = "Sorry, you do not have permission to do that. Please contact an administrator!"
        error_message_delete_title = "Error: Cannot be deleted"
        embed_errormessage = discord.Embed(title=error_message_delete_title, description=error_message_delete,
                                           color=errormessage_colour)
        await message.channel.send(embed=embed_errormessage)


async def get_list_of_users_in_quest(message):
    thischannel = message.channel
    if thischannel.category.name not in ["Archived-Quests", "Active-Quests"]:
        error_message_title = "Error: Not a Quest!"
        error_message = "This command only works in quest channels in the Active and Archived Quest Categories! Use !help to receive more information on how to use this bot."
        error_message_embed = discord.Embed(title=error_message_title, description=error_message,
                                           color=errormessage_colour)
        await message.channel.send(embed=error_message_embed)
    else:
        channelID = message.channel.id
        listofusers = await get_joinedusers_quest(channelID)
        listusers = json.loads(listofusers)
        list_ofwho_message = ', '.join(listusers)
        list_ofwho_message_title = "List of Adventurers in this Quest"
        list_ofwho_message_embed = discord.Embed(title=list_ofwho_message_title, description=list_ofwho_message,
                                           color=quotemessage_colour)
        await message.channel.send(embed=list_ofwho_message_embed)


async def help():
    help_title = "Quest Companion Help"
    helpmessage = "Welcome to " + BotName + "! You can ask me:\n !inspire me -- for an inspiring quote \n !image --for an image\n 'React with thumbs up to join a quest' \n!create [quest name] --available in the create-quests channel, it allows anyone to create an active quest channel\n !archive quest --to archive a quest\n !unarchive quest --to unarchive a quest\n  !delete quest channel --to delete the quest channel\n !who --to list users who have joined a quest \n!help -- to list all the commands\n'Note: The archive, unarchive and delete commands are accessble for the creator of the quest and admins only'\n"
    helpmessage_embed = discord.Embed(title=help_title, description=helpmessage,
                                             color=quotemessage_colour)
    return helpmessage_embed

##Reminder setter
async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(dt, coro):
    await wait_until(dt)
    return await coro


async def remind(message, scheduled_msg):
    await message.channel.send("REMINDER: " + scheduled_msg)

async def set_reminder(message, scheduled_time, reminder_msg):
    loop = asyncio.get_event_loop()
    loop.create_task(run_at(datetime.datetime.strptime(scheduled_time, '%Y-%m-%d,%H:%M'),
                            remind(message, reminder_msg)))
    loop.run_forever()





##Database code
import sqlite3
from sqlite3 import Error

path = 'C:\\Users\\PEAQ\\Documents\\PearlHacks\\questcompanion_database.db'
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


conn = create_connection('C:\\Users\\PEAQ\\Documents\\PearlHacks\\questcompanion_database.db') # saves the database to disk so it persists across restarts
db_cursor = conn.cursor()
async def add_new_quest(current_quest_name, guildID, channelID, creationID, creatorName, creatorID):
    #check if channel name is unique
    quest_exists_query = 'SELECT QuestName FROM Quests WHERE QuestName = ' + "'" + current_quest_name + "'"
    exists = db_cursor.execute(quest_exists_query)
    if exists.fetchone():
        #error message for user
        error_message = "This quest already exists. To join it,  click the thumbs up reaction on the original message to join "+ current_quest_name
        return error_message
    #print(exists)
    #try to add quest to channel
    try:
        joinedusersList = json.dumps([creatorName])
        add_quest_query = 'INSERT INTO Quests(Guild, Channel, CreationMessage, QuestName, CreatorID, CreatorMember, JoinedMembers) VALUES (' + "'" +guildID+ "', '" + channelID+ "', '" + creationID+ "','" + current_quest_name + "','" + creatorID + "','" + creatorName + "','" + joinedusersList + "'"+ ')'
        db_cursor.execute(add_quest_query)
        conn.commit()
        success_message = "The Quest was successfully logged. All other adventurers, to join this quest, please click the thumbs up reaction on the original message and " +BotName + " will add your name to the " + current_quest_name +" channel!"
        return success_message
    except Error as e:
        print(f"The error '{e}' occurred")
        #error message for user
        error_message = "Something went wrong, please try again in a bit or contact the administrator of the server. You can show them this error message: " + str(e) +"."
        return error_message


async def add_member_to_quest(creationmessageID, joiningMember):
    #find quest
    quest_exists_query = 'SELECT JoinedMembers FROM Quests WHERE CreationMessage = ' + "'" + str(creationmessageID) + "'"
    exists = db_cursor.execute(quest_exists_query)
    content =  exists.fetchone()
    if content is None:
        return 0
    else:
        current_joinedusers = json.loads(content[0])
        current_joinedusers.append(joiningMember)

        #update users
        listofusers = json.dumps(current_joinedusers)

        update_listofjoinedmembers_query = "UPDATE Quests SET JoinedMembers = '"+ listofusers + "'"+ ' WHERE CreationMessage = ' + "'" + str(creationmessageID) + "'"
        print(update_listofjoinedmembers_query)
        db_cursor.execute(update_listofjoinedmembers_query)
        conn.commit()
        #get channel id to send welcome message in
        channel_of_quest_query = 'SELECT Channel FROM Quests WHERE CreationMessage = ' + "'" + str(
            creationmessageID) + "'"
        channel_of_quest = db_cursor.execute(channel_of_quest_query)
        content = channel_of_quest.fetchone()
        return content[0]


async def get_creator_quest(channelID):
    # get channel id to send welcome message in
    channel_of_quest_query = 'SELECT CreatorID FROM Quests WHERE Channel = ' + "'" + str(
        channelID) + "'"
    channel_of_quest = db_cursor.execute(channel_of_quest_query)
    content = channel_of_quest.fetchone()
    return content[0]

async def get_joinedusers_quest(channelID):
    # get channel id to send welcome message in
    channel_of_quest_query = 'SELECT JoinedMembers FROM Quests WHERE Channel = ' + "'" + str(
        channelID) + "'"
    channel_of_quest = db_cursor.execute(channel_of_quest_query)
    content = channel_of_quest.fetchone()
    return content[0]



##run bot
client.run(bot_token)