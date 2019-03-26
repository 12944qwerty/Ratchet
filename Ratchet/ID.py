import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import asyncio as a

class ID(c.Cog):
	def __init__(self,client):
		self.bot = client

	@c.command(name='roleID')
	async def roleID(self,ctx,*,role=None):
		"""Get the ID of a role"""
		if role != None:
			await ctx.send('```{}```'.format(d.utils.get(ctx.guild.roles,name=role).id))
		else:
			await ctx.send('Please type in the name of the role!')

	
def setup(bot):
    bot.add_cog(ID(bot))