import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext.commands.cooldown import BucketType
from discord.ext import commands as c
import os
from random import randint
import asyncio as a
import sqlite3 as sql
import requests
import re

class MyHelpCommand(c.MinimalHelpCommand):
	def get_command_signature(self, command):
		return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

class Miscellaneous(c.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command
	
	@c.group(invoke_without_command=True,name='scratch')
	async def scratch(self,ctx,user:str):
		messages = self.messages(user)
		followers = self.followers(user)
		message = [f'**{user}**',f'**Messages:** {messages}',f'**Followers:** {followers}']
		em = d.Embed(title=message[0],description=f'{message[1]}\n{message[2]}')
		await ctx.send(embed=em)
	
	def messages(self,user):
		messages = requests.get('https://api.scratch.mit.edu/users/{}/messages/count'.format(user))
		self.messages = messages.json()['count']
		return f'{self.messages} messages on [scratch](https://scratch.mit.edu)'
	
	def followers(self,user):
		followers = int(re.search(r'Followers \(([0-9]+)\)', requests.get(f'https://scratch.mit.edu/users/{user}/followers').text, re.I).group(1))
		if user == 'griffpatch' or user == 'Will_Wam' or user == 'WazzoTV':
			until = 100000 - followers
			return f'{followers} on [scratch](https://scratch.mit.edu/users/{user}/followers)\n{until} more until 100,000'
		else:
			return f'{followers} on [scratch](https://scratch.mit.edu/users/{user}/followers)'

	@c.guild_only()
	@c.command(name='leaderboard',aliases=['lb'])
	async def leaderboard(self,ctx):
		"""Leaderboard of guild"""
		lb = {}
		self.bot.conn.commit()
		self.bot.crsr.execute('SELECT user_id , xp FROM users WHERE guild_id=?', (ctx.guild.id,))
		users = self.bot.crsr.fetchall() # array of users
		for i in range(9):
			high = 0
			for user in users:
				user[1] # that users xp
				user[0] # the id
				if user[1] > high:
					high = user[1]
					high_user = ctx.guild.get_member(user[0])
					high_id = user[0]
			if high_user.display_name not in lb:
				lb[high_user.display_name] = high
			try:
				index = users.index((high_id,high))
				del users[index]
			except ValueError:
				pass
		count = 1
		message = ''
		for key in lb:
			message += f'{count}. {key} - {lb[key]}xp\n'
			count += 1
		await ctx.send(f'```{message}```')

	@c.cooldown(1,600,BucketType.user)
	@c.command(name='work',hidden=True)
	async def work(self,ctx):
		self.bot.conn.commit()
		self.bot.crsr.execute(' \
			SELECT xp FROM users WHERE user_id=? AND guild_id=? \
		',(ctx.author.id,ctx.guild.id))
		xp = self.bot.crsr.fetchone()[0]
		if ctx.author.id == 499400512559382538:
			work = randint(50,100)
		else:
			work = randint(30,70)
		self.bot.crsr.execute('UPDATE users SET xp=? WHERE user_id=? AND guild_id=?',((xp + work),ctx.author.id,ctx.guild.id))
		self.bot.conn.commit()
		await ctx.send(f'You earned {work} xp')

def setup(bot):
	bot.add_cog(Miscellaneous(bot))
