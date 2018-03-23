import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Activating the dream farm')
    print('-------------------------')

@client.event
async def on_message(message):
    if message.content == "!ping":
        await client.send_message(message.channel, 'pong!')

client.run('token')
