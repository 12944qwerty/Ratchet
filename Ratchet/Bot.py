import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import datetime

class Bot(c.Cog):
	def __init__(self,client):
		self.bot = client
	
	@c.command(name='status', aliases=['use','usage'])
	async def status(self,ctx):
		em = d.Embed(title='__**_Status_**__')
		em.add_field(name='Server Count:',value=len(self.bot.guilds),inline=False)
		user = 0
		for guild in self.bot.guilds:
			for member in guild.members:
				user += 1
		em.add_field(name='Serving # of users: ',value=user,inline=False)
		await ctx.send(embed=em)

	@c.command(name='play', aliases=['watch','listen'])
	@c.is_owner()
	async def play(self,ctx,media_title: str):
		"""Update my presence."""
		p_types = {'play': 0, 'listen': 2, 'watch': 3}
		my_media = d.Activity(name=media_title, type=p_types[ctx.invoked_with])
		await self.bot.change_presence(activity=my_media)


	@c.command(name='inv', aliases=['invite_link','invite'])
	async def inv(self,ctx):
		"""Want this bot on your server?"""
		await ctx.send('Hi! If you would like me to be on your server, please use this link:\n <https://discordapp.com/api/oauth2/authorize?client_id=549642567718010880&permissions=2146958839&scope=bot>')
	
	@c.command(name='stop')
	@c.is_owner()
	async def stop(self,ctx):
		"""Stop the bot. ONLY OWNER CAN DO SO"""
		try:
			msg = await ctx.send('Stopping.......')
			await msg.edit(content='Stopped!')
			self.bot.loop.run_until_complete(self.bot.logout())
		except Exception as e:
			print(e)
			
	@c.command(name='desc')
	async def desc(self,ctx):
		"""Sends desc of bot"""
		try:	
			await ctx.send('I am Ratchet. A fun bot. To see a list of commands, type in \'?R helps\'.\n To report a bug, DM the owner. @12944qwerty#9317')
		except Exception as e:
			print(e)

	@c.command(name='report',aliases=['bug'])
	async def report(self,ctx,*,bug:str):
		msg = await ctx.send('Your message is being logged.... This is going to take a while')
		log = open('bugs.txt','a')
		log.write('\n\n{0.message.created_at} - {1} - {0.author} in {0.guild}'.format(ctx,bug))
		await msg.edit(content='I have logged your bug!')

	@c.command(name='ping')
	async def ping(self,ctx):
		"""Tests for reply speed"""
		milis = datetime.datetime.now().timestamp()
		try:
			em = d.Embed(title='Pong!:ping_pong:')
			em.add_field(name='Latency',value=f'{round(self.bot.latency * 1000,1)}ms')
			milis1 = datetime.datetime.now().timestamp()
			em.add_field(name='Heartbeat:heartbeat:',value=f'{round((milis1-milis) * 1000,1)}ms')
			em.set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
			msg = await ctx.send(embed=em)
			milis2 = datetime.datetime.now().timestamp()
			em.add_field(name='Edit',value=f'{round((milis2-milis)*1000,1)}ms')
			await msg.edit(embed=em)
		except Exception as e:
			print(e)

	@c.command(name='hi',aliases=['hello','test'])
	async def hi(self,ctx):
		"""Test if bot is working"""

		try:
			await ctx.send('Hello {}!'.format(ctx.author.display_name))
		except Exception as e:
			print(e)

def setup(bot):
    bot.add_cog(Bot(bot))