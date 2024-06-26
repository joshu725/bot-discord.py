# Librerias
import discord
from discord.ext import commands
from discord import app_commands

class Slash_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")

    # Comando de prueba
    @app_commands.command(name="prueba", description="Probar comandos con slash")
    async def prueba(self, interaction: discord.Interaction):
        await interaction.response.send_message("Comando slash de prueba :)")

async def setup(bot):
    await bot.add_cog(Slash_Commands(bot))