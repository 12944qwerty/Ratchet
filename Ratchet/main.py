import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import jishaku

token = os.environ.get('TOKEN')

client = Bot(command_prefix='?R ')

cogs = ['Bot','Moderation','ID','Games','Miscellaneous','jishaku']

@client.event
async def on_ready():
	for cog in cogs:
		client.load_extension(cog)
	await client.change_presence(activity=d.Activity(name='?R help',type='3'))
	print('Logged in as')
	print('{0.user}'.format(client))
	print('Serving', end=' ')
	print('{} server(s)'.format(len(client.guilds)))

try:
    client.loop.run_until_complete(client.start(token))
except KeyboardInterrupt:
    client.loop.run_until_complete(client.logout())
finally:
    client.loop.close()