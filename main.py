# Librerias
import discord
from discord.ext import commands
import os
import asyncio
from datetime import datetime

# Configuración inicial
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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