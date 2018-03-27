import discord
import asyncio
import requests
import json
import logging
import os
from dreamfarm.bot.log import logger
from dreamfarm.bot.embed import EmbedBuilder

api_host = os.environ.get('API_HOST')

# List of bot commands supplied by the user
async def commands(client, message):
    author = message.author.name
    user_id = message.author.id

    if message.content.startswith('$start'):
        params = {
            'user_id': user_id,
            'user_name': author
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(api_host + '/register', data=json.dumps(params), headers=headers)

        if (response.status_code == 200):
            await client.send_message(message.channel, response.text)
        else:
            logger.warn('ERROR: register; user %s; %s %s', user_id, response.status_code, response.reason)
            return ''

    if message.content.startswith('$show'):
        builder = EmbedBuilder()
        embed = await builder.build(author + '\'s Farm', 'Current plot', user_id, [])
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('$corn'):
        builder = EmbedBuilder()
        embed = await builder.build(author + '\'s Farm', 'Current plot', user_id, [])
        await client.send_message(message.channel, embed=embed)
