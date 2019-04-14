import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import asyncio as a
import sqlite3 as sql

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
