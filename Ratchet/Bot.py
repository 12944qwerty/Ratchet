import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import datetime
from pendulum import instance as to_utc, timezone

class Bot(c.Cog):
	def __init__(self,client):
		self.bot = client

	@c.group(invoke_without_command=True,name='info',aliases=['desc','botinfo'])
	async def info(self,ctx):
		"""Sends desc of bot"""
		try:
			await ctx.send('I am Ratchet. A fun bot. To see a list of commands, type in \'\\helps\'.\n To report a bug, DM the owner. `12944qwerty#9317`')
			await ctx.send('Subcommands:\n - `\\info guilds`\n - `\\info status`\n - `\\info invite`\n - `\\info ping`\n - `\\info emojis`')
		except Exception as e:
			print(e)
	
	@info.command(name='guilds')
	async def guilds(self,ctx):
		for guild in self.bot.guilds:
			await ctx.send(f'{guild.name} - {guild.id}')
	
	@info.command(name='emojis')
	async def emojis(self,ctx):
		"""spits out the emojis that this bot is connected to"""
		emojis = ''
		for emoji in self.bot.emojis:
			emojis += '{}'.format(str(emoji))
		await ctx.send(emojis)
	
	@info.command(name='status', aliases=['use','usage'])
	async def status(self,ctx):
		await ctx.send('__**_Status_**__ <:online:512174327899226123>')
		await ctx.send('Server Count: {}'.format(len(self.bot.guilds)))
		user = 0
		for guild in self.bot.guilds:
			for member in guild.members:
				user += 1
		await ctx.send('Serving {} users'.format(user))

	@c.command(name='play', aliases=['watch','listen'])
	@c.is_owner()
	async def play(self,ctx,media_title: str):
		"""Update my presence."""
		p_types = {'play': 0, 'listen': 2, 'watch': 3}
		my_media = d.Activity(name=media_title, type=p_types[ctx.invoked_with])
		await self.bot.change_presence(activity=my_media)

	@info.command(name='inv', aliases=['invite_link','invite'])
	async def inv(self,ctx):
		Want this bot on your server?
		await ctx.send('Hi! If you would like me to be on your server, please use this link:\n <https://discordapp.com/api/oauth2/authorize?client_id=549642567718010880&permissions=2146958839&scope=bot>')
	
	@c.guild_only()
	@c.command(name='leave')
	async def leave(self,ctx):
		"""LEaves the Guild. ADMIN ONLY"""
		if ctx.author.id == 499400512559382538 or ctx.author.permissions.administrator:
			await ctx.send('Awww, why don\'t you want me???')
			await ctx.guild.leave()

	@c.command(name='stop')
	async def stop(self,ctx):
		"""Stop the bot. ONLY ADMINS CAN DO SO (and owner)"""
		if ctx.author.id == 499400512559382538:
			msg = await ctx.send('Stopping.......')
			await msg.edit(content='Stopped!')
			print('{} stopped this bot. - {}'.format(ctx.author.display_name,ctx.guild.name))
			conn.commit()
			conn.close()
			self.bot.loop.run_until_complete(self.bot.logout())
		else:
			await ctx.send('You are not my owner.... OR an admin!!!!')

	@c.command(name='report',aliases=['bug'])
	async def report(self,ctx):
		await ctx.send('Please report any bugs or glitches with this bot to 12944qwerty#9317. :D\nIf you have any suggestions, feel free to talk there too.')

	@info.command(name='ping')
	async def ping(self,ctx):
		"""Tests for reply speed"""
		milis = datetime.datetime.now().timestamp()
		try:
			em = d.Embed(title='Pong!:ping_pong:')
			em.add_field(name='Latency',value=f'{round(self.bot.latency * 1000,1)}ms')
			milis1 = datetime.datetime.now().timestamp()
			em.add_field(name='Heartbeat:heartbeat:',value=f'{round((milis1-milis) * 1000000,2)}ms')
			em.set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
			msg = await ctx.send(embed=em)
			milis2 = datetime.datetime.now().timestamp()
			em.add_field(name='Edit',value=f'{round((milis2-milis)*1000,1)}ms')
			await msg.edit(embed=em)
		except Exception as e:
			print(e)

def setup(bot):
    bot.add_cog(Bot(bot))
