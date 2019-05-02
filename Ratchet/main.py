import discord as d
from discord_webhook import DiscordWebhook
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import sqlite3 as sql
import asyncio

conn = sql.connect('Ratchet.db')
crsr = conn.cursor()

class MyClient(Bot):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.griffpatch = self.loop.create_task(self.griffpatch())
		self.activity = self.loop.create_task(self.activity())
		
	async def on_ready(self):
		for cog in cogs:
			client.load_extension(cog)
		"""try:
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
		conn.commit()"""
		print('Logged in as')
		print('{0.user}'.format(client))
		print('Serving', end=' ')
		print('{} server(s)'.format(len(client.guilds)))
		
	async def on_message(self,message):
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
		
	async def griffpatch(self):
		while not self.bot.is_closed():
			followers = int(re.search(r'Followers \(([0-9]+)\)', requests.get('https://scratch.mit.edu/users/griffpatch/followers').text, re.I).group(1)) + 148
			griffpatch = DiscordWebhook(url='https://discordapp.com/api/webhooks/573277772458229798/k6G4O_O4inaVWKYtbK7PKyKDLP44mQ7Y-x7MR7J1FIS4KSBUJl3d8YDsGo7jpRdn_Y7u',content=str(followers)+' followers')
			griffpatch.execute()
			await asyncio.sleep(1800.0)
			
	async def activity(self):
		while not self.bot.is_closed():
			await client.change_presence(activity=d.Activity(type=d.ActivityType.watching, name='\\help'))
			await asyncio.sleep(5)
			await client.change_presence(activity=d.Activity(type=d.ActivityType.watching, name=f'{len(client.guilds)} servers'))
			await asyncio.sleep(5)

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

client = MyClient(command_prefix=get_prefix)

client.crsr = crsr
client.conn = conn

cogs = ['Bot','Moderation','Miscellaneous','Games','errorhandler','owner']

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
