import discord
import asyncio
from cogs.commands import commands

client = discord.Client()

@client.event
async def on_ready():
    print('Building the Dream Farm')
    print('-----------------------')
    # Set nickname in all servers
    for server in client.servers:
        try:
            await client.change_nickname(server.me, '✨Dream Farm✨')
        except Exception:
            print("Nickname exception in: " + server.name)

@client.event
async def on_message(message):
    if message.author != client.user:
        await commands(client, message)

client.run('token')
