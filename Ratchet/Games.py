import discord as d
import sys, traceback
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import os
from random import randint
import asyncio as a

class Games(c.Cog):
	def __init__(self,bot):
		self.bot = bot
	
	@bot_has_permissions(manage_messages=True)
	@c.command(name='tic-tac-toe',aliases=['tic tac toe'])
	async def tictactoe(self,ctx):
		"""Play TicTacToe!"""
		em = d.Embed(title='Tic-Tac-Toe')
		em.add_field(name='P1 - :regional_indicator_x:',value=ctx.author.display_name)
		em.add_field(name='P2 - :regional_indicator_o:',value='React to be P2')
		game = await ctx.send(embed=em)
		await game.add_reaction('\U0001f579')
		def check(reaction, user):
			return user != ctx.author and (str(reaction.emoji) == '\U0001f579')
		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0,check=check)
			await game.remove_reaction('\U0001f579',user)
			await game.remove_reaction('\U0001f579',self.bot.user)
		except a.TimeoutError:
			await game.edit(embed=None,content='No one joined your game. Try again later.')
			await game.remove_reaction('\U0001f579',self.bot.user)
		pone = ctx.author
		ptwo = user
		em.set_field_at(1,value=user.display_name)
		em.add_field(name='Turn ',value='It is currently pone\'s turn')
		await game.edit(embed=em)
		

	@bot_has_permissions(manage_messages=True)
	@c.command(name='hangman')
	async def hangman(self,ctx):
		"""Play hangman! 6 misses max!"""
		misses = []
		em = d.Embed(title='Hangman!')
		em.add_field(name='Word!',value='_',inline=True)
		em.add_field(name='Misses ',value='0')
		em.set_footer(text=ctx.author.display_name,icon_url=ctx.author.avatar_url)
		game = await ctx.send(embed=em)
		join = await ctx.send('Please react to join this game')
		await game.add_reaction('\U0001f579')

		def check(reaction, user):
			return (str(reaction.emoji) == '\U0001f579')
		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0,check=check)
			await game.remove_reaction('\U0001f579',user)
			await game.remove_reaction('\U0001f579',self.bot.user)
			await join.edit(content=None)
		except a.TimeoutError as e:
			await game.edit(embed=None,content='No one joined your game. Try again later.')
			await join.edit(content=None)
			await game.remove_reaction('\U0001f579',self.bot.user)
		
		pone = ctx.author
		ptwo = user
		waiting = await ctx.send('Waiting for a word :thinking:...')
		if pone.dm_channel == None:
			await pone.create_dm()
		await pone.dm_channel.send('Please type in the word you want {} to guess for!\nMake sure it is less than 10 letters!'.format(ptwo.mention))
		try:
			def chec(message):
				return message.channel == pone.dm_channel and len(message.content) > 0 and message.author != self.bot.user
			message = await self.bot.wait_for('message',check=chec)
			word = message.content
			i = len(word)
			word = list(word)
			space='|\_| '
			while i>1:
				space += '|\_| '
				i -= 1
			em.set_field_at(0,name='Word!',value=space)
			playing = True
			alphabet1 = {'\U0001f1e6':'a','\U0001f1e7':'b','\U0001f1e8':'c','\U0001f1e9':'d','\U0001f1ea':'e','\U0001f1eb':'f','\U0001f1ec':'g','\U0001f1ed':'h','\U0001f1ee':'i','\U0001f1ef':'j','\U0001f1f0':'k','\U0001f1f1':'l','\U0001f1f2':'m','\U0001f1f3':'n','\U0001f1f4':'o','\U0001f1f5':'p','\U0001f1f6':'q','\U0001f1f7':'r','\U0001f1f8':'s','\U0001f1f9':'t'}
			alphabet2 = {'\U0001f1fa':'u','\U0001f1fb':'v','\U0001f1fc':'w','\U0001f1fd':'x','\U0001f1fe':'y','\U0001f1ff':'z'}
			for letter in alphabet1:
				await game.add_reaction(letter)
			await waiting.edit(content='')
			for letter in alphabet2:
				await waiting.add_reaction(letter)
			win = 0
			def check_letter(reaction, user):
				return (reaction.emoji in alphabet1 or reaction.emoji in alphabet2 and user == ptwo and user != pone)
			while playing:
				space = space.split(' ')
				reaction, user = await self.bot.wait_for('reaction_add',timeout=180.0,check=check_letter)
				if reaction.emoji in alphabet1: #removes reaction
					await game.remove_reaction(reaction.emoji,user)
					react = alphabet1[reaction.emoji]
				else:
					await waiting.remove_reaction(reaction.emoji,user)
					react = alphabet2[reaction.emoji]
				if react not in word:
					misses.append('react')
				while react in word:
					index_l = word.index(react) #get index of letter to replace in the `space` list
					word[index_l] = 'GUESSED' #workaround
					space[index_l] = '{}'.format(react)
				space = ' '.join(space) #need to get the 'blanks' joined to display when updating
				em.set_field_at(0,name='Game!',value=space)
				em.set_field_at(1,name='Misses!',value=', '.join(misses))
				await game.edit(embed=em)
				if len(misses) > 6: #win / lose
					playing = False 
					winner = pone
					loser = ptwo
				win = 0
				for letter in word:
					if letter == 'GUESSED':
						win += 1
				if win == len(word):
					playing = False
					winner = ptwo.mention
					loser = pone.mention
				
			await ctx.send('{} has won! \n{} has lost!'.format(winner, loser))
		except a.TimeoutError:
			await ctx.send('This game timed out.')


def setup(bot):
	bot.add_cog(Games(bot))