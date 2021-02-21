import re
import os
import discord
import logging
import pandas as pd
import requests
import json
from stanfordcorenlp import StanfordCoreNLP
from discord.ext import tasks

logging.basicConfig(level=logging.INFO)

BASE_URL = "http://09f5a8030481.ngrok.io"
LEADERBOARD_URL = "https://google.com"

client = discord.Client()
guild = discord.Guild
print(discord.version_info)

active = False
firstRun = True


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('_scan help'))


def is_command(message):
    if len(message.content) == 0:
        return False
    elif message.content.split()[0] == '_scan':
        return True
    else:
        return False


@tasks.loop(seconds=10)
async def get_answers(channel):
    answers = json.loads(requests.get(
        f"{BASE_URL}/api/data?type=answers").text)
    for answer in answers:
        # Get the message ID
        # Check the chat history to see if this message has any reactions
        message_id = answer['messageId']
        message = await channel.fetch_message(message_id)
        reactions = message.reactions
        reactionUsers = []
        for reaction in reactions:
            reactionUsers.append(await reaction.users().flatten())

        uniqueUsers = []
        for reactionList in reactionUsers:
            for user in reactionList:
                if user not in uniqueUsers:
                    uniqueUsers.append(str(user.id))

        for userId in uniqueUsers:
            if userId == str(message.author.id):
                uniqueUsers.remove(userId)

        answer["reactedBy"] = uniqueUsers
        requests.post(f"{BASE_URL}/api/data", json=answer)


async def get_data(channel):
    msg = (await channel.history(limit=1).flatten())[0]
    if msg.author != client.user:
        if not is_command(msg):
            response = requests.get(
                f"{BASE_URL}/api/index?sentence=" + msg.content)
            isQuestion = json.loads(response.text)['value']
            print(isQuestion)

            isAnswer = False
            userid = ""
            reference = ""
            if (msg.reference != None):
                reference = msg.reference.message_id
                isAnswer = True
            elif (msg.content.find("<@") >= 0):
                match = re.search("(?<=\<@)(.*)(?=\>)", msg.content)
                if (match):
                    userid = match.groups()[0]
                    if (userid[0] == '&'):
                        return

                    if (userid[0] == '!'):
                        userid = userid[1:]

                    # Gets if the tagged user asked a question
                    q_response = json.loads(requests.get(
                        f"{BASE_URL}/api/data/query?user=" + userid).text)
                    if (q_response['value']):
                        reference = q_response['messageId']
                        isAnswer = True

            if (not isQuestion and not isAnswer):
                return

            data = {
                "type": 1 if isAnswer else 0,
                "content": str(msg.content),
                "messageId": str(msg.id),
                "refersTo": str(reference),
                "reactedBy": [],
                "sender": str(msg.author.id),
                "sent-at": str(msg.created_at)
            }

            requests.post(f"{BASE_URL}/api/data", json=data)


@client.event
async def on_message(message):
    global active
    global firstRun

    if (active):
        if len(message.channel_mentions) > 0:
            channel = message.channel_mentions[0]
        else:
            channel = message.channel

        if message.author != client.user:
            await get_data(channel)

    # TODO: Award for reactions
    # On _scan, create recurring job to periodically get all answers on backend and update them
    # Get all answers from backend
    # Loop through all answers and find message IDs
        # Check if message has been reacted to
        # PUT to backend to update answers and reactions
        # (On backend) Award points accordingly

    # We don't want an api call to increase points because that's insecure and people can cheat
    # We want server to update automatically

    if message.author == client.user:
        return
    elif message.content.startswith('_'):

        print("This is running")
        cmd = message.content.split()[0].replace("_", "")
        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

        # Bot Commands
        if cmd == 'stop':
            active = False

        if cmd == 'leaderboard':
            active = False
            response = json.loads(requests.get(
                f"{BASE_URL}/api/leaderboard").text)

            desc = f"Full leaderboard: {LEADERBOARD_URL}"
            for i in range(3):
                desc += f"\n{i+1}. {response[i]['firstname']} {response[i]['lastname']}: {response[i]['points']}"

            msg = discord.Embed(title="Leaderboard",
                                description=desc,
                                colour=0x1a7794)

            await message.channel.send(embed=msg)
            active = True

        if cmd == 'register':
            active = False
            parameters = message.content.split(' ')[1:]
            if len(parameters) <= 1:
                msg = discord.Embed(title="Error",
                                    description=f"Could not register user - missing full name",
                                    colour=0x1a7794)
                await message.channel.send(embed=msg)
                active = True
                return
            first_name = parameters[0]
            last_name = parameters[1]

            requests.post(f"{BASE_URL}/api/users", json={"firstname": first_name,
                                                         "lastname": last_name,
                                                         "discordid": str(message.author.id)})
            msg = discord.Embed(title="Registered user",
                                description=f"Successfully registered user {first_name} {last_name}",
                                colour=0x1a7794)
            await message.channel.send(embed=msg)

            active = True

        if cmd == 'scan':
            if (firstRun):
                get_answers.start(message.channel)

            firstRun = False
            active = True

            msg = discord.Embed(title="Scan Start",
                                description=f"Beginning scan in {message.channel}",
                                colour=0x1a7794)
            await message.channel.send(embed=msg)

            # data = pd.DataFrame(columns=['content', 'time'])

            # Acquiring the channel via the bot command

            """
            # Aquiring the number of messages to be scraped via the bot command
            if (len(message.content.split()) > 1 and len(message.channel_mentions) == 0) or len(message.content.split()) > 2:
                for parameter in parameters:
                    if parameter == "help":
                        answer = discord.Embed(title="Command Format",
                                               description=`_scan <channel> <number_of_messages>`\n\n`<channel>` : **the channel you wish to scan**\n`<number_of_messages>` : **the number of messages you wish to scan**\n\n*The order of the parameters does not matter.*,
                                               colour=0x1a7794) 
                        await message.channel.send(embed=answer)
                        return
                    elif parameter[0] != "<": # Channels are enveloped by "<>" as strings
                        limit = int(parameter)
            else:
                limit = 10 

            
            answer = discord.Embed(title="Creating your Message History Dataframe",
                                   description="Please Wait. The data will be sent to you privately once it's finished.",
                                   colour=0x1a7794) 

            await message.channel.send(embed=answer)
            """

            # Turning the pandas dataframe into a .csv file and sending it to the user

            # file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv" # Determining file name and location
            # data.to_csv(file_location) # Saving the file as a .csv via pandas

            # answer = discord.Embed(title="Here is your .CSV File",
            # description=f"""It might have taken a while, but here is what you asked for.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{limit}**""",
            # colour=0x1a7794)

            # await message.author.send(embed=answer)
            # await message.author.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
            # os.remove(file_location) # Deleting the file


file = open('token.txt', 'r')
client.run(file.read())
