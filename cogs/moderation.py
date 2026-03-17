import discord
from discord.ext import commands
from datetime import timedelta
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        reason = reason or "Sebep belirtilmedi"
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="🔨 Kick",
                description=f"{member} sunucudan atildi!",
                color=discord.Color.red()
            )
            embed.add_field(name="Sebep", value=reason, inline=True)
            embed.add_field(name="Yetkili", value=ctx.author, inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, days: int = 0, *, reason=None):
        reason = reason or "Sebep belirtilmedi"
        try:
            await member.ban(reason=reason, delete_message_days=days)
            embed = discord.Embed(
                title="🔨 Ban",
                description=f"{member} sunucudan banlandi!",
                color=discord.Color.red()
            )
            embed.add_field(name="Sebep", value=reason, inline=True)
            embed.add_field(name="Yetkili", value=ctx.author, inline=True)
            if days > 0:
                embed.add_field(name="Silinen mesajlar", value=f"{days} gun", inline=True)
            await ctx.send(embed=embed)
            
            cursor = await self.bot.db.execute(
                "INSERT INTO bans (user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
                (str(member.id), str(ctx.guild.id), str(ctx.author.id), reason)
            )
            await self.bot.db.commit()
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str = None):
        if not user_id:
            await ctx.send("Kullanim: h!unban <user_id>")
            return
        try:
            user_id = user_id.replace('<@', '').replace('>', '').replace('!', '')
            user = await self.bot.fetch_user(int(user_id))
            await ctx.guild.unban(user)
            await ctx.send(f"✅ {user} banı kaldırıldı!")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, sure: int = 30, *, reason=None):
        reason = reason or "Sebep belirtilmedi"
        try:
            until = discord.utils.utcnow() + timedelta(minutes=sure)
            await member.timeout(until, reason=reason)
            
            cursor = await self.bot.db.execute(
                "INSERT INTO mutes (user_id, server_id, moderator_id, reason, expires_at) VALUES (?, ?, ?, ?, ?)",
                (str(member.id), str(ctx.guild.id), str(ctx.author.id), reason, int(until.timestamp()))
            )
            await self.bot.db.commit()
            
            embed = discord.Embed(
                title="🔇 Mute",
                description=f"{member} {sure} dakika susturuldu!",
                color=discord.Color.orange()
            )
            embed.add_field(name="Sebep", value=reason, inline=True)
            embed.add_field(name="Yetkili", value=ctx.author, inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        try:
            await member.timeout(None)
            await ctx.send(f"✅ {member} artik konusabilir!")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        reason = reason or "Sebep belirtilmedi"
        cursor = await self.bot.db.execute(
            "INSERT INTO warns (user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (str(member.id), str(ctx.guild.id), str(ctx.author.id), reason)
        )
        await self.bot.db.commit()
        
        cursor = await self.bot.db.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id = ? AND server_id = ?",
            (str(member.id), str(ctx.guild.id))
        )
        count = (await cursor.fetchone())[0]
        
        embed = discord.Embed(
            title="⚠️ Warn",
            description=f"{member} uyarildi!",
            color=discord.Color.orange()
        )
        embed.add_field(name="Sebep", value=reason, inline=True)
        embed.add_field(name="Toplam uyari", value=str(count), inline=True)
        embed.add_field(name="Yetkili", value=ctx.author, inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='warns')
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        cursor = await self.bot.db.execute(
            "SELECT * FROM warns WHERE user_id = ? AND server_id = ? ORDER BY created_at DESC",
            (str(member.id), str(ctx.guild.id))
        )
        warns = await cursor.fetchall()
        
        if not warns:
            await ctx.send(f"{member} icin uyari yok!")
            return
        
        embed = discord.Embed(
            title=f"⚠️ {member} Uyari Listesi",
            description=f"Toplam: {len(warns)} uyari",
            color=discord.Color.orange()
        )
        
        for i, warn in enumerate(warns[:10], 1):
            mod = self.bot.get_user(int(warn[3]))
            mod_name = mod.name if mod else "Bilinmiyor"
            embed.add_field(
                name=f"Uyari #{i}",
                value=f"**Sebep:** {warn[4]}\n**Yetkili:** {mod_name}\n**Tarih:** <t:{warn[5]}:R>",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='sil', aliases=['temizle'])
    @commands.has_permissions(manage_messages=True)
    async def sil(self, ctx, amount: int = 10):
        if amount < 1:
            amount = 1
        elif amount > 500:
            await ctx.send("❌ **Hata!** Lütfen 1-500 arası sayı giriniz.")
            return
        
        deleted = await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title="🗑️ Temizle",
            description=f"{len(deleted)} mesaj silindi!",
            color=discord.Color.green()
        )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()
    
    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, sure: int = None):
        if sure is None:
            current = ctx.channel.slowmode_delay
            await ctx.send(f"Mevcut slowmode: {current} saniye")
            return
        
        if sure == 0:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send("✅ Slowmode kapatildi!")
        else:
            await ctx.channel.edit(slowmode_delay=sure)
            await ctx.send(f"✅ Slowmode {sure} saniye yapildi!")
    
    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"🔒 {channel} kilitlendi!")
    
    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=None)
        await ctx.send(f"🔓 {channel} kilidi acildi!")
    
    @commands.command(name='rolver')
    @commands.has_permissions(manage_roles=True)
    async def rolever(self, ctx, member: discord.Member, *, role: discord.Role):
        try:
            await member.add_roles(role)
            await ctx.send(f"✅ {member} adli kullaciya {role} rolü verildi!")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='rolal')
    @commands.has_permissions(manage_roles=True)
    async def rolal(self, ctx, member: discord.Member, *, role: discord.Role):
        try:
            await member.remove_roles(role)
            await ctx.send(f"✅ {member} adli kullanicidan {role} rolü alindi!")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='kullanici')
    async def kullanici(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Sunucuya katilma", value=f"<t:{int(member.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Hesap olusturma", value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Roller", value=", ".join([r.name for r in member.roles[:10]]), inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
