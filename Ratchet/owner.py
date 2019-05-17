import discord
import discord.ext.commands
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from io import StringIO
from contextlib import redirect_stdout

class Owner(commands.Cog,command_attrs={'hidden':True}):
	def __init__(self,client):
		self.bot = client

	@commands.command(name='reload',alias=['reload_cog'])
	async def reload_(self,ctx,cog):
		"""reload a cog"""
		try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

	@commands.command(name='eval')
	@commands.is_owner()
	async def eval_(self,ctx, *, arg:str):
		await ctx.message.add_reaction(chr(0x25b6))
		env = {
			'ctx':ctx,
			'discord':discord,
			'commands':commands,
			'guild':ctx.guild,
			'channel':ctx.channel,
			'client':self.bot,
			'message':ctx.message.content
		}
		out = StringIO()
		arg = arg.strip('`').rstrip().lstrip('\n').splitlines()
		indent = '    '
		for line in arg:
			strp = line.lstrip()
			if strp != line:
				indent = line[:len(line) - len(strp)]
				break
		arg = ''.join(indent + line + '\n' for line in arg)
		try:
			with redirect_stdout(out):
				exec(f"async def func():\n{arg}", env)
				ret = await env['func']()
		except BaseException as e:
			await ctx.message.add_reaction('\U0000203c')
			em = discord.Embed(
				title='EVALUATED'
			)
			em.add_field(
				name='CONSOLE',
				value=f'```{out.getvalue()}```'
			)
			em.add_field(
				name='RETURN',
				value=f'```{ret!r}```'
			)
			em.add_field(
				name='ERROR',
				value=f'```{e}```'
			)
		else:
			em = discord.Embed(
				title='EVALUATED'
			)
			em.add_field(
				name='CONSOLE',
				value=f'```{out.getvalue()}```'
			)
			em.add_field(
				name='RETURN',
				value=f'```{ret!r}```'
			)
			await ctx.message.add_reaction('\U00002705')
		await ctx.send(embed=em)

	async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            await ctx.send('You need to own this bot. Which only 12944qwerty#9317 does.')
        return True

def setup(bot):
	bot.add_cog(Owner(bot))
