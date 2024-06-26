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

    # Latencia
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms :ping_pong:")

async def setup(bot):
    await bot.add_cog(Prefix_Commands(bot))