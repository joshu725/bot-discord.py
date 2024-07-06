# Librerias
import discord
from discord.ext import commands
from discord import app_commands
import requests
import random
from PIL import Image, ImageDraw, ImageFont

# Clase principal
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Comando meme "apuntar"
    @commands.hybrid_command(name="apuntar", description="Comando meme \"apuntar\"  que utiliza el avatar del usuario")
    @app_commands.describe(member = "Usuario con el que deseas aplicar este comando")
    async def apuntar(self, ctx, member : discord.Member=None):
        await ctx.defer()
        if member == None:
            await descargar_avatar(ctx.author.avatar)
        else:
            await descargar_avatar(member.avatar)
        avatar = Image.open("img/avatar.png")
        avatar = avatar.resize((512, 512))
        pistola = Image.open("assets/gun.png")
        pistola = pistola.resize((200, 200))
        avatar.paste(pistola, (300, 300), pistola)
        avatar.save("img/avatar.png")
        await ctx.send(file=discord.File("img/avatar.png"))
    
    # Comando meme "quieres?"
    @commands.hybrid_command(name="quieres", description="Comando meme \"quieres\" que utiliza el avatar del usuario")
    @app_commands.describe(member = "Usuario con el que deseas aplicar este comando")
    async def quieres(self, ctx, member : discord.Member=None):
        await ctx.defer()
        if member == None:
            await descargar_avatar(ctx.author.avatar)
        else:
            await descargar_avatar(member.avatar)
        avatar = Image.open("img/avatar.png")
        avatar = avatar.resize((512, 512))
        quieres = Image.open("assets/quieres.png")
        quieres = quieres.resize((512, 512))
        avatar.paste(quieres, (0, 0), quieres)
        avatar.save("img/avatar.png")
        await ctx.send(file=discord.File("img/avatar.png"))

    # Comando para determinar aleatoriamente la compatibilidad entre personas
    @commands.command()
    async def love(self, ctx, *member: discord.Member):
        p=random.randrange(1,101)
        if p >= 1 and p <= 10:
            porcentaje= f"💖 `██                  ` 💖  **{p}%**"
        if p > 10 and p <= 20:
            porcentaje= f"💖 `████                ` 💖  **{p}%**"
        if p > 20 and p <= 30:
            porcentaje= f"💖 `██████              ` 💖  **{p}%**"
        if p > 30 and p <= 40:
            porcentaje= f"💖 `████████            ` 💖  **{p}%**"
        if p > 40 and p <= 50:
            porcentaje= f"💖 `██████████          ` 💖  **{p}%**"
        if p > 50 and p <= 60:
            porcentaje= f"💖 `████████████        ` 💖  **{p}%**"
        if p > 60 and p <= 70:
            porcentaje= f"💖 `██████████████      ` 💖  **{p}%**"
        if p > 70 and p <= 80:
            porcentaje= f"💖 `████████████████    ` 💖  **{p}%**"
        if p > 80 and p <= 90:
            porcentaje= f"💖 `██████████████████  ` 💖  **{p}%**"
        if p > 90 and p <= 100:
            porcentaje= f"💖 `████████████████████` 💖  **{p}%**"

        if len(member) == 0:
            await ctx.send(embed=discord.Embed(description=f"**Menciona a dos usuarios para ver su porcentaje de amor**\n\n`c!love @usuario1 @usuario2`", color=0xdd6879))
        if len(member) == 1:
            embed = discord.Embed(title=f"{ctx.author.display_name} & {member[0].display_name}", description=porcentaje, color=0xdd6879)
            embed.set_thumbnail(url="https://i.imgur.com/sCFJA7V.gif")
            await ctx.send(embed=embed)
        if len(member) == 2:
            if member[0].id == 235197855529304064:
                if member[1].id == 263880901094539266:
                    embed=discord.Embed(title=f"{member[0].display_name} & {member[1].display_name}",description="💖 `████████████████████` 💖  **100%**", color=0xdd6879)
                    embed.set_thumbnail(url="https://i.imgur.com/sCFJA7V.gif")
                    await ctx.send(embed=embed)
            elif member[0].id == 263880901094539266:
                if member[1].id == 235197855529304064:
                    embed=discord.Embed(title=f"{member[0].display_name} & {member[1].display_name}",description="💖 `████████████████████` 💖  **100%**", color=0xdd6879)
                    embed.set_thumbnail(url="https://i.imgur.com/sCFJA7V.gif")
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title=f"{member[0].display_name} & {member[1].display_name}",description=porcentaje, color=0xdd6879)
                embed.set_thumbnail(url="https://i.imgur.com/sCFJA7V.gif")
                await ctx.send(embed=embed)
        if len(member) > 2:
            await ctx.send(embed=discord.Embed(description=f"**Menciona a dos usuarios para ver su porcentaje de amor**\n\n`c!love @usuario1 @usuario2`", color=0xdd6879))

    # Comando para mandar una imagen del logro de Minecraft con los carácteres que indiquemos
    @commands.hybrid_command(name="logro", description="Comando para mandar una imagen del logro de Minecraft con el texto que indiquemos")
    @app_commands.describe(texto = "Texto a indicar (21 carácteres máximo)")
    async def logro(self, ctx, texto : str = None):
        if texto == None:
            await ctx.send(embed=discord.Embed(description=f"**Crea tu propio logro al estilo Minecraft** \n\n`c!logro \"texto\"` (21 carácteres máximo)", color=0xdd6879))
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

            await ctx.send(file=discord.File("assets/logro_minecraft/minecraft_logro.png"))
        else:
            await ctx.send(embed=discord.Embed(description=f"❌・21 carácteres máximo", color=0xdd6879), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Fun(bot))

# Funciones extras
async def descargar_avatar(avatar):
    with requests.get(avatar) as r:
        img_data = r.content
    with open('img/avatar.png', 'wb') as handler:
        handler.write(img_data)