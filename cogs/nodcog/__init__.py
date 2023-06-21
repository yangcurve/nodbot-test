from .nodcog import NodCog


async def setup(bot):
    await bot.add_cog(NodCog(bot))
