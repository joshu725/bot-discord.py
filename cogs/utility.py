# Librerias
import discord
from discord.ext import commands
from discord import app_commands
from colorthief import ColorThief
import requests
from urllib.parse import urlparse
import yt_dlp
import pyktok as pyk
import instaloader
import os
from dotenv import load_dotenv

COLOR = 0xb2b2ff

load_dotenv()
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
INSTAGRAM_USER = os.getenv("INSTAGRAM_USER")

pyk.specify_browser('firefox')

# Clase principal
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Muestra el avatar tuyo o de la persona que menciones
    @commands.hybrid_command(name="avatar", description="Ver el avatar tuyo o de otra persona")
    @app_commands.describe(member = "Usuario que deseas ver su avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        await ctx.defer()
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
    @avatar.error
    async def avatar_error(self, ctx, error):
        print(error)

    # Borra el mensaje y dice exactamente lo mismo que le indiques
    @commands.command()
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)
    
    # Comando para ver la latencia del bot
    @commands.hybrid_command(name="ping", description="Muestra la latencia del bot")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms :ping_pong:")
    
    # Comando para mandar el enlace de Twitter de manera que los videos y las imagenes puedan visualizarse correctamente
    @commands.hybrid_command(name="fxtwitter", description="Manda el enlace de Twitter de manera que los videos y las imagenes puedan visualizarse correctamente")
    @app_commands.describe(enlace = "Enlace de Twitter")
    async def fxtwitter(self, ctx, enlace : str):
        await ctx.defer()
        # Función para verificar validez del enlace y dominio
        def verificar_enlace(url):
            # Verificar si el dominio es "x.com"
            parsed_url = urlparse(url)
            if parsed_url.netloc != "x.com":
                return "El enlace no pertenece a 'x.com'"
            else:
                return "El enlace es válido"

        # Verificación del enlace
        resultado = verificar_enlace(enlace)

        if resultado == "El enlace es válido":
            transformed_url = enlace.replace("x.com", "fxtwitter.com")
            if ctx.message.content.startswith(self.bot.command_prefix):
                await ctx.message.delete()
            await ctx.send(f"{transformed_url}")
        else:
            if resultado == "El enlace no pertenece a 'x.com'":
                await ctx.send(embed=discord.Embed(description=f"❌ El enlace no pertenece a Twitter", color=COLOR), ephemeral=True)
            else:
                await ctx.send(embed=discord.Embed(description=f"❌ Enlace inválido", color=COLOR), ephemeral=True)
    @fxtwitter.error
    async def fxtwitter_error(self, ctx, error):
        print(error)
        await ctx.send(embed=createEmbedInfo("fxtwitter", "Envía el enlace de **Twitter** de manera que los videos e imagenes puedan visualizarse **correctamente**", "!fxtwitter 'https://x.com/ejemplo/status/1234567890'", ctx.author.avatar))

    # Comando para reemplazar el texto indicado
    @commands.hybrid_command(name="reemplazar", description="Comando para reemplazar el texto indicado")
    @app_commands.describe(texto = "Texto original", textoareemplazar = "Texto a reemplazar", reemplazo = "Reemplazo")
    async def reemplazar(self, ctx, texto : str, textoareemplazar : str, reemplazo : str):
        await ctx.send(texto.replace(textoareemplazar, reemplazo))
    @reemplazar.error
    async def reemplazar_error(self, ctx, error):
        print(error)
        await ctx.send(embed=createEmbedInfo("reemplazar", "**Reemplaza** el texto indicado", "/reemplazar 'texto_original' 'texto_a_reemplazar' 'reemplazo'", ctx.author.avatar))

    # Comando para descargar y enviar un video de Youtube
    @commands.hybrid_command(name="youtube", description="Comando para descargar y enviar un video de Youtube")
    @app_commands.describe(enlace = "Enlace de Youtube")
    async def youtube(self, ctx, enlace : str):
        await ctx.defer()
        
        if os.path.exists("video/youtube.mp4"):
            os.remove("video/youtube.mp4")
        
        try:
            ydl_opts = {
                'format': 'bestvideo[height<=720][vcodec^=avc1]+bestaudio/best',
                'outtmpl': f'video/youtube.%(ext)s'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([enlace])
            
            await ctx.send(file=discord.File("video/youtube.mp4"))
        except:
            await ctx.send(embed=discord.Embed(description=f"❌ Error al descargar el video", color=COLOR), ephemeral=True)
    @youtube.error
    async def youtube_error(self, ctx, error):
        print(error)
        if str(error) == "Hybrid command raised an error: Command 'youtube' raised an exception: HTTPException: 413 Payload Too Large (error code: 40005): Request entity too large":
            await ctx.send(embed=discord.Embed(description=f"❌ El vídeo pesa más de 25 MB", color=COLOR), ephemeral=True)
        else:
            await ctx.send(embed=createEmbedInfo("youtube", "Descarga y envía un video o short de **YouTube**", "!youtube 'url'", ctx.author.avatar))

    # Comando para descargar y enviar el audio de un video de Youtube
    @commands.hybrid_command(name="mp3youtube", description="Comando para descargar y enviar el audio de un video de Youtube")
    @app_commands.describe(enlace = "Enlace de Youtube")
    async def mp3youtube(self, ctx, enlace : str):
        await ctx.defer()

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'audio/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
            }],
            'prefer_ffmpeg': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(enlace, download=False)
                file_path = ydl.prepare_filename(info_dict).replace('.m4a', '.mp3')
                ydl.download([enlace])

            await ctx.send(file=discord.File(file_path))
        except:
            await ctx.send(embed=discord.Embed(description=f"❌ Error al descargar el audio del video", color=COLOR), ephemeral=True)
    @mp3youtube.error
    async def mp3youtube_error(self, ctx, error):
        print(error)
        if str(error) == "Hybrid command raised an error: Command 'mp3youtube' raised an exception: HTTPException: 413 Payload Too Large (error code: 40005): Request entity too large":
            await ctx.send(embed=discord.Embed(description=f"❌ El audio pesa más de 25 MB", color=COLOR), ephemeral=True)
        else:
            await ctx.send(embed=createEmbedInfo("mp3youtube", "Descarga y envía el audio de un video de **YouTube**", "!mp3youtube 'url'", ctx.author.avatar))

    # Comando para descargar y enviar un video de TikTok
    @commands.hybrid_command(name="tiktok", description="Comando para descargar y enviar un video de TikTok")
    @app_commands.describe(enlace = "Enlace de TikTok")
    async def tiktok(self, ctx, enlace : str):
        await ctx.defer()
        try:
            pyk.save_tiktok(enlace, True)
            await ctx.send(file=discord.File("video/tiktok.mp4"))
        except:
            await ctx.send(embed=discord.Embed(description=f"❌ Error al descargar el video", color=COLOR), ephemeral=True)
    @tiktok.error
    async def tiktok_error(self, ctx, error):
        print(error)
        if str(error) == "Hybrid command raised an error: Command 'tiktok' raised an exception: HTTPException: 413 Payload Too Large (error code: 40005): Request entity too large":
            await ctx.send(embed=discord.Embed(description=f"❌ El vídeo pesa más de 25 MB", color=COLOR), ephemeral=True)
        else:
            await ctx.send(embed=createEmbedInfo("tiktok", "Descarga y envía un video de **TikTok**", "!tiktok 'url'", ctx.author.avatar))

    # Comando para descargar y enviar un Reel en Instagram
    @commands.hybrid_command(name="reel", description="Comando para descargar y enviar un Reel en Instagram")
    @app_commands.describe(enlace = "Enlace del Reel")
    async def reel(self, ctx, enlace : str):
        if "/reel/" in enlace or "/reels/" in enlace:
            await ctx.defer()
            
            # Crear una instancia de Instaloader
            reel = instaloader.Instaloader()
            
            # Iniciamos sesion en Intagram
            # IMPORTANTE TENER TU ARCHIVO DE INICIO DE SESION CON INSTALOADER
            reel.load_session_from_file(INSTAGRAM_USER)
            
            # Modificamos el enlace en caso de tener el acortador /share/
            if "/share/" in enlace:
                enlace = requests.head(enlace, allow_redirects=True).url
            
            # Extraer el shortcode de la URL
            shortcode = enlace.split("/")[-2]
            
            # Descarga el Reel
            post = instaloader.Post.from_shortcode(reel.context, shortcode)
            reel.filename_pattern = f"{post.owner_username}_{shortcode}"
            reel.download_post(post, "download")
            
            # Se elimina el anterior Reel
            if os.path.exists("video/instagram/"):
                for file in os.listdir(os.path.join("video", "instagram")):
                    os.remove(os.path.join(os.path.join("video", "instagram"), file))
            
            # Se renombra y se mueve el Reel, ademas de borrar los demás archivos innecesarios
            for file in os.listdir("download"):
                ruta_origen = os.path.join("download", file)
                ruta_destino = os.path.join("video", "instagram", file)
                
                if file.endswith(".mp4"):
                    os.rename(ruta_origen, ruta_destino)
                else:
                    os.remove(ruta_origen)
            
            await ctx.send(file=discord.File(f"video/instagram/{reel.filename_pattern}.mp4"))
        else:
            await ctx.send(embed=discord.Embed(description=f"❌ El enlace no es un Reel, utiliza el comando `/instagram` para una publicación en Instagram.", color=COLOR), ephemeral=True)
    @reel.error
    async def reel_error(self, ctx, error):
        print(error)
        if str(error) == "Hybrid command raised an error: Command 'reel' raised an exception: HTTPException: 413 Payload Too Large (error code: 40005): Request entity too large":
            await ctx.send(embed=discord.Embed(description=f"❌ El Reel pesa más de 25 MB", color=COLOR), ephemeral=True)
        else:
            await ctx.send(embed=createEmbedInfo("reel", "Descarga y envía un Reel en **Instagram**", "!reel 'url'", ctx.author.avatar))

    # Comando para visualizar en grande un emoji custom
    @commands.hybrid_command(name="emoji", description="Comando para visualizar en grande un emoji custom", aliases=["e"])
    @app_commands.describe(emoji = "Emoji custom")
    async def emoji(self, ctx, emoji : discord.Emoji):
        embed=discord.Embed(title=f":{emoji.name}:", description=f"[URL]({emoji.url})", color = discord.Color(COLOR))
        embed.set_image(url=f"{emoji.url}")
        await ctx.send(embed=embed)
    @emoji.error
    async def emoji_error(self, ctx, error):
        print(error)
        await ctx.send(embed=createEmbedInfo("emoji", "Visualiza en grande un **emoji custom**", "!emoji ':emoji_custom:'", ctx.author.avatar))

    # Comando para subir enlace de imagen o gif a Imgur
    @commands.hybrid_command(name="imgur", description="Comando para subir enlace de imagen o gif a Imgur")
    @app_commands.describe(enlace = "Enlace de la imagen o gif")
    async def imgur(self, ctx, enlace : str):
        await ctx.defer()
        headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
        data = {"image": enlace}

        response = requests.post("https://api.imgur.com/3/upload", headers=headers, data=data)

        if response.status_code == 200:
            imgur_link = response.json()['data']['link']
            embed = discord.Embed(
                description=f"```{imgur_link}```",
                color = discord.Color(COLOR)
            )
            embed.set_image(url=imgur_link)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(description=f"❌ No se ha podido subir el enlace", color=COLOR))
    @imgur.error
    async def imgur_error(self, ctx, error):
        print(error)
        await ctx.send(embed=createEmbedInfo("imgur", "Sube un enlace de imagen o gif a **Imgur**", "!imgur 'url'", ctx.author.avatar))

    # Comando para descargar y enviar imagenes/videos de una publicación en Instagram
    @commands.hybrid_command(name="instagram", description="Comando para descargar y enviar imagenes/videos de una publicación en Instagram")
    @app_commands.describe(enlace = "Enlace de la publicación en Instagram")
    async def instagram(self, ctx, enlace : str):
        if "/p/" in enlace:
            await ctx.defer()
            
            # Crear una instancia de Instaloader
            reel = instaloader.Instaloader()
            
            # Iniciamos sesion en Intagram
            # IMPORTANTE TENER TU ARCHIVO DE INICIO DE SESION CON INSTALOADER
            reel.load_session_from_file(INSTAGRAM_USER)
            
            # Extraer el shortcode de la URL
            shortcode = enlace.split("/")[-2]
            
            # Descargar los archivos de la publicación
            post = instaloader.Post.from_shortcode(reel.context, shortcode)
            reel.filename_pattern = f"{post.owner_username}_{shortcode}"
            reel.download_post(post, "download")
            
            # Se eliminan los anteriores archivos
            if os.path.exists("img/instagram/"):
                for file in os.listdir(os.path.join("img", "instagram")):
                    os.remove(os.path.join(os.path.join("img", "instagram"), file))
            
            # Se renombra y se mueve los archivos
            for file in os.listdir("download"):
                ruta_origen = os.path.join("download", file)
                ruta_destino = os.path.join("img", "instagram", file)
                
                if file.endswith(".mp4") or file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    os.rename(ruta_origen, ruta_destino)
                    await ctx.send(file=discord.File(f"img/instagram/{file}"))
                else:
                    os.remove(ruta_origen)
            
        else:
            await ctx.send(embed=discord.Embed(description=f"❌ El enlace no es una publicación en Instagram, utiliza el comando `/reel` para un Reel en Instagram.", color=COLOR), ephemeral=True)
    @instagram.error
    async def instagram_error(self, ctx, error):
        print(error)
        await ctx.send(embed=createEmbedInfo("instagram", "Descarga y envia imagenes/videos de una publicación en **Instagram**", "!instagram 'url'", ctx.author.avatar))

    # Comando para descargar y enviar un video de Twitter
    @commands.hybrid_command(name="twitter", description="Comando para descargar y enviar un video de Twitter (X)")
    @app_commands.describe(enlace = "Enlace de Twitter (X)")
    async def twitter(self, ctx, enlace : str):
        await ctx.defer()
        
        if os.path.exists("video/twitter.mp4"):
            os.remove("video/twitter.mp4")
        
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'video/twitter.%(ext)s'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([enlace])
            
            await ctx.send(file=discord.File("video/twitter.mp4"))
        except:
            await ctx.send(embed=discord.Embed(description=f"❌ Error al descargar el video", color=COLOR), ephemeral=True)
    @twitter.error
    async def twitter_error(self, ctx, error):
        print(error)
        if str(error) == "Hybrid command raised an error: Command 'twitter' raised an exception: HTTPException: 413 Payload Too Large (error code: 40005): Request entity too large":
            await ctx.send(embed=discord.Embed(description=f"❌ El vídeo pesa más de 25 MB", color=COLOR), ephemeral=True)
        else:
            await ctx.send(embed=createEmbedInfo("twitter", "Descarga y envía un video de **Twitter** (X)", "!twitter 'url'", ctx.author.avatar))


async def setup(bot):
    await bot.add_cog(Utility(bot))

def createEmbedInfo(comando : str, especificacion : str, formato : str, urlIcono : str):
    embed = discord.Embed(description = especificacion, color = COLOR)
    embed.set_author(name = comando, icon_url = urlIcono)
    embed.add_field(name = "🗒️ Formato", value=f"`{formato}`", inline=False)
    return embed