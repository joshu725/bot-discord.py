# Librerias
import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
from colorthief import ColorThief
import colorsys
import asyncio
from PIL import Image, ImageSequence
from datetime import datetime, timedelta

# Clase principal
class Mudae(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.comprobarTiempo.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Registra el momento en el que se hace correctamente un $bitesthedust requiem
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 432610292342587392 and message.content == "Otro más que muerde el polvo...\nhttps://imgur.com/Fiptqgp.gif" and message.channel.id == 1247267606415806496:
            f = open("assets/datetime.txt", "w")
            f.write(str(message.created_at))
            f.close()

    @tasks.loop(minutes=5.0)
    async def comprobarTiempo(self):
        f = open("assets/datetime.txt", "r")
        time = datetime.strptime(f.read(26), '%Y-%m-%d %H:%M:%S.%f')
        f.close()
        
        time += timedelta(days=14, hours=18)
        now_time = datetime.now()
        
        if now_time > time:
            channel = await self.bot.fetch_channel(1247267606415806496)
            
            embed = discord.Embed(title="Kakera :)", description=f"El siguiente comando está disponible\n```$bitesthedust requiem```", colour=0xa484a6)
            embed.set_thumbnail(url="https://i.imgur.com/FDBj4Oe.gif")
            embed.set_image(url="https://imgur.com/Fiptqgp.gif")

            await channel.send("<@263880901094539266> <@235197855529304064>", embed=embed)
            self.comprobarTiempo.stop()

    # Comando para colocar color al embed del bot Mudae
    @commands.command(aliases=['ec'])
    async def embedcolor(self, ctx):
        async for message in ctx.channel.history(limit=100):
            if message.author.id == 432610292342587392:
                embeds = message.embeds
                for embed in embeds:
                    lastEmbed = embed.to_dict()
                    image = lastEmbed['image']['url']

                    def ensure_png_extension(image_url):
                        # Lista de extensiones de imágenes comunes
                        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
                        
                        # Verifica si la URL termina con alguna de las extensiones válidas
                        if not any(image_url.endswith(ext) for ext in valid_extensions):
                            image_url += '.png'
                        
                        return image_url

                    image = ensure_png_extension(image)

                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                    
                    with requests.get(image, headers=headers, allow_redirects=True) as r:
                        img_data = r.content
                    with open('img/mudae.png', 'wb') as handler:
                        handler.write(img_data)

                    # 5 colores dominantes
                    ct = ColorThief("img/mudae.png")
                    palette = ct.get_palette(color_count=5)

                    embedImg = discord.Embed(
                        title = lastEmbed['author']['name'],
                        description=f"```$ec {lastEmbed['author']['name']} $#{palette[0][0]:02x}{palette[0][1]:02x}{palette[0][2]:02x}```",
                        color = discord.Color.from_rgb(palette[0][0], palette[0][1], palette[0][2])
                    )
                    embedImg.set_image(url=image)
                    embedImg.set_footer(text=f"{1}")

                    class changeButtons(discord.ui.View):
                        def __init__(self, author : str, palette : list, url : str, idAutor : int):
                            super().__init__()
                            self.author = author
                            self.palette = palette
                            self.url = url
                            self.idAutor = idAutor
                            self.index = 0

                        @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.grey)
                        async def changeLeft(self, interaction: discord.Interaction, button: discord.ui.Button):
                            if self.index <= 0:
                                self.index = 4
                            else:
                                self.index -= 1

                            embedImg = discord.Embed(
                                title = self.author,
                                description = f"```$ec {self.author} $#{self.palette[self.index][0]:02x}{self.palette[self.index][1]:02x}{self.palette[self.index][2]:02x}```",
                                color = discord.Color.from_rgb(self.palette[self.index][0], self.palette[self.index][1], self.palette[self.index][2])
                            )
                            embedImg.set_image(url=self.url)
                            embedImg.set_footer(text=f"{self.index+1}")

                            await interaction.response.edit_message(embed=embedImg)
                        
                        @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.grey)
                        async def changeRight(self, interaction: discord.Interaction, button: discord.ui.Button):
                            if self.index >= 4:
                                self.index = 0
                            else:
                                self.index += 1
                                
                            embedImg = discord.Embed(
                                title = self.author,
                                description = f"```$ec {self.author} $#{self.palette[self.index][0]:02x}{self.palette[self.index][1]:02x}{self.palette[self.index][2]:02x}```",
                                color = discord.Color.from_rgb(self.palette[self.index][0], self.palette[self.index][1], self.palette[self.index][2])
                            )
                            embedImg.set_image(url=self.url)
                            embedImg.set_footer(text=f"{self.index+1}")

                            await interaction.response.edit_message(embed=embedImg)
                        
                        @discord.ui.button(emoji='🗑️', style=discord.ButtonStyle.red)
                        async def changeDelete(self, interaction: discord.Interaction, button: discord.ui.Button):
                            if interaction.user.id == self.idAutor:
                                await interaction.message.delete()
                            else:
                                await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)

                    await ctx.send(embed=embedImg, view=changeButtons(lastEmbed['author']['name'], palette, image, ctx.author.id))
                    return

    # Comando para cortar gifs conservando la relación de aspecto de las imagenes del bot Mudae
    @commands.command(aliases=['cg'])
    async def cortargif(self, ctx, link = None):
        async with ctx.message.channel.typing():
            if link == None:
                if ctx.message.attachments:
                    link = ctx.message.attachments[0].url
                else:
                    await ctx.send(embed=discord.Embed(description=f"❌・Inserta un gif o un enlace", color=0xdd6879))
                    return

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            with requests.get(link, headers=headers, allow_redirects=True) as r:
                img_data = r.content
            with open('img/imagen_cortada.gif', 'wb') as handler:
                handler.write(img_data)

            img = Image.open("img/imagen_cortada.gif")

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

            frames = []
            for frame in ImageSequence.Iterator(img):
                frame = frame.crop((left, top, right, bottom))
                frames.append(frame)

            frames[0].save('img/imagen_cortada.gif', save_all=True, append_images=frames[1:], loop=0)

            await ctx.send(
                content=f"- **Dimensiones:** {round(right-left)}x{round(bottom-top)}\n- **Recortar manualmente:**\n<https://www.iloveimg.com/crop-image>",
                file=discord.File("img/imagen_cortada.gif"))
    @cortargif.error
    async def cortargif_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(description=f"❌・Inserta un gif o un enlace", color=0xdd6879))

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

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            with requests.get(link, headers=headers, allow_redirects=True) as r:
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