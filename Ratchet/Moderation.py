import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import time

class Moderation(c.Cog):
	def __init__(self,client):
		self.bot = client
	
	@c.command(name='unban')
	@bot_has_permissions(ban_members=True)
	async def unban(self,ctx,user:d.Member,*,reason=None):
		if ctx.channel.permissions_for(ctx.author).ban_members:
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
				await ctx.send('@everyone, {} has been unbanned'.format(user.mention))
				await user.unban(reason=reason)
			elif Yay < Nay:
				await ctx.send('@everyone, {} has been voted to stay banned'.format(user.mention))
			else:
				await ctx.send('@everyone, the vote against {} has been a tie. He will stay banned!'.format(user.mention))
	
	@bot_has_permissions(manage_messages=True,ban_members=True,kick_members=True)
	@c.command(name='ban')
	async def ban(self,ctx,user:d.Member,purge_days:int=13,reason=None):
		"""Ban someone in the server. Optionally purge a max of 13 days of user's message. Reason is default 'None'"""
		for member in ctx.guild:
			if member.status == 'online' or member.status == 'idle' and ctx.channel.permissions_for(member).ban_members:
				banner = member
		
		if ctx.author != banner:
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
				await ctx.send(f'<@everyone> {user.display_name} has been voted to be banned! :wave:')
				await ctx.guild.ban(user,reason=reason,delete_message_days=purge_days)
			elif Nay < Yay:
				await ctx.send(f'<@everyone> {user.display_name} has been voted to not be banned! :laugh:')
			else:
				await ctx.send(f'<@everyone> The vote for {user.display_name} has been cancelled for a tie! :laugh:')
		else:
			await ctx.guild.ban(user,reason=reason,delete_message_days=purge_days)
			await ctx.send(f'<@everyone> {user.display_name} has been banned by {ctx.author}! :wave:')
	
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
		msg = await ctx.send(embed=d.Embed(title=('purge'),description=('purged {} messages'.format(len(deleted)))
		))
		time.sleep(2)
		await msg.delete()



def setup(bot):
    bot.add_cog(Moderation(bot))