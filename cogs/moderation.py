# Librerias
import discord
from discord.ext import commands
from discord import app_commands, utils

from humanfriendly import parse_timespan, format_timespan, InvalidTimespan
from typing import Optional
from datetime import timedelta

COLOR = 0xffa3a3

# Clase principal
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")
    
    # Comando para eliminar la cantidad de mensajes especificada
    @commands.hybrid_command(name="prune", description="Elimina la cantidad de mensajes especificada")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(cantidad="Cantidad de mensajes que deseas eliminar")
    async def prune(self, ctx, cantidad : commands.Range[int, 1]):
        if cantidad > 100:
            return await ctx.send(embed=discord.Embed(description = "❌ La cantidad de mensajes no puede ser mayor a 100", color = COLOR))

        if not ctx.interaction:
            await ctx.message.delete()
        else:
            await ctx.defer(ephemeral=True)
        
        await ctx.channel.purge(limit=cantidad)

        if ctx.interaction:
            await ctx.send(f"Se han eliminado {cantidad} mensajes", ephemeral=True, delete_after=3)
    @prune.error
    async def prune_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("prune", "**Elimina** la cantidad de mensajes especificada", "!prune 'cantidad'", ctx.author.avatar))

    # Comando para expulsar a un miembro del servidor
    @commands.hybrid_command(name="kick", description="Expulsa a un miembro del servidor")
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(miembro="Miembro a expulsar", razon="Razón de la expulsión")
    async def kick(self, ctx, miembro: discord.Member, *, razon: Optional[str]):
        await miembro.kick(reason=razon)
        embed = embed=discord.Embed(description = f"{miembro.mention} ha sido **expulsado** del servidor", color = COLOR)
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar)
        embed.set_thumbnail(url=miembro.avatar)
        if razon:
            embed.add_field(name = "✏️ Razón", value=razon, inline=False)
        await ctx.send(embed=embed)
    @kick.error
    async def kick_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("kick", "**Expulsa** del servidor a la persona indicada", "!kick '@miembro' 'razón'", ctx.author.avatar))

    # Comando para banear a un miembro del servidor
    @commands.hybrid_command(name="ban", description="Banea a un miembro del servidor")
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(miembro="Miembro a banear", razon="Razón del baneo")
    async def ban(self, ctx, miembro: discord.Member, *, razon: Optional[str]):
        await miembro.ban(reason=razon)
        embed = embed=discord.Embed(description = f"{miembro.mention} ha sido **baneado** del servidor", color = COLOR)
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar)
        embed.set_thumbnail(url=miembro.avatar)
        if razon:
            embed.add_field(name = "✏️ Razón", value=razon, inline=False)
        await ctx.send(embed=embed)
    @ban.error
    async def ban_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("ban", "**Banea** del servidor a la persona indicada", "!ban '@miembro' 'razón'", ctx.author.avatar))

    # Comando para silenciar a un miembro del servidor
    @commands.hybrid_command(name="mute", description="Silencia a un miembro del servidor")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(miembro="Miembro a silenciar", duracion="Duración del silencio", razon="Razón del silencio")
    async def mute(self, ctx, miembro: discord.Member, duracion : Optional[str]="2h", *, razon: Optional[str]):
        try:
            duracion = parse_timespan(duracion)
        except InvalidTimespan:
            return await ctx.send(embed=discord.Embed(description = "❌ Formato de duración incorrecto **(1s, 1m, 1h, 1d)**", color = COLOR))
        
        await miembro.timeout(utils.utcnow() + timedelta(seconds=duracion), reason=razon)
        
        embed = embed=discord.Embed(description = f"{miembro.mention} ha sido **silenciado** del servidor durante **{format_timespan(duracion)}**", color = COLOR)
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar)
        embed.set_thumbnail(url=miembro.avatar)
        if razon:
            embed.add_field(name = "✏️ Razón", value=razon, inline=False)
        await ctx.send(embed=embed)
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("mute", "**Silencia** del servidor a la persona indicada", "!mute '@miembro' 'duración : 1s 1m 1h 1d' 'razón'", ctx.author.avatar))

    # Comando para quitar el silencio a un miembro del servidor
    @commands.hybrid_command(name="unmute", description="Desilencia a un miembro del servidor")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(miembro="Miembro a desilenciar")
    async def unmute(self, ctx, miembro: discord.Member):
        if not miembro.is_timed_out():
            return await ctx.send(embed=discord.Embed(description = "❌ El usuario no está silenciado", color = COLOR))
        
        await miembro.timeout(None)
        
        embed = embed=discord.Embed(description = f"{miembro.mention} ha sido **desilenciado**", color = COLOR)
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar)
        embed.set_thumbnail(url=miembro.avatar)
        await ctx.send(embed=embed)
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("unmute", "**Desilencia** del servidor a la persona indicada", "!unmute '@miembro'", ctx.author.avatar))

async def setup(bot):
    await bot.add_cog(Moderation(bot))

def createEmbedInfo(comando : str, especificacion : str, formato : str, urlIcono : str):
    embed = discord.Embed(description = especificacion, color = COLOR)
    embed.set_author(name = comando, icon_url = urlIcono)
    embed.add_field(name = "🗒️ Formato", value=f"`{formato}`", inline=False)
    return embed