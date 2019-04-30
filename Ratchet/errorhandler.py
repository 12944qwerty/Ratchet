import traceback
import sys
from discord.ext import commands
import discord

class CommandErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		"""The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

		if hasattr(ctx.command, 'on_error'):
			return

		ignored = (commands.CommandNotFound, commands.UserInputError)

		error = getattr(error, 'original', error)

		if isinstance(error, ignored):
			return

		elif isinstance(error, commands.DisabledCommand):
			return await ctx.send(f'{ctx.command} has been disabled.')

		elif isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
			except:
				pass

		elif isinstance(error, commands.BadArgument):
			return await ctx.send('Error: Bad Argument')

		elif isinstance(error, commands.CommandOnCooldown):
			return await ctx.send(f'Please wait another {round(error.retry_after,1)} secs')

def setup(bot):
	bot.add_cog(CommandErrorHandler(bot))
