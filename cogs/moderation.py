# Librerias
import discord
from discord.ext import commands
from discord import app_commands, utils
import os
import json
from humanfriendly import parse_timespan, format_timespan, InvalidTimespan
from typing import Optional
from datetime import timedelta, datetime

COLOR = 0xffa3a3

# Clase principal
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Si no existe el archivo de warns, se creará
        if not os.path.exists("assets/warnings.json"):
            with open("assets/warnings.json", "w") as file:
                json.dump({}, file, indent=4)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} conectado")
    
    # Comando para eliminar la cantidad de mensajes especificada
    @commands.hybrid_command(name="prune", description="Elimina la cantidad de mensajes especificada")
    @commands.has_guild_permissions(manage_messages=True)
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
            await ctx.send(embed=createEmbedInfo("prune", "**Elimina** la cantidad de mensajes especificada", "!prune 'cantidad'", "!prune 10", ctx.author.avatar))

    # Comando para expulsar a un miembro del servidor
    @commands.hybrid_command(name="kick", description="Expulsa a un miembro del servidor")
    @commands.has_guild_permissions(kick_members=True)
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
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("kick", "**Expulsa** del servidor a la persona indicada", "!kick '@miembro' 'razón'", "!kick @Albert Molestar en exceso", ctx.author.avatar))

    # Comando para banear a un miembro del servidor
    @commands.hybrid_command(name="ban", description="Banea a un miembro del servidor")
    @commands.has_guild_permissions(ban_members=True)
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
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("ban", "**Banea** del servidor a la persona indicada", "!ban '@miembro' 'razón'", "!ban @Albert Demasiadas llamadas de atención", ctx.author.avatar))

    # Comando para remover el baneo de un usuario
    @commands.hybrid_command(name="unban", description="Remueve el baneo de un usuario")
    @commands.has_guild_permissions(ban_members=True)
    @app_commands.describe(id="ID del miembro a remover su baneo")
    async def unban(self, ctx, id: int):
        # Obtenemos al usuario a partir de su ID
        usuario = await ctx.bot.fetch_user(id)
        # Removemos el baneo
        try:
            await ctx.guild.unban(usuario)
            embed = embed=discord.Embed(description = f"Se ha **removido** el **baneo** del usuario {usuario.mention}", color = COLOR)
            embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar)
            embed.set_thumbnail(url=usuario.avatar)
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=discord.Embed(description = "❌ No se ha podido remover el baneo", color = COLOR))
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("unban", "**Remueve** el **baneo** de un usuario mediante su ID", "!unban 'id'", "!unban 200393923456781386", ctx.author.avatar))

    # Comando para silenciar a un miembro del servidor
    @commands.hybrid_command(name="mute", description="Silencia a un miembro del servidor")
    @commands.has_guild_permissions(manage_messages=True)
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
            await ctx.send(embed=createEmbedInfo("mute", "**Silencia** del servidor a la persona indicada", "!mute '@miembro' 'duración : 1s 1m 1h 1d' 'razón'", "!mute @Albert 4h Insultar con frecuencia", ctx.author.avatar))

    # Comando para quitar el silencio a un miembro del servidor
    @commands.hybrid_command(name="unmute", description="Desilencia a un miembro del servidor")
    @commands.has_guild_permissions(manage_messages=True)
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
            await ctx.send(embed=createEmbedInfo("unmute", "**Desilencia** del servidor a la persona indicada", "!unmute '@miembro'", "!unmute @Albert", ctx.author.avatar))

    # Comando para dar una advertencia a un miembro del servidor
    @commands.hybrid_command(name="warn", description="Advierte a un miembro del servidor")
    @commands.has_guild_permissions(kick_members=True)
    @app_commands.describe(miembro = "Miembro a advertir", razon = "Razon de la advertencia")
    async def warn(self, ctx, miembro: discord.Member, *, razon: str):
        # Cargamos los anteriores datos existentes
        data = {}
        with open('assets\\warns.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}

        # Comprobamos que el servidor esté en los datos del JSON
        server_id = str(ctx.message.guild.id)
        if server_id not in data:
            data[server_id] = {}

        # Comprobamos que el usuario esté en los datos del JSON
        user_id = str(miembro.id)
        if user_id not in data[server_id]:
            data[server_id][user_id] = {}
        
        # Se agrega la nueva advertencia con su ID correspondiente
        warning_id = str(ctx.message.id)
        data[server_id][user_id][warning_id] = {
            "date": str(ctx.message.created_at),
            "by": ctx.message.author.id,
            "reason": razon
        }
        
        # Se actualiza el .json
        with open('assets\\warns.json', 'w') as file:
            json.dump(data, file, indent = 4)
        
        # Se envia el mensaje para confirmar que el usuario fue advertido
        embed = embed=discord.Embed(description = f"{miembro.mention} ha sido **advertido**", color = COLOR)
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar)
        embed.set_thumbnail(url=miembro.avatar)
        embed.add_field(name = "✏️ Razón", value=razon, inline=False)
        await ctx.send(embed=embed)
    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = "❌ No tienes los permisos necesarios para realizar eso", color = COLOR))
        else:
            await ctx.send(embed=createEmbedInfo("warn", "**Advierte** a un miembro del servidor", "!warn '@miembro' 'formato de razón'", "!warn @Albert Por decir una palabra prohibida", ctx.author.avatar))

    # Comando para ver una lista de las advertencias que tiene un miembro del servidor
    @commands.hybrid_command(name="warnings", description="Permite ver una lista de las advertencias que tiene un miembro del servidor")
    @app_commands.describe(miembro = "Miembro a visualizar sus advertencias")
    async def warnings(self, ctx, miembro: discord.Member):
        # Abrir el archivo JSON
        with open('assets\\warnings.json', 'r') as file:
            data = json.load(file)
        
        # Comprobar si el servidor y el miembro existen en el JSON
        guild_id = str(ctx.message.guild.id)
        miembro_id = str(miembro.id)
        if guild_id not in data or miembro_id not in data[guild_id] or not data[guild_id][miembro_id]:
            await ctx.send(embed=discord.Embed(description = f"📄 {miembro.mention} no tiene advertencias", color = COLOR), ephemeral=True)
            return
        
        # Se guarda las advertencias que tiene el usuario en una variable
        advertencias = data[guild_id][miembro_id]
        
        # Crear el embed
        embed = embed=discord.Embed(color = COLOR)
        embed.set_author(name = f"El usuario {miembro.display_name} tiene {len(advertencias)} advertencias", icon_url = miembro.avatar)
        
        # Iterar sobre las advertencias del miembro
        for warn_id, warn in advertencias.items():
            razon = warn.get("reason")
            moderador = await ctx.bot.fetch_user(warn.get("by"))
            
            # Primero convertimos nuestra fecha str en objeto datetime, despues lo pasamos a formato epoch para poder usarlo directamente como un timestamp en el embed
            fechaEpoch = int((datetime.fromisoformat(warn.get("date"))).timestamp())
            
            embed.add_field(
                name=f"👤 {moderador.display_name}",
                value=f"{razon} - <t:{fechaEpoch}:R>",
                inline=False
            )
        
        await ctx.send(embed=embed, ephemeral=True)
    @warnings.error
    async def warnings_error(self, ctx, error):
        print(error)
        await ctx.send(embed=createEmbedInfo("warnings", "Permite ver una **lista** de las **advertencias** que tiene un miembro", "!warnings '@miembro'", "!warnings @Albert", ctx.author.avatar), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))

def createEmbedInfo(comando : str, especificacion : str, formato : str, ejemplo : str, urlIcono : str):
    embed = discord.Embed(description = especificacion, color = COLOR)
    embed.set_author(name = comando, icon_url = urlIcono)
    embed.add_field(name = "🗒️ Formato", value=f"`{formato}`", inline=False)
    embed.add_field(name= "✏️ Ejemplo", value=f"`{ejemplo}`", inline=False)
    return embed