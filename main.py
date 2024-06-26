# Librerias
import discord
from discord.ext import commands, tasks
from discord import app_commands

import os
import asyncio

# Librerias extra
from datetime import datetime

# Configuración inicial
bot = commands.Bot(command_prefix='c!', intents=discord.Intents.all())

bot.remove_command("help")

# Evento que indica la conexión del bot
@bot.event
async def on_ready():
    print("")
    print('+--------------------------------+')
    print(f"|    Conectado en {bot.user}    |")
    print('+--------------------------------+')
    hora = datetime.now()
    print(hora.strftime("      Hora actual: %H:%M:%S\n"))

    await bot.change_presence(activity=discord.Game(name="🍧 c!help"))
    
    try:
        synced = await bot.tree.sync()
        print(f"\nComandos slash sincronizados: {len(synced)}\n")
    except Exception as e:
        print(e)

# Función para cargar los cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Comando para recargar los cogs
@bot.command(aliases=['re'])
@commands.has_permissions(administrator=True)
async def reload(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.reload_extension(f"cogs.{filename[:-3]}")
            await ctx.message.add_reaction('✅')
@reload.error
async def reload_error(ctx, error):
    await ctx.message.add_reaction('❌')

# Comando informativo
@bot.command()
async def help(ctx):
    user = await bot.fetch_user(235197855529304064)

    embed = discord.Embed(title = "Acerca de Choppa", description=f"- Este es un bot personal creado con el fin de apoyar y divertir con comandos interactivos.", color=0xdd6879)

    embed.add_field(name=f"Utilidad", value="`avatar`\n`say`\n`ping`", inline=True)
    embed.add_field(name=f"Entretenimiento", value="`apuntar`\n`quieres`\n`logro`\n`love`", inline=True)
    embed.add_field(name=f"Mudae", value="\n`embedcolor` (ec)\n`cortarimagen` (ci)", inline=True)

    embed.set_image(url="https://i.imgur.com/WPNdviC.png")
    embed.set_footer(text=f"Prefijo: c!", icon_url=ctx.guild.icon)
    embed.set_thumbnail(url=bot.user.avatar)

    await ctx.send(embed=embed)

# --- Inicio de bot ---

# Lectura de archivo que contiene el token del bot
with open("token.txt") as file:
    token = file.read()

# Función principal que carga los cogs e inicia el bot
async def main():
    async with bot:
        await load()
        await bot.start(token)

# Se ejectuta la función principal
asyncio.run(main())
