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
	
	async def get_admin(self,ctx):
		for member in ctx.guild:
			if ctx.channel.permissions_for(member).ban_members and member.status == 'online' or member.status == 'idle':
				self.admin = member
				break

	@c.guild_only()
	@bot_has_permissions(ban_members=True)
	async def unban(self,ctx,user:d.Member,*,reason=None):
		self.get_admin(ctx)
		if ctx.channel.permissions_for(ctx.author).ban_members and ctx.channel.permissions_for(self.bot.user).ban_members:
			await user.unban(reason=reason)
		else:
			unban = await ctx.send('@everyone, {} has voted for {} to be unbanned. Reason, if any, {}'.format(ctx.author.mention,user.mention,str(reason)))
			DOUNBAN = '\U0001f6ab'
			NOUNBAN = '\U0001f607'
			unban.add_reaction(DOUNBAN)
			unban.add_reaction(NOUNBAN)
			time.sleep(3600.00)
			Yay = 0
			Nay = 0
			for reaction in unban.reactions:
				if reaction == DOUNBAN:
					Yay += 1
				else:
					Nay += 1
			if Yay > Nay:
				if ctx.channel.permissions_for(self.bot.user).ban_members:
					await ctx.send('@everyone, {} has been unbanned'.format(user.mention))
				else:
					await ctx.send('{}, {} has been voted to be unbanned'.format(self.admin.mention,user.mention))
				await user.unban(reason=reason)
			elif Yay < Nay:
				await ctx.send('@everyone, {} has been voted to stay banned'.format(user.mention))
			else:
				await ctx.send('@everyone, the vote against {} has been a tie. He will stay banned!'.format(user.mention))
	
	@c.guild_only()
	@bot_has_permissions(ban_members=True)
	@c.command(name='ban')
	async def ban(self,ctx,user:d.Member,reason=None):
		"""Ban someone in the server. Reason is default 'None'"""
		self.get_admin(ctx)
		
		if ctx.channel.permissions_for(ctx.author).ban_members and ctx.channel.permissions_for(self.bot.user).ban_members:
			await ctx.guild.ban(user,reason=reason)
			await ctx.send(f'<@everyone> {user.display_name} has been banned by {ctx.author.display_name}! :wave:')
		else:
			await ctx.send('{} has requested for {} to be banned - **{}**!'.format(ctx.author.display_name,user.display_name,reason))
			vote = await ctx.send('Please vote below! <@everyone>')
			DOBAN = '\U0001f6ab'
			NOBAN = '\U0001f607'
			await vote.add_reaction(DOBAN)
			await vote.add_reaction(NOBAN)
			time.sleep(1800.00)
			Yay = 0
			Nay = 0
			for reaction in vote.reactions:
				if reaction.emoji == DOBAN:
					Yay += 1
				if reaction.emoji == NOBAN:
					Nay += 1
			if Yay > Nay:
				if ctx.channel.permissions_for(self.bot.user).ban_members:
					await ctx.send(f'<@everyone> {user.display_name} has been voted to be banned! :wave:')
					await ctx.guild.ban(user,reason=reason)
				else:
					await ctx.send('{}, {} has been voted to be banned'.format(admin.mention,user.display_name))
			elif Nay < Yay:
				await ctx.send(f'<@everyone> {user.display_name} has been voted to not be banned! :laugh:')
			else:
				await ctx.send(f'<@everyone> The vote for {user.display_name} has been cancelled for a tie! :laugh:')
	
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

	@c.guild_only()
	@c.command(name='set_prefix',aliases=['change_prefix',])
	async def set_prefix(self,ctx,prefix:str):
		"""Sets prefix of guild!"""
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
		await ctx.send('Prefix has been reset to `?R `')

def setup(bot):
    bot.add_cog(Moderation(bot))
