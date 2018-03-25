import discord
import asyncio
from dreamfarm.bot.embed import EmbedBuilder

# List of bot commands supplied by the user
async def commands(client, message):
    author = message.author.name
    user_id = message.author.id

    if message.content.startswith('$corn'):
        builder = EmbedBuilder()
        embed = await builder.build(author + '\'s Farm', 'Current plot', user_id, [])
        await client.send_message(message.channel, embed=embed)
