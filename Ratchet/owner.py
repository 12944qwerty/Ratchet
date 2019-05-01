from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module."""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
            
  @commands.command(name='stop',hidden=True)
  @commands.is_owner()
	async def stop(self,ctx):
		"""Stop the bot. ONLY ADMINS CAN DO SO (and owner)"""
    msg = await ctx.send('Stopping.......')
    await msg.edit(content='Stopped!')
    print('{} stopped this bot. - {}'.format(ctx.author.display_name,ctx.guild.name))
    self.bot.loop.run_until_complete(self.bot.logout())

def setup(bot):
    bot.add_cog(Owner(bot))
