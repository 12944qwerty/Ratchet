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
	async def scratch(self,ctx,user=None):
		prefix = '&'
		message = ['Hi! This is a small command set where you can look for: ```',f'{prefix}scratch [messages|messagecount] <user>',f'{prefix}scratch followers <user>```']
		await ctx.send('\n'.join(message))
	
	@scratch.command(name='messagecount',aliases=['messages'])
	async def messagecount(self,ctx,user=None):
		if user == None:
			user = ctx.author.display_name
		try:
			messages = requests.get('https://api.scratch.mit.edu/users/{}/messages/count'.format(user))
			self.messages = messages.json()['count']
			em = d.Embed(title=f'{user}',description=f'{self.messages} messages on [scratch](https://scratch.mit.edu)')
			await ctx.send(embed=em)
		except KeyError:
			await ctx.send('This user could not be found. :(')
	
	@scratch.command(name='followers')
	async def followers(self,ctx,user=None):
		"""get the followers the user has"""
		if user == None:
			user = ctx.author.display_name
		
		try:
			followers = int(re.search(r'Followers \(([0-9]+)\)', requests.get(f'https://scratch.mit.edu/users/{user}/followers').text, re.I).group(1))
			if user == 'griffpatch' or user == 'Will_Wam' or user == 'WazzoTV':
				until = 100000 - followers
				em = d.Embed(title=f'{user}',description=f'{followers} on [scratch](https://scratch.mit.edu/users/{user}/followers)\n{until} more until 100,000')
			else:
				em = d.Embed(title=f'{user}',description=f'{followers} on [scratch](https://scratch.mit.edu/users/{user}/followers)')
			await ctx.send(embed=em)
		except AttributeError:
			await ctx.send('This user could not be')

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
