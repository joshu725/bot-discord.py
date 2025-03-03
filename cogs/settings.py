# Librerias
import discord
from discord.ext import commands
from discord import app_commands
import os

# Clase principal
class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Muestra el avatar tuyo o de la persona que menciones
    @commands.hybrid_command(name="help", description="Acerca de Choppa")
    async def help(self, ctx):
        embed = discord.Embed(title = "Acerca de Choppa", description=f"- Este es un bot personal creado con el fin de apoyar y divertir con comandos interactivos.", color=0xffa3a3)

        embed.add_field(name=f"🔧 Utilidad", value="`avatar`, `say`, `emoji`, `fxtwitter`, `reemplazar`", inline=False)
        embed.add_field(name=f"🖼️ Multimedia", value="`youtube`, `twitter`, `tiktok`, `reel`, `instagram`, `imgur`", inline=False)
        embed.add_field(name=f"🎨 Entretenimiento", value="`apuntar`, `quieres`, `logro`, `love`", inline=False)
        embed.add_field(name=f"🛠️ Moderación", value="`prune`, `kick`, `ban`, `unban`, `mute`, `unmute`, `warn`, `warnings`", inline=False)
        embed.add_field(name=f"<:kakera:1260465357085474968> Mudae", value="`embedcolor`, `cortarimagen`, `cortargif`, `tiemporestante`, `kakera`, `personajes`", inline=False)

        embed.set_image(url="https://i.imgur.com/SOZfVMH.jpeg")

        owner = await self.bot.fetch_user(235197855529304064)
        embed.set_footer(text=f"© moguril", icon_url=owner.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)

        await ctx.send(embed=embed)

    # Comando para recargar los cogs
    @commands.command(aliases=['re'])
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[:-3]}")
                await ctx.message.add_reaction('✅')
    @reload.error
    async def reload_error(self, ctx, error):
        print(error)
        await ctx.message.add_reaction('❌')
    
    # Comando para para ver la información de un mensaje con su ID
    @commands.command(aliases=['m'])
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, channel_id : int, message_id : int):
        await ctx.message.delete()
        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        print("--------------------")
        print(message.embeds[0].to_dict())
        print("---")
        print(message.created_at)
        print("--------------------")

async def setup(bot):
    await bot.add_cog(Settings(bot))