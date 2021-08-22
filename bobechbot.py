import discord
import os
import random
import requests
import json
from dotenv import load_dotenv
import mariadb
import sys

# Load env variables
load_dotenv()

# Get env variables
token = os.getenv('DISCORD_TOKEN')
key = os.getenv('TENOR_KEY')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')

# Initialize usage of database set to true
use_db = True

# Try to connect to database
# If errors occurs, set use_db to false
try: 
    conn = mariadb.connect(
        user=db_user,
        password=db_pass,
        host="127.0.0.1",
        port=3306,
        database="bobechgifs"
    )

    cur = conn.cursor()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    use_db = False

# Create discord bot client
client = discord.Client()

# Used for list of ids
gif_ids = []
gif_blacklist = [22077733]

# At start up, get ids (currently from txt-file)
# Should be from database at later point
@client.event
async def on_ready():
    global gif_ids
    f = open('ids.txt', "r")
    gif_ids = f.read().split(",")
    f.close()
    for element in gif_blacklist:
        if element in gif_ids:
            gif_ids.remove(element)
    print('We have logged in as {0.user}'.format(client))

# Command handling in discord 
@client.event
async def on_message(message):
    # If message was from the bot itself, ignore
    if message.author == client.user:
        return
    # Use random command
    if message.content.startswith('/bo_random '):
        id = random.choice(gif_ids)
        url = get_url(id)
        await message.channel.send(url)
    # Use mood command
    if message.content.startswith("/bo_mood"):
        # If database is not responding, don't allow this command
        if (not use_db):
            await message.channel.send("This command does not work at the moment.")
            return

        # Otherwise use command, check if argument (mood) is a correct mood
        try:
            mood_type = message.content[len("/bo_mood "):]
            id = get_id_from_mood(mood_type)
            url = get_url(id)
            await message.channel.send(url)
        except:
            await message.channel.send("Mood not found. Bo is not happy about that.")
            id = get_id_from_mood("angry")
            url = get_url(id)
            await message.channel.send(url)

# Given mood, use query to find all ids with this mood
# return a random id
def get_id_from_mood(mood_type):
    cur.execute("SELECT ID, MoodType FROM gifmood WHERE MoodType=?", (mood_type,))
    ids,_ = zip(*cur)
    id = random.choice(ids)
    return id

# Using found gif id, use tenor api 
# to get url for gif and return it
def get_url(id):
    response = requests.get('https://g.tenor.com/v1/gifs?media_filter=minimal&key='+key+'&ids='+str(id)).json()
    url = response['results'][0]['url']
    print(client.user, "requested", url)
    return url

# Run the bot! :D 
client.run(token)