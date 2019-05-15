import discord as d
import discord.ext.commands as c
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from io import StringIO
from contextlib import redirect_stdout

class Owner(c.Cog,command_attrs={'hidden':True}):
	def __init__(self,client):
		self.bot = client

	@c.command(name='reload',alias=['reload_cog'])
	async def reload_(self,ctx,cog):
		"""reload a cog"""
		try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

	@c.command(name='eval')
	@c.is_owner()
	async def eval_(self,ctx, *, arg:str):
		env = {
			'ctx':ctx,
			'discord':d,
			'commands':c,
			'guild':ctx.guild,
			'channel':ctx.channel,
			'client':self.bot
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
			em = d.Embed(
				title='error',
				description=f'```{e}```'
			)
			await ctx.send(f'```\n{out.getvalue()}\n```',embed=em)
		else:
			em = d.Embed(
				title='Success!',
				description=f'```{ret!r}```'
			)
			await ctx.send(f'```\n{out.getvalue()}\n```',embed=em)

	async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            await ctx.send('You need to own this bot. Which only 12944qwerty#9317 does.')
        return True

def setup(bot):
	bot.add_cog(Owner(bot))
