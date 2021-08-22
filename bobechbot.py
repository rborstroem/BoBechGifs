import discord
import os
import random
import requests
import json
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
gif_ids = []

token = os.getenv('DISCORD_TOKEN')
key = os.getenv('TENOR_KEY')


@client.event
async def on_ready():
    global gif_ids
    f = open('ids.txt', "r")
    gif_ids = f.read().split(",")
    f.close()
    print('We have logged in as {0.user}'.format(client))
        
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('/random_bo'):
        id = random.choice(gif_ids)
        response = requests.get('https://g.tenor.com/v1/gifs?media_filter=minimal&key='+key+'&ids='+id).json()
        url = response['results'][0]['url']
        print(client.user, "requested", url)
        await message.channel.send(url)
    
client.run(token)