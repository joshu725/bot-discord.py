# Librerias
import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
from colorthief import ColorThief
from PIL import Image, ImageSequence
from datetime import datetime, timedelta
import re

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

    # Cada 5 minutos se comprueba que la fecha actual sea mayor a la fecha indicada en 'datetime.txt' + 15 dias
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
    @commands.hybrid_command(name="embedcolor", description="Comando para colocar color al embed del personaje en el bot Mudae", aliases=['ec'])
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
    @embedcolor.error
    async def embedcolor_error(self, ctx, error):
        print(error)
        await ctx.send(embed=discord.Embed(description=f"❌・No se ha encontrado un mensaje `embed` de Mudae", color=0xdd6879))

    # Comando para cortar imagenes conservando la relación de aspecto de las imagenes del bot Mudae
    @commands.hybrid_command(name="cortarimagen", description="Comando para cortar imagenes conservando la relación de aspecto de las imagenes del bot Mudae", aliases=['ci'])
    @app_commands.describe(enlace = "Enlace de imagen")
    async def cortarimagen(self, ctx, enlace : str = None):
        class cropButtonsW(discord.ui.View):
            def __init__(self, img_original : Image, idAutor : int, left : int, top : int, right : int, bottom : int):
                super().__init__()
                self.img_original = img_original
                self.idAutor = idAutor
                self.left = left
                self.top = top
                self.right = right
                self.bottom = bottom

            @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.grey)
            async def cropLeft(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.left > 25:
                        self.left -= 25
                        self.right -= 25

                        img_cortada = self.img_original.crop((self.left, self.top, self.right, self.bottom))
                        img_cortada = img_cortada.save("img/imagen_cortada.png")

                        img_cortada = Image.open("img/imagen_cortada.png")
                        img_cortada = img_cortada.resize((225, 350))
                        marco = Image.open("assets/marco.png")
                        img_cortada.paste(marco, (0, 0), marco)
                        img_cortada.save("img/imagen_cortada.png")

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.png")],
                            view=cropButtonsW(self.img_original, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)
                    
            
            @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.grey)
            async def cropRight(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.right < self.img_original.size[0] - 25:
                        self.left += 25
                        self.right += 25

                        img_cortada = self.img_original.crop((self.left, self.top, self.right, self.bottom))
                        img_cortada = img_cortada.save("img/imagen_cortada.png")

                        img_cortada = Image.open("img/imagen_cortada.png")
                        img_cortada = img_cortada.resize((225, 350))
                        marco = Image.open("assets/marco.png")
                        img_cortada.paste(marco, (0, 0), marco)
                        img_cortada.save("img/imagen_cortada.png")

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.png")],
                            view=cropButtonsW(self.img_original, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)

        class cropButtonsH(discord.ui.View):
            def __init__(self, img_original : Image, idAutor : int, left : int, top : int, right : int, bottom : int):
                super().__init__()
                self.img_original = img_original
                self.idAutor = idAutor
                self.left = left
                self.top = top
                self.right = right
                self.bottom = bottom

            @discord.ui.button(emoji='🔼', style=discord.ButtonStyle.grey)
            async def cropTop(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.top > 25:
                        self.top -= 25
                        self.bottom -= 25

                        img_cortada = self.img_original.crop((self.left, self.top, self.right, self.bottom))
                        img_cortada = img_cortada.save("img/imagen_cortada.png")

                        img_cortada = Image.open("img/imagen_cortada.png")
                        img_cortada = img_cortada.resize((225, 350))
                        marco = Image.open("assets/marco.png")
                        img_cortada.paste(marco, (0, 0), marco)
                        img_cortada.save("img/imagen_cortada.png")

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.png")],
                            view=cropButtonsH(self.img_original, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)
                    
            
            @discord.ui.button(emoji='🔽', style=discord.ButtonStyle.grey)
            async def cropBottom(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.bottom < self.img_original.size[1] - 25:
                        self.top += 25
                        self.bottom += 25

                        img_cortada = self.img_original.crop((self.left, self.top, self.right, self.bottom))
                        img_cortada = img_cortada.save("img/imagen_cortada.png")

                        img_cortada = Image.open("img/imagen_cortada.png")
                        img_cortada = img_cortada.resize((225, 350))
                        marco = Image.open("assets/marco.png")
                        img_cortada.paste(marco, (0, 0), marco)
                        img_cortada.save("img/imagen_cortada.png")

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.png")],
                            view=cropButtonsH(self.img_original, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)

        if enlace == None:
            if ctx.message.attachments:
                enlace = ctx.message.attachments[0].url
            else:
                await ctx.send(embed=discord.Embed(description=f"❌・Inserta una imagen o un enlace", color=0xdd6879))
                return

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        with requests.get(enlace, headers=headers, allow_redirects=True) as r:
            img_data = r.content
        with open('img/imagen_original.png', 'wb') as handler:
            handler.write(img_data)

        img_original = Image.open("img/imagen_original.png")
        width, height = img_original.size

        aspectratio = 9/14

        widthN = aspectratio * height
        heightN = width / aspectratio

        bandera = False

        if width >= widthN:
            top = 0
            bottom = height
            
            centerW = width / 2

            left = centerW - (widthN/2)
            right = centerW + (widthN/2)

            bandera = True
        else:
            left = 0
            right = width

            centerH = height / 2

            top = centerH - (heightN/2)
            bottom = centerH + (heightN/2)

            bandera = False

        img_cortada = img_original.crop((left, top, right, bottom))
        img_cortada = img_cortada.save("img/imagen_cortada.png")

        img_cortada = Image.open("img/imagen_cortada.png")
        img_cortada = img_cortada.resize((225, 350))
        marco = Image.open("assets/marco.png")
        img_cortada.paste(marco, (0, 0), marco)
        img_cortada.save("img/imagen_cortada.png")

        if bandera == True:
            await ctx.send(
                file=discord.File("img/imagen_cortada.png"),
                view=cropButtonsW(img_original, ctx.author.id, left, top, right, bottom))
        else:
            await ctx.send(
                file=discord.File("img/imagen_cortada.png"),
                view=cropButtonsH(img_original, ctx.author.id, left, top, right, bottom))
    @cortarimagen.error
    async def cortarimagen_error(self, ctx, error):
        print(error)
        await ctx.send(embed=discord.Embed(description=f"❌・Inserta una imagen o un enlace", color=0xdd6879))

    # Comando para cortar imagenes conservando la relación de aspecto de las imagenes del bot Mudae
    @commands.hybrid_command(name="cortargif", description="Comando para cortar gifs conservando la relación de aspecto de las imagenes del bot Mudae", aliases=['cg'])
    @app_commands.describe(enlace = "Enlace del gif")
    async def cortargif(self, ctx, enlace : str = None):
        await ctx.defer()
        class cropButtonsW(discord.ui.View):
            def __init__(self, img_original : Image, marco : Image, idAutor : int, left : int, top : int, right : int, bottom : int):
                super().__init__()
                self.img_original = img_original
                self.marco = marco
                self.idAutor = idAutor
                self.left = left
                self.top = top
                self.right = right
                self.bottom = bottom

            @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.grey)
            async def cropLeft(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.left > 25:
                        self.left -= 25
                        self.right -= 25

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frame.thumbnail((225, 350))
                            frame.paste(self.marco, (0, 0), self.marco)
                            frames.append(frame)

                        frames[1].save('img/imagen_cortada.gif', save_all=True, append_images=frames[2:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
                            view=cropButtonsW(self.img_original, self.marco, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)
                    
            
            @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.grey)
            async def cropRight(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.right < self.img_original.size[0] - 25:
                        self.left += 25
                        self.right += 25

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frame.thumbnail((225, 350))
                            frame.paste(self.marco, (0, 0), self.marco)
                            frames.append(frame)

                        frames[1].save('img/imagen_cortada.gif', save_all=True, append_images=frames[2:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
                            view=cropButtonsW(self.img_original, self.marco, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)

        class cropButtonsH(discord.ui.View):
            def __init__(self, img_original : Image, marco : Image, idAutor : int, left : int, top : int, right : int, bottom : int):
                super().__init__()
                self.img_original = img_original
                self.marco = marco
                self.idAutor = idAutor
                self.left = left
                self.top = top
                self.right = right
                self.bottom = bottom

            @discord.ui.button(emoji='🔼', style=discord.ButtonStyle.grey)
            async def cropTop(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.top > 25:
                        self.top -= 25
                        self.bottom -= 25

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frame.thumbnail((225, 350))
                            frame.paste(self.marco, (0, 0), self.marco)
                            frames.append(frame)

                        frames[1].save('img/imagen_cortada.gif', save_all=True, append_images=frames[2:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
                            view=cropButtonsH(self.img_original, self.marco, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)
                    
            
            @discord.ui.button(emoji='🔽', style=discord.ButtonStyle.grey)
            async def cropBottom(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id == self.idAutor:
                    if self.bottom < self.img_original.size[1] - 25:
                        self.top += 25
                        self.bottom += 25

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frame.thumbnail((225, 350))
                            frame.paste(self.marco, (0, 0), self.marco)
                            frames.append(frame)

                        frames[1].save('img/imagen_cortada.gif', save_all=True, append_images=frames[2:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
                            view=cropButtonsH(self.img_original, self.marco, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)

        if enlace == None:
            if ctx.message.attachments:
                enlace = ctx.message.attachments[0].url
            else:
                await ctx.send(embed=discord.Embed(description=f"❌・Inserta un gif o un enlace", color=0xdd6879))
                return

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        with requests.get(enlace, headers=headers, allow_redirects=True) as r:
            img_data = r.content
        with open('img/imagen_original.gif', 'wb') as handler:
            handler.write(img_data)

        img_original = Image.open("img/imagen_original.gif")
        width, height = img_original.size

        aspectratio = 9/14

        widthN = aspectratio * height
        heightN = width / aspectratio

        bandera = False

        if width >= widthN:
            top = 0
            bottom = height
            
            centerW = width / 2

            left = centerW - (widthN/2)
            right = centerW + (widthN/2)

            if width % 2 == 0:
                right -= 1

            bandera = True
        else:
            left = 0
            right = width

            centerH = height / 2

            top = centerH - (heightN/2)
            bottom = centerH + (heightN/2)

            if height % 2 == 0:
                bottom -= 1

            bandera = False

        marco = Image.open("assets/marco.png")
        if (right-left) < 225 or (bottom-top) < 350:
            marco = marco.resize((int(right-left), int(bottom-top)))

        frames = []
        for frame in ImageSequence.Iterator(img_original):
            frame = frame.crop((left, top, right, bottom))
            frame.thumbnail((225, 350))
            frame.paste(marco, (0, 0), marco)
            frames.append(frame)

        frames[1].save('img/imagen_cortada.gif', save_all=True, append_images=frames[2:], loop=0)

        if bandera == True:
            await ctx.send(
                file=discord.File("img/imagen_cortada.gif"),
                view=cropButtonsW(img_original, marco, ctx.author.id, left, top, right, bottom))
        else:
            await ctx.send(
                file=discord.File("img/imagen_cortada.gif"),
                view=cropButtonsH(img_original, marco, ctx.author.id, left, top, right, bottom))
    @cortargif.error
    async def cortargif_error(self, ctx, error):
        print(error)
        await ctx.send(embed=discord.Embed(description=f"❌・Inserta un gif o un enlace", color=0xdd6879))

    # Comando para ver el tiempo exacto que falta para el $bitesthedust requiem
    @commands.hybrid_command(name="tiemporestante", description="Comando para ver el tiempo exacto que falta para el $bitesthedust requiem", aliases=['tr'])
    async def tiemporestante(self, ctx):
        f = open("assets/datetime.txt", "r")
        time = datetime.strptime(f.read(26), '%Y-%m-%d %H:%M:%S.%f')
        f.close()
        
        time += timedelta(days=14, hours=18)
        
        now_time = datetime.now()
        diff = time - now_time
        
        dias = diff.days
        horas = diff.seconds//3600
        minutos = (diff.seconds//60)%60
        
        mudae = await self.bot.fetch_user(432610292342587392)
        
        embed = discord.Embed(title="Tiempo restante", description=f"Faltan {dias} días, {horas} horas, y {minutos} minutos para el `$bitesthedust requiem`", colour=0xdd6879)
        embed.set_thumbnail(url=mudae.avatar)
        embed.timestamp = time
        embed.set_footer(text="Fecha", icon_url="https://i.imgur.com/fEH1X8C.png")
        await ctx.send(embed=embed)

    # Comando para mandar enlace del mensaje con el personaje mas alto en kakera de los tiros recientes en Mudae
    @commands.hybrid_command(name="kakera", description="Comando para mandar enlace del mensaje con el personaje mas alto en kakera de los tiros recientes", aliases=['k'])
    async def kakera(self, ctx):
        mayor = 0
        enlaceMayor = ""
        async for message in ctx.channel.history(limit=100):
            if message.author.id == 432610292342587392:
                if message.interaction:
                    if message.interaction.user.id == ctx.author.id:
                        if not message.components:
                            if (datetime.now(message.created_at.tzinfo) - message.created_at).seconds < 90:
                                if message.embeds:
                                    for embed in message.embeds:
                                        lastEmbed = embed.to_dict()

                                    if "footer" not in lastEmbed or "icon_url" not in lastEmbed["footer"]:
                                        pattern = r"\*\*(\d+)\*\*<:kakera:469835869059153940>"
                                        match = re.search(pattern, lastEmbed["description"])
                                        number = int(match.group(1))
                                        
                                        if (number > mayor):
                                            mayor = number
                                            enlaceMayor = message.jump_url
                                            creadoMayor = message.created_at
                                            msg = message
                                            imgPj = lastEmbed["image"]["url"]
                                            nombrePj = lastEmbed['author']['name']
        
        if not enlaceMayor == "":
            actual = datetime.now(creadoMayor.tzinfo)
            await msg.add_reaction(":kakera:1260465357085474968")
            
            embed = discord.Embed(title=f"{nombrePj}・{mayor} <:kakera:1260465357085474968>", color=0x879bf5)
            embed.add_field(name=f"💬 Enlace al mensaje", value=enlaceMayor, inline=False)
            embed.set_footer(text=f"Tiempo restante: {90 - (actual - creadoMayor).seconds} segundos", icon_url="https://i.imgur.com/fEH1X8C.png")
            embed.set_thumbnail(url=imgPj)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(description=f"❌・No se encontró un tiro tuyo reclamable (comandos slash)", color=0xdd6879), ephemeral=True)
    @kakera.error
    async def kakera_error(self, ctx, error):
        print(error)
        await ctx.send(embed=discord.Embed(description=f"❌・No se encontró un tiro tuyo reclamable (comandos slash)", color=0xdd6879), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mudae(bot))