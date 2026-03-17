import discord
from discord.ext import commands
import time
import asyncio

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member} Avatar",
            color=discord.Color.blue()
        )
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='profil')
    async def profil(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user = await self.bot.db.get_user(str(member.id))
        
        cursor = await self.bot.db.execute(
            "SELECT * FROM levels WHERE server_id = ? AND user_id = ?",
            (str(ctx.guild.id), str(member.id))
        )
        level_data = await cursor.fetchone()
        
        xp = level_data[3] if level_data else 0
        level = level_data[4] if level_data else 1
        
        embed = discord.Embed(
            title=f"{member} Profili",
            color=discord.Color.blue()
        )
        embed.add_field(name="Bakiye", value=f"**{user['balance']}** TL", inline=True)
        embed.add_field(name="Banka", value=f"**{user['bank']}** TL", inline=True)
        embed.add_field(name="Seviye", value=str(level), inline=True)
        embed.add_field(name="XP", value=f"{xp}/{level*100}", inline=True)
        embed.add_field(name="Toplam Mesaj", value=str(user['total_messages']), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='dil')
    async def dil(self, ctx, dil: str = None):
        if not dil:
            user = await self.bot.db.get_user(str(ctx.author.id))
            await ctx.send(f"Mevcut dilin: **{user['language']}**")
            return
        
        if dil not in ['tr', 'en']:
            await ctx.send("Desteklenen diller: tr, en")
            return
        
        await self.bot.db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (dil, str(ctx.author.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"Dil **{dil}** olarak degistirildi!")
    
    @commands.command(name='afk')
    async def afk(self, ctx, *, reason=None):
        reason = reason or "AFK"
        
        await self.bot.db.execute(
            "INSERT OR REPLACE INTO afk (user_id, reason) VALUES (?, ?)",
            (str(ctx.author.id), reason)
        )
        await self.bot.db.commit()
        
        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
        await ctx.send(f"{ctx.author} Artik AFK! Sebep: {reason}")
    
    @commands.command(name='duyuru')
    @commands.has_permissions(manage_messages=True)
    async def duyuru(self, ctx, *, mesaj=None):
        if not mesaj:
            await ctx.send("Bir mesaj yaz!")
            return
        
        embed = discord.Embed(
            title="📢 Duyuru",
            description=mesaj,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Yazan: {ctx.author}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='oylama')
    @commands.has_permissions(manage_messages=True)
    async def oylama(self, ctx, *, mesaj=None):
        if not mesaj:
            await ctx.send("Bir mesaj yaz!")
            return
        
        embed = discord.Embed(
            title="📊 Oylama",
            description=mesaj,
            color=discord.Color.blue()
        )
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
    
    @commands.command(name='ilet')
    async def ilet(self, ctx, *, mesaj=None):
        if not mesaj:
            await ctx.send("Bir mesaj yaz!")
            return
        
        owner = self.bot.get_user(self.bot.config['bot']['owner_id'])
        if owner:
            embed = discord.Embed(
                title="📬 Mesaj Iletildi!",
                description=mesaj,
                color=discord.Color.green()
            )
            embed.add_field(name="Gonderen", value=f"{ctx.author} ({ctx.author.id})", inline=False)
            await ctx.send(embed=embed)
            
            embed2 = discord.Embed(
                title="📬 Yeni Mesaj!",
                description=mesaj,
                color=discord.Color.blue()
            )
            embed2.add_field(name="Gonderen", value=f"{ctx.author} ({ctx.author.id})", inline=False)
            embed2.add_field(name="Sunucu", value=ctx.guild.name if ctx.guild else "DM", inline=False)
            await owner.send(embed=embed2)
        else:
            await ctx.send("Sahip bulunamadi!")
    
    @commands.command(name='sunucu')
    @commands.guild_only()
    async def sunucu(self, ctx):
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Uye", value=str(guild.member_count), inline=True)
        embed.add_field(name="Olusma", value=str(guild.created_at)[:10], inline=True)
        embed.add_field(name="Kanal", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Rol", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Sahip", value=f"<@{guild.owner_id}>", inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='emojiler')
    @commands.guild_only()
    async def emojiler(self, ctx):
        guild = ctx.guild
        
        if not guild.emojis:
            await ctx.send("Sunucuda emoji yok!")
            return
        
        embed = discord.Embed(
            title=f"😀 {guild.name} Emojileri",
            description=" ".join([str(e) for e in guild.emojis]),
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='rolbilgi')
    @commands.guild_only()
    async def rolbilgi(self, ctx, role: discord.Role = None):
        if not role:
            await ctx.send("Bir rol etiketle!")
            return
        
        embed = discord.Embed(
            title=f"📛 {role.name}",
            color=role.color
        )
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Uye sayisi", value=str(len(role.members)), inline=True)
        embed.add_field(name="Renk", value=str(role.color), inline=True)
        embed.add_field(name="Olusturulma", value=str(role.created_at)[:10], inline=True)
        embed.add_field(name="Pozisyon", value=str(role.position), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='kanalbilgi')
    @commands.guild_only()
    async def kanalbilgi(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        
        embed = discord.Embed(
            title=f"#{channel.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Tur", value=str(channel.type), inline=True)
        embed.add_field(name="Olusturulma", value=str(channel.created_at)[:10], inline=True)
        if channel.topic:
            embed.add_field(name="Konu", value=channel.topic, inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='site', aliases=['web', 'panel'])
    async def site(self, ctx):
        url = self.bot.config.get('web', {}).get('url', 'https://huhbot.onrender.com')
        client_id = self.bot.config.get('bot', {}).get('client_id', '1452460095085744238')
        embed = discord.Embed(
            title="🌐 Huh Bot Web Panel",
            description=f"Botun web paneline buradan erişebilirsiniz:\n\n🔗 **Web Panel:** {url}",
            color=discord.Color.blue()
        )
        embed.add_field(name="📋 Özellikler", value="- Sunucu yönetimi\n- Moderasyon ayarları\n- Ekonomi kontrolü\n- Seviye sistemi\n- Hoş geldin mesajları", inline=False)
        embed.add_field(name="➕ Sunucuya Ekle", value=f"[Tıkla](https://discord.com/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot)", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
