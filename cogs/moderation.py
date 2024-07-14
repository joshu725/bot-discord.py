# Librerias
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

# Clase principal
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")
    
    # Comando para eliminar la cantidad de mensajes especificada
    @commands.hybrid_command(name="prune", description="Comando para eliminar la cantidad de mensajes especificada")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(cantidad="Cantidad de mensajes que deseas eliminar")
    async def prune(self, ctx, cantidad : commands.Range[int, 1]):
        if not ctx.interaction:
            await ctx.message.delete()
        else:
            await ctx.defer(ephemeral=True)
        
        await ctx.channel.purge(limit=cantidad)

        if ctx.interaction:
            await ctx.send(f"Se han eliminado {cantidad} mensajes", ephemeral=True, delete_after=3)
    @prune.error
    async def prune_error(self, ctx, error):
        await ctx.send(embed=createEmbedInfo("prune", "Elimina la cantidad de mensajes especificada", "!prune 'cantidad'", self.bot.user.avatar))

async def setup(bot):
    await bot.add_cog(Moderation(bot))

def createEmbedInfo(comando : str, especificacion : str, formato : str, urlIcono : str):
    embed = discord.Embed(description = especificacion, color = 0xffa3a3)
    embed.set_author(name = comando, icon_url = urlIcono)
    embed.add_field(name = "🗒️ Formato", value=f"`{formato}`", inline=False)
    return embed