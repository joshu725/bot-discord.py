# Librerias
import discord
from discord.ext import commands
from colorthief import ColorThief
import requests
import asyncio

# Clase principal
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Muestra el avatar tuyo o de la persona que menciones
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        async with ctx.message.channel.typing():
            bandera = False
            if member == None:
                member = ctx.author
            else:
                bandera = True
            
            with requests.get(member.avatar) as r:
                img_data = r.content
            with open('img/avatar.png', 'wb') as handler:
                handler.write(img_data)
            
            ct = ColorThief("img/avatar.png")
            color = ct.get_color(quality=1)

            show_avatar = discord.Embed(
                title = member.display_name,
                description=f"[URL]({member.avatar})",
                color = discord.Color.from_rgb(color[0], color[1], color[2])
            )
            show_avatar.set_image(url=member.avatar)
            if bandera == True:
                show_avatar.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=show_avatar)

    # Borra el mensaje y dice exactamente lo mismo que le indiques
    @commands.command()
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)

async def setup(bot):
    await bot.add_cog(Utility(bot))