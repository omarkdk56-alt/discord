import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

class AdvancedFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
    
    async def cog_load(self):
        self.session = aiohttp.ClientSession()
    
    async def cog_unload(self):
        if self.session:
            await self.session.close()
    
    @commands.command(name='kullanıcıbilgi2', aliases=['kb2', 'userinfo2'])
    async def kullanici_bilgi2(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"👤 {member}",
            color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Sunucu Adı", value=member.display_name, inline=True)
        embed.add_field(name="Bot mu?", value="Evet" if member.bot else "Hayır", inline=True)
        
        created = member.created_at.strftime('%d/%m/%Y %H:%M')
        joined = member.joined_at.strftime('%d/%m/%Y %H:%M') if member.joined_at else "Bilinmiyor"
        
        embed.add_field(name="Hesap Oluşturulma", value=created, inline=True)
        embed.add_field(name="Sunucuya Katılma", value=joined, inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='sunucu-durumu')
    async def sunucu_durumu(self, ctx):
        guild = ctx.guild
        
        online = len([m for m in guild.members if m.status == discord.Status.online])
        idle = len([m for m in guild.members if m.status == discord.Status.idle])
        dnd = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline = len([m for m in guild.members if m.status == discord.Status.offline])
        
        embed = discord.Embed(
            title=f"📊 {guild.name} Durumu",
            color=discord.Color.blue()
        )
        embed.add_field(name="🟢 Çevrimiçi", value=online, inline=True)
        embed.add_field(name="🟡 Boşta", value=idle, inline=True)
        embed.add_field(name="🔴 Rahatsız Etmeyin", value=dnd, inline=True)
        embed.add_field(name="⚪ Çevrimdışı", value=offline, inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='rol-bilgi', aliases=['rb'])
    async def rol_bilgi(self, ctx, role: discord.Role):
        embed = discord.Embed(
            title=f"📋 {role.name}",
            color=role.color
        )
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Renk", value=str(role.color), inline=True)
        embed.add_field(name="Üye Sayısı", value=len(role.members), inline=True)
        embed.add_field(name="Pozisyon", value=role.position, inline=True)
        embed.add_field(name="Ayrıcalıklı mı?", value="Evet" if role.permissions.administrator else "Hayır", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='kanal-bilgi2')
    async def kanal_bilgi2(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        
        embed = discord.Embed(
            title=f"📁 {channel.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Kategori", value=channel.category.name if channel.category else "Yok", inline=True)
        embed.add_field(name="Konum", value=channel.position, inline=True)
        embed.add_field(name="Slowmode", value=f"{channel.slowmode_delay} saniye", inline=True)
        embed.add_field(name="Üst Üste Mesaj", value=channel.last_message.content[:100] if channel.last_message else "Yok", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='emoji-bilgi', aliases=['eb'])
    async def emoji_bilgi(self, ctx, emoji: discord.Emoji):
        embed = discord.Embed(
            title=f"😀 {emoji.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=emoji.url)
        embed.add_field(name="ID", value=emoji.id, inline=True)
        embed.add_field(name="Sunucu", value=emoji.guild.name, inline=True)
        embed.add_field(name="Animasyonlu mu?", value="Evet" if emoji.animated else "Hayır", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='davet-bilgi', aliases=['davetbilgi'])
    async def davet_bilgi(self, ctx, invite: str = None):
        if not invite:
            invites = await ctx.guild.invites()
            if not invites:
                return await ctx.send("Bu sunucuda davet yok!")
            
            embed = discord.Embed(
                title="🔗 Sunucu Davetleri",
                color=discord.Color.blue()
            )
            
            for inv in invites[:10]:
                embed.add_field(
                    name=f"Kanal: {inv.channel.name}",
                    value=f"Kullanım: {inv.uses}/{inv.max_uses}\nOluşturan: {inv.inviter.mention if inv.inviter else 'Bilinmiyor'}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
        else:
            try:
                inv = await self.bot.fetch_invite(invite)
                embed = discord.Embed(
                    title="🔗 Davet Bilgileri",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Sunucu", value=inv.guild.name if inv.guild else "Bilinmiyor", inline=True)
                embed.add_field(name="Kanal", value=inv.channel.name if inv.channel else "Bilinmiyor", inline=True)
                embed.add_field(name="Davet Eden", value=inv.inviter.mention if inv.inviter else "Bilinmiyor", inline=True)
                embed.add_field(name="Kullanım", value=f"{inv.uses}/{inv.max_uses if inv.max_uses else 'Sınırsız'}", inline=True)
                
                await ctx.send(embed=embed)
            except:
                await ctx.send("Davet bulunamadı!")
    
    @commands.command(name='yazı-kanalı')
    async def yazi_kanali(self, ctx, kanal: discord.VoiceChannel = None):
        if not kanal:
            await ctx.send("Bir ses kanalı belirtin!")
            return
        
        embed = discord.Embed(
            title=f"🔊 {kanal.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=kanal.id, inline=True)
        embed.add_field(name="Kategori", value=kanal.category.name if kanal.category else "Yok", inline=True)
        embed.add_field(name="Üye Sayısı", value=len(kanal.members), inline=True)
        embed.add_field(name="Kullanıcılar", value=", ".join([m.mention for m in kanal.members]) if kanal.members else "Yok", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='random-üye')
    async def random_uye(self, ctx):
        members = [m for m in ctx.guild.members if not m.bot]
        if not members:
            return await ctx.send("Üye bulunamadı!")
        
        member = random.choice(members)
        
        embed = discord.Embed(
            title="🎲 Rastgele Üye",
            description=member.mention,
            color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='random-emoji')
    async def random_emoji(self, ctx):
        emojis = ctx.guild.emojis
        if not emojis:
            return await ctx.send("Sunucuda emoji yok!")
        
        emoji = random.choice(emojis)
        
        embed = discord.Embed(
            title="🎲 Rastgele Emoji",
            description=f"{emoji} `{emoji.name}`",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=emoji.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='sayı-tahmin')
    async def sayi_tahmin(self, ctx):
        sayi = random.randint(1, 100)
        
        embed = discord.Embed(
            title="🎯 Sayı Tahmin",
            description="1-100 arasında bir sayı tuttum! Tahmin et!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        
        for _ in range(7):
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
                tahmin = int(msg.content)
                
                if tahmin == sayi:
                    await ctx.send(f"🎉 Tebrikler! Doğru cevap: {sayi}")
                    return
                elif tahmin < sayi:
                    await ctx.send("📈 Daha büyük!")
                else:
                    await ctx.send("📉 Daha küçük!")
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Süre doldu! Doğru cevap: {sayi}")
                return
        
        await ctx.send(f"⏰ Hakkin bitti! Doğru cevap: {sayi}")
    
    @commands.command(name='matematik')
    async def matematik(self, ctx, islem: str = None):
        if not islem:
            await ctx.send("Kullanım: h!matematik <işlem>\nÖrnek: h!matematik 5+5")
            return
        
        islem = islem.replace("x", "*").replace("X", "*").replace("÷", "/").replace("^", "**")
        
        try:
            if any(x in islem for x in ["__import__", "eval", "exec", "open", "os", "sys"]):
                return await ctx.send("Güvenlik: İzin verilmeyen karakter!")
            
            sonuc = eval(islem)
            
            embed = discord.Embed(
                title="🧮 Matematik",
                description=f"İşlem: `{islem}`\nSonuç: `{sonuc}`",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except:
            await ctx.send("Hatalı işlem!")
    
    @commands.command(name='fbi')
    async def fbi(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        embed = discord.Embed(
            title="👮 FBI",
            description=f"{member.mention} adlı kişiFBI tarafından aranıyor!",
            color=discord.Color.red()
        )
        embed.set_image(url="https://media.tenor.com/J5iuG7XWcNoAAAAi/fbi-open-up.gif")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='waifu')
    async def waifu(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        waifu_isimleri = ["Rem", "Mikasa", "Asuna", "Hinata", "Power", "Zero Two", "Mai", "Rias", "Yukino"]
        
        embed = discord.Embed(
            title="👘 Waifu",
            description=f"{member.mention} = **{random.choice(waifu_isimleri)}**",
            color=discord.Color.pink()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='np')
    async def np(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Bir ses kanalında değilsin!")
            return
        
        player = ctx.voice_client
        if not player or not player.current:
            await ctx.send("Müzik çalmıyor!")
            return
        
        track = player.current
        
        embed = discord.Embed(
            title="🎵 Şimdi Çalan",
            description=f"**{track.title}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Süre", value=f"{int(track.length // 60)}:{int(track.length % 60):02d}", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='qrcode')
    async def qrcode(self, ctx, *, text: str = None):
        if not text:
            await ctx.send("Bir metin belirtin!")
            return
        
        if len(text) > 500:
            await ctx.send("Metin çok uzun!")
            return
        
        embed = discord.Embed(
            title="📱 QR Code",
            description=f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}",
            color=discord.Color.blue()
        )
        embed.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='yapay-zeka', aliases=['ai', 'yapayzeka'])
    async def yapay_zeka(self, ctx, *, soru: str = None):
        if not soru:
            await ctx.send("Bir soru sorun!")
            return
        
        yanitlar = [
            "Bu ilginç bir soru!",
            "Kesinlikle!",
            "Bence öyle.",
            "Bilmiyorum ama araştırmam lazım.",
            "Tabii ki!",
            "Bu konuda bir fikrim yok.",
            "Evet, kesinlikle!",
            "Sanırım öyle.",
            "Biraz garip bir soru ama... Evet!"
        ]
        
        embed = discord.Embed(
            title="🤖 Yapay Zeka",
            description=f"Soru: **{soru}**\n\nYanıt: **{random.choice(yanitlar)}**",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='token')
    async def token(self, ctx):
        await ctx.send("Token: `MTA4MjMxNjUwNDc0MzA4ODk4MQ.G5k9B2.Wx4qCpX7vT9nR2yK3jH8mP1cL6vN4sD9fR2` 🚀")
    
    @commands.command(name='kbps')
    async def kbps(self, ctx):
        kbps = random.randint(10, 1000)
        embed = discord.Embed(
            title="🌐 İnternet Hızı",
            description=f"İndirme: **{kbps} Mbps**\nYükleme: **{kbps//2} Mbps**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='mcskin')
    async def mcskin(self, ctx, isim: str = None):
        if not isim:
            await ctx.send("Bir Minecraft kullanıcı adı belirtin!")
            return
        
        embed = discord.Embed(
            title=f"⛏️ Minecraft: {isim}",
            description=f"![Skin](https://mc-heads.net/body/{isim}/right)",
            color=discord.Color.green()
        )
        embed.set_image(url=f"https://mc-heads.net/body/{isim}/right")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='steam')
    async def steam(self, ctx, *, oyun: str = None):
        if not oyun:
            await ctx.send("Bir oyun adı belirtin!")
            return
        
        embed = discord.Embed(
            title=f"🎮 Steam: {oyun}",
            description="Arama sonuçları Steam'de!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Link", value=f"[Ara](https://store.steampowered.com/search/?term={oyun.replace(' ', '+')})", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='wikipedia')
    async def wikipedia(self, ctx, *, arama: str = None):
        if not arama:
            await ctx.send("Bir arama terimi belirtin!")
            return
        
        embed = discord.Embed(
            title=f"📚 Wikipedia: {arama}",
            description=f"[Wikipedia'da ara](https://tr.wikipedia.org/wiki/{arama.replace(' ', '_')})",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='youtube')
    async def youtube(self, ctx, *, arama: str = None):
        if not arama:
            await ctx.send("Bir arama terimi belirtin!")
            return
        
        embed = discord.Embed(
            title=f"📺 YouTube: {arama}",
            description=f"[YouTube'da ara](https://www.youtube.com/results?search_query={arama.replace(' ', '+')})",
            color=discord.Color.red()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='google')
    async def google(self, ctx, *, arama: str = None):
        if not arama:
            await ctx.send("Bir arama terimi belirtin!")
            return
        
        embed = discord.Embed(
            title=f"🔍 Google: {arama}",
            description=f"[Google'da ara](https://www.google.com/search?q={arama.replace(' ', '+')})",
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)

class AdvancedModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='toplam-üye')
    async def toplam_uye(self, ctx):
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"👥 {guild.name} Üye Bilgileri",
            color=discord.Color.blue()
        )
        embed.add_field(name="Toplam", value=guild.member_count, inline=True)
        embed.add_field(name="Kullanıcı", value=len([m for m in guild.members if not m.bot]), inline=True)
        embed.add_field(name="Bot", value=len([m for m in guild.members if m.bot]), inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='banlı-kullanıcılar')
    async def banli_kullanicilar(self, ctx):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("Yetkin yok!")
            return
        
        bans = await ctx.guild.bans()
        
        if not bans:
            return await ctx.send("Yasaklı kullanıcı yok!")
        
        embed = discord.Embed(
            title="🚫 Yasaklı Kullanıcılar",
            color=discord.Color.red()
        )
        
        for ban in bans[:10]:
            embed.add_field(
                name=f"{ban.user}",
                value=f"Sebep: {ban.reason or 'Belirtilmemiş'}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='rolleri-oluştur')
    @commands.has_permissions(manage_roles=True)
    async def roller_olustur(self, ctx, *roller):
        if not roller:
            await ctx.send("Oluşturulacak rolleri belirtin!")
            return
        
        for rol in roller:
            try:
                await ctx.guild.create_role(name=rol, color=discord.Color.random())
            except:
                pass
        
        await ctx.send(f"✅ {len(roller)} rol oluşturuldu!")
    
    @commands.command(name='temizle')
    @commands.has_permissions(manage_messages=True)
    async def temizle(self, ctx, miktar: int = 10):
        if miktar < 1:
            miktar = 1
        if miktar > 1000:
            miktar = 1000
        
        deleted = await ctx.channel.purge(limit=miktar + 1)
        
        embed = discord.Embed(
            title="🧹 Temizlendi",
            description=f"{len(deleted)-1} mesaj silindi!",
            color=discord.Color.green()
        )
        
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, sebep: str = None):
        try:
            await member.kick(reason=sebep)
            
            embed = discord.Embed(
                title="🦶 Kick",
                description=f"{member} sunucudan atıldı!",
                color=discord.Color.red()
            )
            if sebep:
                embed.add_field(name="Sebep", value=sebep, inline=False)
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, sebep: str = None):
        try:
            await member.ban(reason=sebep)
            
            embed = discord.Embed(
                title="🔨 Ban",
                description=f"{member} yasaklandı!",
                color=discord.Color.red()
            )
            if sebep:
                embed.add_field(name="Sebep", value=sebep, inline=False)
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int = None):
        if not user_id:
            await ctx.send("Bir kullanıcı ID'si belirtin!")
            return
        
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            
            embed = discord.Embed(
                title="✅ Unban",
                description=f"{user} yasağı kaldırıldı!",
                color=discord.Color.green()
            )
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, sebep: str = None):
        await self.bot.db.execute(
            "INSERT INTO warns (user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (str(member.id), str(ctx.guild.id), str(ctx.author.id), sebep or "Belirtilmemiş")
        )
        await self.bot.db.commit()
        
        embed = discord.Embed(
            title="⚠️ Uyarı",
            description=f"{member} uyarıldı!",
            color=discord.Color.yellow()
        )
        if sebep:
            embed.add_field(name="Sebep", value=sebep, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='uyarılar')
    async def uyarilar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        cursor = await self.bot.db.execute(
            "SELECT * FROM warns WHERE user_id = ? AND server_id = ?",
            (str(member.id), str(ctx.guild.id))
        )
        warns = await cursor.fetchall()
        
        if not warns:
            return await ctx.send(f"{member} uyarısı yok!")
        
        embed = discord.Embed(
            title=f"⚠️ {member} Uyarıları",
            description=f"Toplam: {len(warns)} uyarı",
            color=discord.Color.yellow()
        )
        
        for i, warn in enumerate(warns[:10], 1):
            embed.add_field(
                name=f"Uyarı #{i}",
                value=f"Sebep: {warn[3]}\nModeratör: <@{warn[2]}>",
                inline=False
            )
        
        await ctx.send(embed=embed)

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='çekiliş-oluştur', aliases=['giveaway'])
    @commands.has_permissions(manage_messages=True)
    async def cekilis_olustur(self, ctx, sure: int = None, *, odul: str = None):
        if not sure or not odul:
            await ctx.send("Kullanım: h!çekiliş-oluştur <süre(dk)> <ödül>")
            return
        
        embed = discord.Embed(
            title="🎉 Çekiliş!",
            description=f"**Ödül:** {odul}\n\nKatılmak için 🎉 emojisine tıklayın!\nSüre: {sure} dakika",
            color=discord.Color.gold()
        )
        embed.set_footer(text="Çekilişi başlatan: " + str(ctx.author))
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")
        
        await self.bot.db.execute(
            "INSERT INTO giveaways (message_id, server_id, channel_id, prize, winners, ends_at, created_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (str(msg.id), str(ctx.guild.id), str(ctx.channel.id), odul, 1, int((ctx.message.created_at + timedelta(minutes=sure)).timestamp()), str(ctx.author.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"Çekiliş oluşturuldu! {sure} dakika sonra sonuçlanacak.")
    
    @commands.command(name='çekiliş-bitir')
    @commands.has_permissions(manage_messages=True)
    async def cekilis_bitir(self, ctx):
        cursor = await self.bot.db.execute(
            "SELECT * FROM giveaways WHERE server_id = ? AND is_ended = 0",
            (str(ctx.guild.id),)
        )
        giveaways = await cursor.fetchall()
        
        if not giveaways:
            return await ctx.send("Aktif çekiliş yok!")
        
        giveaway = giveaways[0]
        
        try:
            channel = self.bot.get_channel(int(giveaway[3]))
            msg = await channel.fetch_message(int(giveaway[1]))
            
            reaction = discord.utils.get(msg.reactions, emoji="🎉")
            users = await reaction.users().flatten()
            users = [u for u in users if not u.bot]
            
            if not users:
                await ctx.send("Katılım yok!")
                return
            
            winner = random.choice(users)
            
            embed = discord.Embed(
                title="🎉 Kazanan!",
                description=f"**Ödül:** {giveaway[5]}\n\n**Kazanan:** {winner.mention}",
                color=discord.Color.gold()
            )
            
            await ctx.send(embed=embed)
            
            await self.bot.db.execute(
                "UPDATE giveaways SET is_ended = 1 WHERE id = ?",
                (giveaway[0],)
            )
            await self.bot.db.commit()
            
        except Exception as e:
            await ctx.send(f"Hata: {e}")

class Economy2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='market')
    async def market(self, ctx):
        items = [
            ("💻 Bilgisayar", 5000, "Enerjinizi artırır!"),
            ("📱 Telefon", 3000, "Her yerde kullanın!"),
            ("🏠 Ev", 50000, "Statü sembolü!"),
            ("🚗 Araba", 25000, "Hızlı ulaşım!"),
            ("💰 Para Çarpanı", 10000, "Kazanılan para 2x!"),
            ("🎫 Lotarya Bileti", 500, "Şansınızı deneyin!"),
            ("🎮 Oyun Konsolu", 2000, "Eğlence!"),
            ("☕ Kahve", 50, "Günlük enerji!")
        ]
        
        embed = discord.Embed(
            title="🛒 Market",
            description="Almak istediğiniz ürünü seçin!",
            color=discord.Color.gold()
        )
        
        for item, fiyat, aciklama in items:
            embed.add_field(name=f"{item} - {fiyat} TL", value=aciklama, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='satın-al')
    async def satin_al(self, ctx, *item_name):
        if not item_name:
            await ctx.send("Kullanım: h!satın-al <ürün adı>")
            return
        
        user = await self.bot.get_user(ctx.author.id)
        
        items = {
            "bilgisayar": 5000,
            "telefon": 3000,
            "ev": 50000,
            "araba": 25000,
            "para çarpanı": 10000,
            "loterry bileti": 500,
            "lotarya bileti": 500,
            "oyun konsolu": 2000,
            "kahve": 50
        }
        
        item = " ".join(item_name)
        fiyat = items.get(item.lower())
        
        if not fiyat:
            await ctx.send("Ürün bulunamadı!")
            return
        
        if user['balance'] < fiyat:
            await ctx.send("Yetersiz bakiye!")
            return
        
        await self.bot.db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (fiyat, str(ctx.author.id))
        )
        await self.bot.db.commit()
        
        embed = discord.Embed(
            title="✅ Satın Alındı!",
            description=f"**Ürün:** {item}\n**Fiyat:** {fiyat} TL",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='günlük')
    async def gunluk(self, ctx):
        user = await self.bot.get_user(ctx.author.id)
        
        if user['daily_cooldown'] and int(datetime.now().timestamp()) - user['daily_cooldown'] < 86400:
            kalan = 86400 - (int(datetime.now().timestamp()) - user['daily_cooldown'])
            saat = kalan // 3600
            dakika = (kalan % 3600) // 60
            return await ctx.send(f"Günlük ödülü almak için {saat} saat {dakika} dakika bekle!")
        
        odul = random.randint(200, 500)
        
        await self.bot.db.execute(
            "UPDATE users SET balance = balance + ?, daily_cooldown = ? WHERE user_id = ?",
            (odul, int(datetime.now().timestamp()), str(ctx.author.id))
        )
        await self.bot.db.commit()
        
        embed = discord.Embed(
            title="💰 Günlük Ödül!",
            description=f"+{odul} TL kazandın!",
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='bonus')
    async def bonus(self, ctx):
        odul = random.randint(100, 1000)
        
        await self.bot.db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (odul, str(ctx.author.id))
        )
        await self.bot.db.commit()
        
        embed = discord.Embed(
            title="🎁 Bonus!",
            description=f"+{odul} TL bonus para!",
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdvancedFun(bot))
    await bot.add_cog(AdvancedModeration(bot))
    await bot.add_cog(Giveaway(bot))
    await bot.add_cog(Economy2(bot))
