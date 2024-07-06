# Librerias
import discord
from discord.ext import commands
from colorthief import ColorThief
import requests
from urllib.parse import urlparse

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
    
    # Comando para ver la latencia del bot
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms :ping_pong:")
    
    # Comando para mandar el enlace de Twitter de manera que los videos y las imagenes puedan visualizarse correctamente
    @commands.command()
    async def fxtwitter(self, ctx, enlace : str = None):
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
            await ctx.message.delete()
            await ctx.send(f"<@{ctx.author.id}> {transformed_url}")
        else:
            if resultado == "El enlace no pertenece a 'x.com'":
                await ctx.send(content=f"<@{ctx.author.id}>", embed=discord.Embed(description=f"❌・El enlace no pertenece a Twitter", color=0xdd6879))
            else:
                await ctx.send(content=f"<@{ctx.author.id}>", embed=discord.Embed(description=f"❌・Enlace inválido", color=0xdd6879))
        
async def setup(bot):
    await bot.add_cog(Utility(bot))