import discord
import asyncio
import requests
import json
import logging
import os
import binascii
from dreamfarm.bot.log import logger
from dreamfarm.bot.embed import EmbedBuilder

api_host = os.environ.get('API_HOST')
remote_host = os.environ.get('REMOTE_HOST')

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

    if message.content.startswith('$farm'):
        url = remote_host + '/get-current-farm?duid=' + user_id + '&v=' + binascii.b2a_hex(os.urandom(15)).decode('utf-8')
        builder = EmbedBuilder()
        embed = await builder.build(
            author + '\'s :sparkles:**DREAM FARM**:sparkles:',
            ':moneybag: 24903\n:sunny: Sunny\n:calendar: Day 492, 13:37',
            user_id,
            url,
            'https://i.imgur.com/IDQwaUp.png',
            []
        )
        await client.send_message(message.channel, embed=embed)
