# Librerias
import discord
from discord.ext import commands
import requests
from colorthief import ColorThief
import colorsys
import asyncio
from PIL import Image

# Clase principal
class Mudae(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Comando para colocar color al embed del bot Mudae
    @commands.command(aliases=['ec'])
    async def embedcolor(self, ctx):
        async for message in ctx.channel.history(limit=100):
            if message.author.id == 432610292342587392:
                embeds = message.embeds
                for embed in embeds:
                    lastEmbed = embed.to_dict()
                    image = lastEmbed['image']['url']
                    with requests.get(image) as r:
                        img_data = r.content
                    with open('img/mudae.png', 'wb') as handler:
                        handler.write(img_data)

                    # 5 colores dominantes
                    ct = ColorThief("img/mudae.png")
                    palette = ct.get_palette(color_count=5)

                    i = 0

                    embedImg = discord.Embed(
                        title = lastEmbed['author']['name'],
                        description=f"```$ec {lastEmbed['author']['name']} $#{palette[0][0]:02x}{palette[0][1]:02x}{palette[0][2]:02x}```",
                        color = discord.Color.from_rgb(palette[0][0], palette[0][1], palette[0][2])
                    )
                    embedImg.set_image(url=image)
                    embedImg.set_footer(text=f"{i+1}")
                    msg = await ctx.send(embed=embedImg)

                    atras = "◀️"
                    adelante = "▶️"

                    await msg.add_reaction(atras)
                    await msg.add_reaction(adelante)

                    tiempo = 0

                    valid_reactions = ['◀️', '▶️']

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in valid_reactions
                    
                    while tiempo < 3:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=45, check=check)
                        if reaction != None and user != None:
                            if str(reaction.emoji) == adelante:
                                if i >= 4:
                                    i = 0
                                else:
                                    i += 1
                                tiempo = 0
                                await msg.remove_reaction(reaction, user)
                                
                            if str(reaction.emoji) == atras:
                                if i <= 0:
                                    i = 4
                                else:
                                    i -= 1
                                tiempo = 0
                                await msg.remove_reaction(reaction, user)

                            reaction = None
                            user = None

                            embedImg = discord.Embed(
                                title = lastEmbed['author']['name'],
                                description=f"```$ec {lastEmbed['author']['name']} $#{palette[i][0]:02x}{palette[i][1]:02x}{palette[i][2]:02x}```",
                                color = discord.Color.from_rgb(palette[i][0], palette[i][1], palette[i][2])
                            )
                            embedImg.set_image(url=image)
                            embedImg.set_footer(text=f"{i+1}")
                            await msg.edit(embed=embedImg)
                        
                        await asyncio.sleep(1)
                        tiempo += 1
                    return

    # Comando para cortar imagenes conservando la relación de aspecto de las imagenes del bot Mudae
    @commands.command(aliases=['ci'])
    async def cortarimagen(self, ctx, link = None):
        async with ctx.message.channel.typing():
            if link == None:
                if ctx.message.attachments:
                    link = ctx.message.attachments[0].url
                else:
                    await ctx.send(embed=discord.Embed(description=f"❌・Inserta una imagen o un enlace", color=0xdd6879))
                    return

            with requests.get(link) as r:
                img_data = r.content
            with open('img/imagen_cortada.png', 'wb') as handler:
                handler.write(img_data)

            img = Image.open("img/imagen_cortada.png")
            width, height = img.size

            aspectratio = 9/14

            widthN = aspectratio * height
            heightN = width / aspectratio

            if width >= widthN:
                top = 0
                bottom = height
                
                centerW = width / 2

                left = centerW - (widthN/2)
                right = centerW + (widthN/2)
            else:
                left = 0
                right = width

                centerH = height / 2

                top = centerH - (heightN/2)
                bottom = centerH + (heightN/2)

            img = img.crop((left, top, right, bottom))
            width, height = img.size
            img = img.save("img/imagen_cortada.png")

            await ctx.send(content=f"- **Dimensiones:** {round(width)}x{round(height)}\n- **Recortar manualmente:**\n<https://www.iloveimg.com/crop-image>", file=discord.File("img/imagen_cortada.png"))
    @cortarimagen.error
    async def cortarimagen_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(description=f"❌・Inserta una imagen o un enlace", color=0xdd6879))

async def setup(bot):
    await bot.add_cog(Mudae(bot))