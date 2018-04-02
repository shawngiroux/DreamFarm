import asyncio
import os

import discord
from dreamfarm.bot.commands import commands


client = discord.Client()
api_key = os.environ.get('DISCORD_API_KEY')
api_host = os.environ.get('API_HOST')

@client.event
async def on_ready():
    print('Building the Dream Farm')
    print('-----------------------')
    # Set nickname in all servers
    # for server in client.servers:
    #     try:
    #         await client.change_nickname(server.me, '✨𝐃𝐑𝐄𝐀𝐌 𝐅𝐀𝐑𝐌✨')
    #     except Exception:
    #         print("Nickname exception in: " + server.name)

@client.event
async def on_message(message):
    if message.author != client.user:
        await commands(client, message)

def run():
    client.run(api_key)
