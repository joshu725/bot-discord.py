# Librerias
import discord
from discord.ext import commands
from discord import app_commands
from colorthief import ColorThief
import requests
import random
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import asyncio
import colorsys
from urllib.parse import urlparse

class Slash_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # ----- Utilidad -----

    # Muestra el avatar tuyo o de la persona que menciones
    @app_commands.command(name="avatar", description="Ver el avatar tuyo o de otra persona")
    @app_commands.describe(member = "Usuario que deseas ver su avatar")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        bandera = False
        if member == None:
            member = interaction.user
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
            show_avatar.set_footer(text=f"Solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=show_avatar)
    @avatar.error
    async def avatar_error(self, interaction: discord.Interaction, error):
        print(error)

    # Comando para ver la latencia del bot
    @app_commands.command(name="ping", description="Muestra la latencia del bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms :ping_pong:")

    # Comando para mandar el enlace de Twitter de manera que los videos y las imagenes puedan visualizarse correctamente
    @app_commands.command(name="fxtwitter", description="Manda el enlace de Twitter de manera que los videos y las imagenes puedan visualizarse correctamente")
    @app_commands.describe(enlace = "Enlace de Twitter")
    async def fxtwitter(self, interaction: discord.Interaction, enlace : str):
        # Función para verificar validez del enlace y dominio
        def verificar_enlace(url):
            try:
                # Verificar si el dominio es "x.com"
                parsed_url = urlparse(url)
                if parsed_url.netloc != "x.com":
                    return "El enlace no pertenece a 'x.com'"
                
                # Encabezados para la solicitud
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                
                # Verificar si el enlace es válido
                response = requests.get(url, headers=headers, allow_redirects=True)
                if response.status_code == 200:
                    return "El enlace es válido"
                else:
                    return f"El enlace no es válido, código de estado: {response.status_code}"
            except requests.RequestException as e:
                return f"Ocurrió un error al verificar el enlace: {e}"

        # Verificación del enlace
        resultado = verificar_enlace(enlace)

        if resultado == "El enlace es válido":
            transformed_url = enlace.replace("x.com", "fxtwitter.com")
            await interaction.response.send_message(f"{transformed_url}")
        else:
            if resultado == "El enlace no pertenece a 'x.com'":
                await interaction.response.send_message(embed=discord.Embed(description=f"❌・El enlace no pertenece a Twitter", color=0xdd6879), ephemeral=True)
            else:
                await interaction.response.send_message(embed=discord.Embed(description=f"❌・Enlace inválido", color=0xdd6879), ephemeral=True)

    # --------------------

    # ------- Fun --------

    # Comando meme "apuntar"
    @app_commands.command(name="apuntar", description="Comando meme \"apuntar\"  que utiliza el avatar del usuario")
    @app_commands.describe(member = "Usuario con el que deseas aplicar este comando")
    async def apuntar(self, interaction: discord.Interaction, member : discord.Member=None):
        if member == None:
            await descargar_avatar(interaction.user.avatar)
        else:
            await descargar_avatar(member.avatar)
        avatar = Image.open("img/avatar.png")
        avatar = avatar.resize((512, 512))
        pistola = Image.open("assets/gun.png")
        pistola = pistola.resize((200, 200))
        avatar.paste(pistola, (300, 300), pistola)
        avatar.save("img/avatar.png")
        await interaction.response.send_message(file=discord.File("img/avatar.png"))

    # Comando meme "quieres?"
    @app_commands.command(name="quieres", description="Comando meme \"quieres\" que utiliza el avatar del usuario")
    @app_commands.describe(member = "Usuario con el que deseas aplicar este comando")
    async def quieres(self, interaction: discord.Interaction, member : discord.Member=None):
        if member == None:
            await descargar_avatar(interaction.user.avatar)
        else:
            await descargar_avatar(member.avatar)
        avatar = Image.open("img/avatar.png")
        avatar = avatar.resize((512, 512))
        quieres = Image.open("assets/quieres.png")
        quieres = quieres.resize((512, 512))
        avatar.paste(quieres, (0, 0), quieres)
        avatar.save("img/avatar.png")
        await interaction.response.send_message(file=discord.File("img/avatar.png"))

    # Comando para mandar una imagen del logro de Minecraft con los carácteres que indiquemos
    @app_commands.command(name="logro", description="Comando para mandar una imagen del logro de Minecraft con el texto que indiquemos")
    @app_commands.describe(texto = "Texto a indicar (21 carácteres máximo)")
    async def logro(self, interaction: discord.Interaction, texto : str = None):
        if texto == None:
            await interaction.response.send_message(embed=discord.Embed(description=f"**Crea tu propio logro al estilo Minecraft** \n\n`c!logro \"texto\"` (21 carácteres máximo)", color=0xdd6879))
            return

        if len(texto) < 22:
            items = ["apple", "arrow", "bed", "book", "bottled", "bucket", "cake", "charcoal", "chest", "chestplate", "diamond", "furnace", "gold", "grass", "musicdisk", "pickaxe", "sword", "table", "wood", "woodenplank"]
            item_aleatorio = random.choice(items)
            fondo = Image.open("assets/logro_minecraft/background.png")
            item = Image.open(f"assets/logro_minecraft/items/{item_aleatorio}.png")
            font = "assets/logro_minecraft/minecraft-font.ttf"
            fondo.paste(item, (16, 18), mask=item)
            draw = ImageDraw.Draw(fondo)
            fuente = ImageFont.truetype(font, 16)
            draw.text((56, 11), "Logro desbloqueado", (255, 255, 0), font=fuente)
            draw.text((56, 34), texto, (255, 255, 255), font=fuente)
            fondo.save("assets/logro_minecraft/minecraft_logro.png")

            await interaction.response.send_message(file=discord.File("assets/logro_minecraft/minecraft_logro.png"))
        else:
            await interaction.response.send_message(embed=discord.Embed(description=f"❌・21 carácteres máximo", color=0xdd6879), ephemeral=True)
    
    # --------------------

    # ------ Mudae -------

    # Comando para colocar color al embed del bot Mudae
    @app_commands.command(name="embedcolor", description="Comando para colocar color al embed del personaje en el bot Mudae")
    async def embedcolor(self, interaction: discord.Interaction):
        async for message in interaction.channel.history(limit=100):
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
                            
                    await interaction.response.send_message(embed=embedImg, view=changeButtons(lastEmbed['author']['name'], palette, image, interaction.user.id))
    


    # Comando para cortar imagenes conservando la relación de aspecto de las imagenes del bot Mudae
    @app_commands.command(name="cortarimagen", description="Comando para cortar imagenes conservando la relación de aspecto de las imagenes del bot Mudae")
    @app_commands.describe(enlace = "Enlace de imagen")
    async def cortarimagen(self, interaction: discord.Interaction, enlace : str):
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
            await interaction.response.send_message(
                file=discord.File("img/imagen_cortada.png"),
                view=cropButtonsW(img_original, interaction.user.id, left, top, right, bottom))
            
        else:
            await interaction.response.send_message(
                file=discord.File("img/imagen_cortada.png"),
                view=cropButtonsH(img_original, interaction.user.id, left, top, right, bottom))
    @cortarimagen.error
    async def cortarimagen_error(self, interaction: discord.Interaction, error):
        print(f"Error: {error}")


    # Comando para cortar imagenes conservando la relación de aspecto de las imagenes del bot Mudae
    @app_commands.command(name="cortargif", description="Comando para cortar gifs conservando la relación de aspecto de las imagenes del bot Mudae")
    @app_commands.describe(enlace = "Enlace del gif")
    async def cortargif(self, interaction: discord.Interaction, enlace : str):
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

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frames.append(frame)

                        frames[0].save('img/imagen_cortada.gif', save_all=True, append_images=frames[1:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
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

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frames.append(frame)

                        frames[0].save('img/imagen_cortada.gif', save_all=True, append_images=frames[1:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
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

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frames.append(frame)

                        frames[0].save('img/imagen_cortada.gif', save_all=True, append_images=frames[1:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
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

                        frames = []
                        for frame in ImageSequence.Iterator(self.img_original):
                            frame = frame.crop((self.left, self.top, self.right, self.bottom))
                            frames.append(frame)

                        frames[0].save('img/imagen_cortada.gif', save_all=True, append_images=frames[1:], loop=0)

                        await interaction.response.edit_message(
                            attachments=[discord.File("img/imagen_cortada.gif")],
                            view=cropButtonsH(self.img_original, self.idAutor, self.left, self.top, self.right, self.bottom))
                    else:
                        await interaction.response.send_message(embed=discord.Embed(description=f"❌・Límite de la imagen", color=0xdd6879), ephemeral=True)
                else:
                    await interaction.response.send_message(embed=discord.Embed(description=f"❌・Necesitas haber hecho el comando", color=0xdd6879), ephemeral=True)

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

            bandera = True
        else:
            left = 0
            right = width

            centerH = height / 2

            top = centerH - (heightN/2)
            bottom = centerH + (heightN/2)

            bandera = False

        marco = Image.open("assets/marco.png")

        frames = []
        for frame in ImageSequence.Iterator(img_original):
            frame = frame.crop((left, top, right, bottom))
            frame.resize((225, 350))
            frame.paste(marco, (0, 0), marco)
            frames.append(frame)

        frames[0].save('img/imagen_cortada.gif', save_all=True, append_images=frames[1:], loop=0)

        if bandera == True:
            await interaction.response.send_message(
                file=discord.File("img/imagen_cortada.gif"),
                view=cropButtonsW(img_original, interaction.user.id, left, top, right, bottom))
        else:
            await interaction.response.send_message(
                file=discord.File("img/imagen_cortada.gif"),
                view=cropButtonsH(img_original, interaction.user.id, left, top, right, bottom))
    @cortargif.error
    async def cortargif_error(self, interaction: discord.Interaction, error):
        print(f"Error: {error}")

    # --------------------

    # ----- Ajustes ------

    
    # Muestra el avatar tuyo o de la persona que menciones
    @app_commands.command(name="help", description="Acerca de Choppa")
    async def help(self, interaction: discord.Interaction):
        user = await self.bot.fetch_user(235197855529304064)

        embed = discord.Embed(title = "Acerca de Choppa", description=f"- Este es un bot personal creado con el fin de apoyar y divertir con comandos interactivos.", color=0xdd6879)

        embed.add_field(name=f"Utilidad", value="`avatar`\n`say`\n`ping`\n`fxtwitter`", inline=True)
        embed.add_field(name=f"Entretenimiento", value="`apuntar`\n`quieres`\n`logro`\n`love`", inline=True)
        embed.add_field(name=f"Mudae", value="\n`embedcolor`\n`cortarimagen`\n`cortargif`", inline=True)

        embed.set_image(url="https://i.imgur.com/WPNdviC.png")
        embed.set_footer(text=f"Prefijo: c!", icon_url=interaction.guild.icon)
        embed.set_thumbnail(url=self.bot.user.avatar)

        await interaction.response.send_message(embed=embed)

    # --------------------
    
async def setup(bot):
    await bot.add_cog(Slash_Commands(bot))

# Funciones extras
async def descargar_avatar(avatar):
    with requests.get(avatar) as r:
        img_data = r.content
    with open('img/avatar.png', 'wb') as handler:
        handler.write(img_data)
