# Librerias
import discord
from discord.ext import commands

class Prefix_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Saludo
    @commands.command()
    async def hola(self, ctx):
        await ctx.send(f"¡Hola {ctx.author.mention}!")

    # Buenos dias
    @commands.command(aliases=["buendia", "buenosdia"]) # Uso de "aliases"
    async def buenosdias(self, ctx):
        await ctx.send(f"Buenos dias {ctx.author.mention} :)")
    
    @commands.command() # Uso de "aliases"
    async def test(self, ctx):
        embed = discord.Embed(
            description="aaaaa"
        )
        embed.set_image(url="attachment://img/avatar.png",)
        await ctx.send(file=discord.File("img/avatar.png", filename="avatar.png"), embed=embed)
    @test.error
    async def test_error(self, ctx, error):
        print(error)


async def setup(bot):
    await bot.add_cog(Prefix_Commands(bot))