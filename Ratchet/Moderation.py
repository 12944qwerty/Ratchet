import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import time
import sqlite3 as sql

class Moderation(c.Cog):
	def __init__(self,client):
		self.bot = client
	
	@c.guild_only()
	@c.command()
	@has_permissions(manage_messages=True, read_message_history=True)
	@bot_has_permissions(manage_messages=True, read_message_history=True)
	async def purge(self,ctx, limit: int = 100, user: d.Member = None, *, matches: str = None):
		"""Purge all messages, optionally from ``user``
		or contains ``matches``."""
		def check_msg(msg):
			if msg.id == ctx.message.id:
				return True
			if user is not None:
				if msg.author.id != user.id:
					return False
			if matches is not None:
				if matches not in msg.content:
					return False
			return True
		deleted = await ctx.channel.purge(limit=limit, check=check_msg)
		await ctx.send(embed=d.Embed(title=('purge'),description=('purged {} messages'.format(len(deleted)))
		),delete_after=2.0)

	"""@c.guild_only()
	@c.command(name='set_prefix',aliases=['change_prefix',])
	async def set_prefix(self,ctx,prefix:str):
		Sets prefix of guild!
		self.bot.crsr.execute('UPDATE guilds SET prefix=? WHERE guild_id=?',(prefix,ctx.guild.id))
		self.bot.conn.commit()
		self.bot.crsr.execute('SELECT prefix FROM guilds WHERE guild_id=?',(ctx.guild.id,))
		prefix = self.bot.crsr.fetchone()[0]
		await ctx.send(f'Prefix changed to {prefix}')
	
	@c.guild_only()
	@c.command(name='prefix',aliases=['pre'])
	async def prefix(self,ctx):
		pre = self.bot.crsr.execute('SELECT prefix \
			FROM guilds \
			WHERE guild_id=?', (ctx.guild.id,))
		await ctx.send(f'Prefix is currently {pre}')
	
	@c.guild_only()
	@c.command(name='reset_prefix')
	async def reset_prefix(self,ctx):
		self.bot.crsr.execute('UPDATE guilds SET prefix=? WHERE guild_id=?', ('?R ',ctx.guild.id))
		await ctx.send('Prefix has been reset to `?R `')"""

def setup(bot):
    bot.add_cog(Moderation(bot))
