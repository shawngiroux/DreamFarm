import discord

# List of bot commands supplied by the user
async def commands(client, message):
    if message.content == "f!help":
        await client.send_message(message.channel, 'I have no commands yet!')
