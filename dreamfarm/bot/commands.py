import json
import os
import re

import requests
from discord.ext import commands

from dreamfarm.bot.embed import EmbedBuilder
from dreamfarm.bot.log import logger


API_HOST = os.environ.get('API_HOST')
REMOTE_HOST = os.environ.get('REMOTE_HOST')

# List of bot commands supplied by the user
async def parse_commands(client, message):
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
        response = requests.post(API_HOST + '/register', data=json.dumps(params), headers=headers)

        if response.status_code == 200:
            await client.send_message(message.channel, response.text.format(message.author.mention))
        else:
            logger.warn('ERROR: register; user %s; %s %s', user_id, response.status_code, response.reason)
            return ''

    if message.content.startswith('$farm'):
        params = {
            'user_id': user_id
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(API_HOST + '/do-calculations', data=json.dumps(params), headers=headers)

        url = REMOTE_HOST + '/get-current-farm?duid=' + user_id
        builder = EmbedBuilder()

        if response.status_code == 200:
            data = json.loads(response.text)

            # TODO put data from the response in the message
            embed = await builder.build(
                '{}\'s :sparkles:**DREAM FARM**:sparkles:'.format(author),
                ':calendar: {}\n:moneybag: {}'.format(data['game_time'], data['money']),
                user_id,
                url
            )
        else:
            embed = await builder.build(
                '{}\'s :sparkles:**DREAM FARM**:sparkles:'.format(author),
                '',
                user_id,
                url
            )

        await client.send_message(message.channel, message.author.mention, embed=embed)

    if message.content.startswith(('$chop', '$rake')):
        m = re.search(r'\$([a-zA-Z]+)\s+([a-zA-Z][0-9]+)(:[a-zA-Z][0-9]+)?', message.content)

        if m is None:
            await client.send_message(message.channel, '{}, invalid command syntax! Type `$help` for information on commands.'.format(message.author.mention))
        else:
            params = {
                'user_id': user_id,
                'user_name': author,
                'action': m.group(1),
                'range_start': m.group(2)
            }

            if m.group(3) is not None:
                params['range_end'] = m.group(3)

            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(API_HOST + '/add-task', data=json.dumps(params), headers=headers)

            if response.status_code == 200:
                await client.send_message(message.channel, response.text.format(message.author.mention))
            else:
                logger.warn('ERROR: add-task; user %s; %s %s', user_id, response.status_code, response.reason)
                return ''
