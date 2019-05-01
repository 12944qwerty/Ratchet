import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import sqlite3 as sql

conn = sql.connect('Ratchet.db')
crsr = conn.cursor()

def get_prefix(bot,msg):
	try:
		crsr.execute('SELECT prefix FROM guilds WHERE guild_id=?',(msg.guild.id,))
		idk = crsr.fetchone()
		if idk is None or idk[0] is None:
			return '\\'
		return (idk[0], '\\')
		crsr.commit()
	except AttributeError:
		return ['&','\\']

client = Bot(command_prefix=get_prefix,activity=d.Activity(type=d.ActivityType.watching, name='\\help'))

client.crsr = crsr
client.conn = conn

@client.event
async def on_ready():
	for cog in cogs:
		client.load_extension(cog)
	try:
		crsr.execute('DROP TABLE guilds;')
		conn.commit
	except sql.OperationalError:
		pass
	try:
		crsr.execute('DROP TABLE users;')
		conn.commit
	except sql.OperationalError:
		pass
	crsr.execute('CREATE TABLE guilds ( \
		guild_id UNSIGNED BIG integer NOT NULL, \
		prefix string \
	);')
	conn.commit
	for guild in client.guilds:
		crsr.execute('INSERT INTO guilds (guild_id, prefix) VALUES (?, ?)', (guild.id, '\\'))
		conn.commit
	crsr.execute('UPDATE guilds SET prefix=? WHERE guild_id=?',('&',550722337050198036))
	crsr.execute('CREATE TABLE users ( \
		guild_id UNSIGNED BIG INT, \
		user_id UNSIGNED BIG INT, \
		xp INT \
	);')
	conn.commit()
	guilds = [361233849847644160,550722337050198036, 562633473387397134]
	for guild in client.guilds:
		if not guild.id in guilds:
			await guild.leave()
	print('Logged in as')
	print('{0.user}'.format(client))
	print('Serving', end=' ')
	print('{} server(s)'.format(len(client.guilds)))

cogs = ['Bot','Moderation','Miscellaneous','Games','errorhandler','owner']

@client.event
async def on_message(message):
	if not message.author.bot:
		try:
			crsr.execute('SELECT xp FROM users WHERE guild_id=? AND user_id=?', (message.guild.id, message.author.id))
			idk = crsr.fetchone()
			#await message.channel.send(idk)
			if idk is None: #user not ranked
				crsr.execute('INSERT INTO users (guild_id, user_id, xp) VALUES (?, ?, ?)', (message.guild.id, message.author.id, 1))
			else:
				crsr.execute('UPDATE users SET xp=? WHERE guild_id=? AND user_id=?', ((idk[0] or 0) + 1, message.guild.id, message.author.id))
			conn.commit()
		except AttributeError:
			pass
	await client.process_commands(message)

async def activity(*args):
	print(args)
	while not client.is_closed():
		for arg in args:
			await client.change_presence(activity=d.Activity(type=d.ActivityType.watching, name=arg))
			await a.sleep(5)

with open('login.txt') as f:
    token = f.readline().strip()

try:
	client.loop.run_until_complete(client.start(token))
except KeyboardInterrupt:
	conn.close()
	client.loop.run_until_complete(client.logout())
finally:
	client.loop.close()
	conn.close()
