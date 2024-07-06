# Librerias
import discord
from discord.ext import commands
from discord import app_commands
from colorthief import ColorThief
import requests
from urllib.parse import urlparse
from pytube import YouTube
import pyktok as pyk

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
            if ctx.message.content.startswith(self.bot.command_prefix):
                await ctx.message.delete()
            await ctx.send(f"{transformed_url}")
        else:
            if resultado == "El enlace no pertenece a 'x.com'":
                await ctx.send(embed=discord.Embed(description=f"❌・El enlace no pertenece a Twitter", color=0xdd6879), ephemeral=True)
            else:
                await ctx.send(embed=discord.Embed(description=f"❌・Enlace inválido", color=0xdd6879), ephemeral=True)

    # Comando para reemplazar el texto indicado
    @commands.hybrid_command(name="reemplazar", description="Comando para reemplazar el texto indicado")
    @app_commands.describe(texto = "Texto original", textoareemplazar = "Texto a reemplazar", reemplazo = "Reemplazo")
    async def reemplazar(self, ctx, texto : str, textoareemplazar : str, reemplazo : str):
        await ctx.send(texto.replace(textoareemplazar, reemplazo))
    @reemplazar.error
    async def reemplazar_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(description=f"❌・`/reemplazar`", color=0xdd6879), ephemeral=True)

    # Comando para descargar y enviar un video de Youtube
    @commands.hybrid_command(name="youtube", description="Comando para descargar y enviar un video de Youtube")
    @app_commands.describe(enlace = "Enlace de Youtube")
    async def youtube(self, ctx, enlace : str):
        try: 
            yt = YouTube(enlace) 
        except: 
            await ctx.send(embed=discord.Embed(description=f"❌・No se ha encontrado el video", color=0xdd6879), ephemeral=True)
            return
        
        await ctx.defer()
        
        # Obtener la mejor calidad disponible
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()

        try: 
            video.download(output_path="video", filename="youtube.mp4")
            await ctx.send(file=discord.File("video/youtube.mp4"))
        except: 
            await ctx.send(embed=discord.Embed(description=f"❌・Error al descargar el video", color=0xdd6879))
    @youtube.error
    async def youtube_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(description=f"❌・No se ha encontrado el video", color=0xdd6879), ephemeral=True)

    # Comando para descargar y enviar un video de TikTok
    @commands.hybrid_command(name="tiktok", description="Comando para descargar y enviar un video de TikTok")
    @app_commands.describe(enlace = "Enlace de TikTok")
    async def tiktok(self, ctx, enlace : str):
        await ctx.defer()
        pyk.specify_browser('brave')
        pyk.save_tiktok(enlace, True) # Para guardar el archivo con un nombre especifico tuve que modificar la librería pyktok
        await ctx.send(file=discord.File("video/tiktok.mp4"))
    @tiktok.error
    async def tiktok_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(description=f"❌・Error al descargar el video", color=0xdd6879), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))