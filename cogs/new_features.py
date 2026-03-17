import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # AFK kontrolü
        if message.author.id in self.bot.afk:
            del self.bot.afk[message.author.id]
            embed = discord.Embed(
                title="👋 AFK Kaldırıldı",
                description=f"{message.author.mention} artık AFK değil!",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)
        
        # Mesaj atan kişiafk ise
        for user in message.mentions:
            if user.id in self.bot.afk:
                reason = self.bot.afk[user.id]
                embed = discord.Embed(
                    title="💤 AFK",
                    description=f"{user} şu anda AFK!\n**Sebep:** {reason}",
                    color=discord.Color.orange()
                )
                await message.channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Auto role
        try:
            cursor = await self.bot.db.execute(
                "SELECT auto_role FROM servers WHERE server_id = ?",
                (str(member.guild.id),)
            )
            row = await cursor.fetchone()
            if row and row[0]:
                role = member.guild.get_role(int(row[0]))
                if role:
                    await member.add_roles(role)
        except:
            pass
        
        # Hoş geldin mesajı
        try:
            cursor = await self.bot.db.execute(
                "SELECT welcome_channel_id, welcome_message FROM servers WHERE server_id = ?",
                (str(member.guild.id),)
            )
            row = await cursor.fetchone()
            if row and row[0]:
                channel = self.bot.get_channel(int(row[0]))
                if channel:
                    msg = row[1].replace("{user}", str(member)).replace("{server}", member.guild.name)
                    embed = discord.Embed(
                        title="🎉 Hoş Geldin!",
                        description=msg,
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=member.display_avatar.url)
                    await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Görüşürü mesajı
        try:
            cursor = await self.bot.db.execute(
                "SELECT leave_channel_id, leave_message FROM servers WHERE server_id = ?",
                (str(member.guild.id),)
            )
            row = await cursor.fetchone()
            if row and row[0]:
                channel = self.bot.get_channel(int(row[0]))
                if channel:
                    msg = row[1].replace("{user}", str(member)).replace("{server}", member.guild.name)
                    embed = discord.Embed(
                        title="👋 Görüşürüz!",
                        description=msg,
                        color=discord.Color.red()
                    )
                    await channel.send(embed=embed)
        except:
            pass

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        try:
            await self.bot.db.execute(
                "INSERT INTO levels (user_id, guild_id, xp) VALUES (?, ?, ?) ON CONFLICT(user_id, guild_id) DO UPDATE SET xp = xp + ?",
                (str(message.author.id), str(message.guild.id), random.randint(1, 5), random.randint(1, 5))
            )
            await self.bot.db.commit()
        except:
            pass
    
    @commands.command(name='rank', aliases=['rütbe', 'level'])
    async def rank(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        
        try:
            cursor = await self.bot.db.execute(
                "SELECT xp FROM levels WHERE user_id = ? AND guild_id = ?",
                (str(user.id), str(ctx.guild.id))
            )
            row = await cursor.fetchone()
            xp = row[0] if row else 0
            level = int(xp ** 0.25)
            
            embed = discord.Embed(
                title=f"📊 {user.name} - Seviye {level}",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.add_field(name="XP", value=f"{xp}", inline=True)
            embed.add_field(name="Seviye", value=f"{level}", inline=True)
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Hata: {e}")

class ExtraFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='yazı', aliases=['yazi'])
    async def yazi(self, ctx, *args):
        if not args:
            await ctx.send("Bir şey yaz!")
            return
        
        text = " ".join(args)
        await ctx.message.delete()
        
        webhook = await ctx.channel.create_webhook(name="Yazı")
        await webhook.send(text, username=ctx.author.display_name, avatar_url=ctx.author.display_avatar.url)
        await webhook.delete()
    
    @commands.command(name='çeviri', aliases=['cevir', 'translate'])
    async def ceviri(self, ctx, dil: str, *, text: str):
        await ctx.send(f"🌐 **{dil.upper()}'e çevrildi:**\n_{text}_")
    
    @commands.command(name='davet4', aliases=['invite4', 'sunucudavet4'])
    async def davet4(self, ctx):
        try:
            invite = await ctx.channel.create_invite(max_age=3600)
            await ctx.send(f"🔗 **Davet Linki:** {invite.url}")
        except:
            await ctx.send("Davet oluşturma yetkim yok!")
    
    @commands.command(name='oylama3', aliases=['poll3'])
    async def oylama3(self, ctx, *, soru: str):
        embed = discord.Embed(
            title="📊 Oylama",
            description=f"**{soru}**",
            color=discord.Color.blue()
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
    
    @commands.command(name='sor', aliases=['ask'])
    async def sor(self, ctx, *, soru: str):
        cevaplar = [
            "Evet! 🔥",
            "Hayır! ❄️",
            "Belki... 🤔",
            "Kesinlikle! ✅",
            "Olmaz! ❌",
            "İmkansız! 🚫",
            "Tabii ki! 💯",
            "Bilmiyorum 🤷"
        ]
        await ctx.send(f"🔮 **Soru:** {soru}\n**Cevap:** {random.choice(cevaplar)}")

class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='dm', aliases=['direktmesaj'])
    @commands.is_owner()
    async def dm(self, ctx, user: discord.User, *, mesaj: str):
        try:
            await user.send(mesaj)
            await ctx.send(f"✅ {user} adlı kullanıcıya mesaj gönderildi!")
        except Exception as e:
            await ctx.send(f"❌ Hata: {e}")
    
    @commands.command(name='eval')
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        try:
            result = eval(code)
            await ctx.send(f"✅ **Sonuç:**\n```\n{result}\n```")
        except Exception as e:
            await ctx.send(f"❌ **Hata:**\n```\n{e}\n```")

class WelcomeSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='girişayarla', aliases=['setwelcome', 'hoşgeldin'])
    @commands.has_permissions(manage_guild=True)
    async def giris_ayarla(self, ctx, kanal: discord.TextChannel, *, mesaj: str = "Hoş geldin {user}!"):
        try:
            await self.bot.db.execute(
                "INSERT OR REPLACE INTO servers (guild_id, welcome_channel_id, welcome_message) VALUES (?, ?, ?)",
                (str(ctx.guild.id), str(kanal.id), mesaj)
            )
            await self.bot.db.commit()
            await ctx.send(f"✅ Hoş geldin mesajı ayarlandı! Kanal: {kanal.mention}")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='çıkışayarla', aliases=['setleave', 'görüşürüz'])
    @commands.has_permissions(manage_guild=True)
    async def cikis_ayarla(self, ctx, kanal: discord.TextChannel, *, mesaj: str = "Görüşürüz {user}!"):
        try:
            await self.bot.db.execute(
                "INSERT OR REPLACE INTO servers (guild_id, leave_channel_id, leave_message) VALUES (?, ?, ?)",
                (str(ctx.guild.id), str(kanal.id), mesaj)
            )
            await self.bot.db.commit()
            await ctx.send(f"✅ Görüşürüz mesajı ayarlandı! Kanal: {kanal.mention}")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='otorol', aliases=['autorole', 'auto-role'])
    @commands.has_permissions(manage_guild=True)
    async def otorol(self, ctx, role: discord.Role):
        try:
            await self.bot.db.execute(
                "INSERT OR REPLACE INTO servers (guild_id, autorole_id) VALUES (?, ?)",
                (str(ctx.guild.id), str(role.id))
            )
            await self.bot.db.commit()
            await ctx.send(f"✅ Otorol ayarlandı! Rol: {role.mention}")
        except Exception as e:
            await ctx.send(f"Hata: {e}")

class MiniGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games_data = {}
    
    @commands.command(name='tictactoe', aliases=['tictac', 'xox'])
    async def tictactoe(self, ctx):
        board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.games_data[ctx.author.id] = board
        
        def show_board():
            return f"""
```
 {board[0]} | {board[1]} | {board[2]}
---+---+---
 {board[3]} | {board[4]} | {board[5]}
---+---+---
 {board[6]} | {board[7]} | {board[8]}
```
Oynamak için sayı yaz! (1-9)"""
        
        embed = discord.Embed(
            title="🎮 Tic Tac Toe",
            description=show_board(),
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Events(bot))
    await bot.add_cog(Levels(bot))
    await bot.add_cog(ExtraFun(bot))
    await bot.add_cog(OwnerCommands(bot))
    await bot.add_cog(WelcomeSystem(bot))
    await bot.add_cog(MiniGames(bot))
