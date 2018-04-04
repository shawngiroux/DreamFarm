import asyncio
import binascii
import json
import logging
import os

import requests

import discord
from dreamfarm.bot.log import logger


api_host = os.environ.get('API_HOST')
remote_host = os.environ.get('REMOTE_HOST')

class EmbedBuilder:
    async def build(self, title, description, user_id, image_url, thumb_url=None, fields=[]):
        embed = discord.Embed(title=title, description=description, color=0x4c9265)

        if thumb_url is not None:
            embed.set_thumbnail(url=thumb_url)

        embed.set_image(url=image_url)

        for field in fields:
            embed.add_field(name=field['name'], value=field['value'], inline=False)

        return embed
