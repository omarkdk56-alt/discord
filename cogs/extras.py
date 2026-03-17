import discord
from discord.ext import commands
import random
import json
import math
import os
from datetime import datetime, timedelta
from typing import List

class PaginationView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed], ctx, timeout: float = 120):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.ctx = ctx
        self.current_page = 0
        self.total_pages = len(embeds)
        
        self.prev_button.disabled = True
        if self.total_pages <= 1:
            self.next_button.disabled = True
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.message.delete()
    
    def update_buttons(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_pages - 1

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='çekiliş')
    async def cekilis(self, ctx):
        kazanan = random.choice(ctx.guild.members)
        
        embed = discord.Embed(
            title="🎉 Çekiliş!",
            description=f"Kazanan: {kazanan.mention}",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='rastgeleitem', aliases=['rastgele_item'])
    async def rastgele_item(self, ctx, *args):
        if not args:
            await ctx.send("Eleman belirt!")
            return
        
        secim = random.choice(args)
        embed = discord.Embed(
            title="🎲 Rastgele Seçim",
            description=f"Seçilen: **{secim}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='yazıtura')
    async def yazi_tura(self, ctx):
        await ctx.send("🪙 Yazı mı, Tura mı?")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=10)
            secim = msg.content.lower()
            
            if secim not in ['yazı', 'tura']:
                await ctx.send("Yazı veya tura seç!")
                return
            
            sonuc = random.choice(['yazı', 'tura'])
            
            if secim == sonuc:
                await ctx.send(f"✅ Kazandın! Sonuç: **{sonuc}**")
            else:
                await ctx.send(f"❌ Kaybettin! Sonuç: **{sonuc}**")
        except:
            await ctx.send("⏰ Süre doldu!")
    
    @commands.command(name='banner2')
    async def banner2(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user = await self.bot.fetch_user(member.id)
        
        if user.banner:
            embed = discord.Embed(title=f"🎨 {member.name}'nin Banneri", color=member.accent_color or discord.Color.blue())
            embed.set_image(url=user.banner.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member} kullanıcısının banneri yok!")
    
    @commands.command(name='profil')
    async def profil(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        created_at = member.created_at.strftime('%d/%m/%Y')
        joined_at = member.joined_at.strftime('%d/%m/%Y') if member.joined_at else "Bilinmiyor"
        
        roles = [role.mention for role in member.roles if role != member.guild.default_role]
        roles_text = ", ".join(roles[:10]) if roles else "Rol yok"
        
        embed = discord.Embed(
            title=f"👤 {member}",
            color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Sunucuya Katilma", value=joined_at, inline=True)
        embed.add_field(name="Hesap Olusturma", value=created_at, inline=True)
        embed.add_field(name="Roller", value=roles_text, inline=False)
        embed.add_field(name="En Yuksek Rol", value=member.top_role.mention, inline=True)
        embed.add_field(name="Bot mu?", value="Evet" if member.bot else "Hayir", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='serverbanner')
    async def serverbanner(self, ctx):
        guild = ctx.guild
        
        if guild.banner:
            embed = discord.Embed(title=f"🎨 {guild.name} Banneri", color=discord.Color.blue())
            embed.set_image(url=guild.banner.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{guild.name} sunucusunun banneri yok!")
    
    @commands.command(name='servericon')
    async def servericon(self, ctx):
        guild = ctx.guild
        
        if guild.icon:
            embed = discord.Embed(title=f"🖼️ {guild.name} Sunucu Iconu", color=discord.Color.blue())
            embed.set_image(url=guild.icon.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{guild.name} sunucusunun iconu yok!")
    
    @commands.command(name='sunucubilgi', aliases=['sunucu', 'serverinfo', 'sb'])
    async def sunucubilgi(self, ctx):
        guild = ctx.guild
        
        created_at = guild.created_at.strftime('%d/%m/%Y')
        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Olusturulma", value=created_at, inline=True)
        embed.add_field(name="Sahip", value=guild.owner.mention if guild.owner else "Bilinmiyor", inline=True)
        embed.add_field(name="Uye Sayisi", value=guild.member_count, inline=True)
        embed.add_field(name="Bot Sayisi", value=len([m for m in guild.members if m.bot]), inline=True)
        embed.add_field(name="Kanal Sayisi", value=len(guild.channels), inline=True)
        embed.add_field(name="Rol Sayisi", value=len(guild.roles), inline=True)
        embed.add_field(name="Emoji Sayisi", value=len(guild.emojis), inline=True)
        
        if guild.premium_tier > 0:
            embed.add_field(name="Boost Seviyesi", value=f"Tier {guild.premium_tier} ({guild.premium_subscription_count} boost)", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='roller')
    async def roller(self, ctx):
        guild = ctx.guild
        roles = sorted(guild.roles, key=lambda x: x.position, reverse=True)
        
        role_list = [f"`{r.position}` | {r.mention} ({len(r.members)} uye)" for r in roles if r != guild.default_role]
        
        if not role_list:
            return await ctx.send("Sunucuda rol yok!")
        
        items_per_page = 15
        pages = []
        total_pages = math.ceil(len(role_list) / items_per_page)
        
        for i in range(0, len(role_list), items_per_page):
            page_roles = role_list[i:i + items_per_page]
            embed = discord.Embed(title="📋 Sunucu Rolleri (Sayfa " + str(len(pages) + 1) + "/" + str(total_pages) + ")", 
                                  description="\n".join(page_roles), color=discord.Color.blue())
            pages.append(embed)
        
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
        else:
            view = PaginationView(pages, ctx)
            await ctx.send(embed=pages[0], view=view)
    
    @commands.command(name='emojiler')
    async def emojiler(self, ctx):
        guild = ctx.guild
        
        if not guild.emojis:
            return await ctx.send("Sunucuda emoji yok!")
        
        emojis = [f"{str(e)} `{e.name}`" for e in guild.emojis]
        
        items_per_page = 25
        pages = []
        total_pages = math.ceil(len(emojis) / items_per_page)
        
        for i in range(0, len(emojis), items_per_page):
            page_emojis = emojis[i:i + items_per_page]
            embed = discord.Embed(title="😀 Sunucu Emojileri (Sayfa " + str(len(pages) + 1) + "/" + str(total_pages) + ")", 
                                  description="\n".join(page_emojis), color=discord.Color.blue())
            pages.append(embed)
        
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
        else:
            view = PaginationView(pages, ctx)
            await ctx.send(embed=pages[0], view=view)
    
    @commands.command(name='kanallar')
    async def kanallar(self, ctx):
        guild = ctx.guild
        
        text_channels = [c.mention for c in guild.text_channels]
        voice_channels = [c.mention for c in guild.voice_channels]
        
        embed = discord.Embed(title=f"📁 {guild.name} Kanallar", color=discord.Color.blue())
        
        if text_channels:
            text_list = "\n".join(text_channels[:20])
            embed.add_field(name="💬 Metin Kanallari (" + str(len(text_channels)) + ")", value=text_list or "Yok", inline=True)
        
        if voice_channels:
            voice_list = "\n".join(voice_channels[:20])
            embed.add_field(name="🔊 Ses Kanallari (" + str(len(voice_channels)) + ")", value=voice_list or "Yok", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='yetkiler', aliases=['izinler', 'permissions'])
    async def yetkiler(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        perms = []
        for perm, value in member.guild_permissions:
            if value:
                perms.append(perm.replace("_", " ").title())
        
        if not perms:
            return await ctx.send(f"{member} uyesinin ozel yetkisi yok!")
        
        items_per_page = 20
        pages = []
        total_pages = math.ceil(len(perms) / items_per_page)
        
        for i in range(0, len(perms), items_per_page):
            page_perms = perms[i:i + items_per_page]
            embed = discord.Embed(title=f"🔑 {member} Yetkileri (Sayfa " + str(len(pages) + 1) + "/" + str(total_pages) + ")", 
                                  description="\n".join([f"✅ {p}" for p in page_perms]), color=discord.Color.blue())
            pages.append(embed)
        
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
        else:
            view = PaginationView(pages, ctx)
            await ctx.send(embed=pages[0], view=view)

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='şifre')
    async def sifre(self, ctx, uzunluk: int = 12):
        if uzunluk < 4:
            uzunluk = 4
        if uzunluk > 64:
            uzunluk = 64
        
        import string
        harfler = string.ascii_letters + string.digits + "!@#$%^&*"
        sifre = ''.join(random.choice(harfler) for _ in range(uzunluk))
        
        embed = discord.Embed(
            title="🔐 Rastgele Şifre",
            description=f"```\n{sifre}\n```",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='embed')
    async def embed_olustur(self, ctx, *, args: str = None):
        if not args:
            embed = discord.Embed(
                title="📝 Embed Oluştur",
                description="Kullanım: h!embed başlık | açıklama | renk",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        
        parcalar = args.split('|')
        baslik = parcalar[0].strip() if len(parcalar) > 0 else "Başlık"
        aciklama = parcalar[1].strip() if len(parcalar) > 1 else "Açıklama"
        
        embed = discord.Embed(
            title=baslik,
            description=aciklama,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='oylama2')
    async def oylama_yap2(self, ctx, *, soru: str = None):
        if not soru:
            await ctx.send("Bir soru belirt!")
            return
        
        embed = discord.Embed(
            title="📊 Oylama",
            description=soru,
            color=discord.Color.blue()
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
    
    @commands.command(name='anket')
    async def anket(self, ctx, sure: int = None, *, soru: str = None):
        if not soru:
            await ctx.send("Bir soru belirt!")
            return
        
        embed = discord.Embed(
            title="📊 Anket",
            description=f"**{soru}**",
            color=discord.Color.blue()
        )
        
        if sure:
            embed.set_footer(text=f"Süre: {sure} dakika | Anketi başlatan: {ctx.author}")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await msg.add_reaction("🤷")
    
    @commands.command(name='davet3')
    async def davet3(self, ctx):
        client_id = self.bot.config.get('bot', {}).get('client_id', 'YOUR_CLIENT_ID')
        embed = discord.Embed(
            title="🔗 Bot Davet Linki",
            description=f"[Botu sunucuna ekle](https://discord.com/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot)",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='sunucudavet')
    @commands.guild_only()
    async def sunucu_davet(self, ctx):
        try:
            davet = await ctx.channel.create_invite(max_age=3600, max_uses=10)
            embed = discord.Embed(
                title="🔗 Sunucu Davet Linki",
                description=f"[Davet Et]({davet.url})",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except:
            await ctx.send("Davet oluşturulamadı!")
    
    @commands.command(name='afk')
    async def afk(self, ctx, *, reason: str = "AFK"):
        await self.bot.db.execute(
            "INSERT OR REPLACE INTO afk (user_id, server_id, reason) VALUES (?, ?, ?)",
            (str(ctx.author.id), str(ctx.guild.id), reason)
        )
        await self.bot.db.commit()
        
        try:
            await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
        except:
            pass
        
        embed = discord.Embed(
            title="💤 AFK",
            description=f"{ctx.author.mention} Artik AFK!\nSebep: {reason}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='sil')
    async def sil(self, ctx, miktar: int):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Bu komutu kullanmak için yetkin yok!")
            return
        
        if miktar < 1 or miktar > 1000:
            await ctx.send("1-1000 arasında bir sayı girmelisin!")
            return
        
        deleted = await ctx.channel.purge(limit=miktar + 1)
        await ctx.send(f"✅ {len(deleted)-1} mesaj silindi!", delete_after=3)
    
    @commands.command(name='slowmode')
    async def slowmode(self, ctx, sure: int = None):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("Bu komutu kullanmak için yetkin yok!")
            return
        
        if sure is None:
            return await ctx.send(f"Mevcut slowmode: {ctx.channel.slowmode_delay} saniye")
        
        await ctx.channel.edit(slowmode_delay=sure)
        
        if sure == 0:
            await ctx.send("✅ Slowmode kapatıldı!")
        else:
            await ctx.send(f"✅ Slowmode {sure} saniye olarak ayarlandı!")
    
    @commands.command(name='kilit')
    async def kilit(self, ctx):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("Bu komutu kullanmak için yetkin yok!")
            return
        
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"🔒 {ctx.channel} kilitlendi!")
    
    @commands.command(name='ac')
    async def ac(self, ctx):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("Bu komutu kullanmak için yetkin yok!")
            return
        
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"🔓 {ctx.channel} açıldı!")
    
    @commands.command(name='duyuru')
    @commands.has_permissions(manage_messages=True)
    async def duyuru_yap(self, ctx, *, mesaj: str = None):
        if not mesaj:
            await ctx.send("Duyuru mesajı belirt!")
            return
        
        embed = discord.Embed(
            title="📢 DUYURU",
            description=mesaj,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Duyuran: {ctx.author}")
        await ctx.send(embed=embed)
    
    @commands.command(name='buton')
    async def buton(self, ctx, *, label: str = "Tıkla"):
        view = discord.ui.View()
        
        button = discord.ui.Button(label=label, style=discord.ButtonStyle.primary, custom_id="buton")
        
        async def button_callback(interaction):
            await interaction.response.send_message("Butona tıklandı!", ephemeral=True)
        
        button.callback = button_callback
        view.add_item(button)
        
        await ctx.send("Buton:", view=view)
    
    @commands.command(name='dropdown')
    async def dropdown(self, ctx, *options):
        if not options or len(options) < 2:
            await ctx.send("En az 2 seçenek belirtin!")
            return
        
        view = discord.ui.View()
        
        dropdown = discord.ui.Select(
            placeholder="Seçeneklerden birini seçin...",
            options=[discord.SelectOption(label=opt) for opt in options]
        )
        
        async def dropdown_callback(interaction):
            await interaction.response.send_message(f"Seçtin: {dropdown.values[0]}", ephemeral=True)
        
        dropdown.callback = dropdown_callback
        view.add_item(dropdown)
        
        await ctx.send("Dropdown:", view=view)

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='botbilgi')
    async def bilgi_goster(self, ctx):
        total_members = sum(g.member_count for g in self.bot.guilds)
        
        embed = discord.Embed(
            title=f"🤖 {self.bot.user} Bilgi",
            color=discord.Color.blue()
        )
        embed.add_field(name="Sunucu", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Kullanıcı", value=str(total_members), inline=True)
        embed.add_field(name="Kanal", value=str(len(self.bot.channels)), inline=True)
        embed.add_field(name="Komut", value=str(len(self.bot.commands)), inline=True)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='pingler')
    async def pingler(self, ctx):
        from datetime import datetime
        embed = discord.Embed(
            title="🏓 Ping Bilgileri",
            color=discord.Color.green()
        )
        embed.add_field(name="Bot Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Mesaj Ping", value=f"{round((datetime.now() - ctx.message.created_at).total_seconds() * 1000)}ms", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='uptime')
    async def uptime(self, ctx):
        uptime = datetime.now() - self.bot.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        embed = discord.Embed(
            title="⏰ Uptime",
            description=f"{days} gün, {hours} saat, {minutes} dakika, {seconds} saniye",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='istatistik')
    async def istatistik(self, ctx):
        total_members = sum(g.member_count for g in self.bot.guilds)
        total_channels = len(self.bot.channels)
        
        embed = discord.Embed(
            title="📊 Bot İstatistikleri",
            color=discord.Color.blue()
        )
        embed.add_field(name="Sunucu Sayısı", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Toplam Kullanıcı", value=total_members, inline=True)
        embed.add_field(name="Kanal Sayısı", value=total_channels, inline=True)
        embed.add_field(name="Komut Sayısı", value=len(self.bot.commands), inline=True)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        await ctx.send(embed=embed)

class Moderasyon2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='sustur')
    @commands.has_permissions(moderate_members=True)
    async def sustur(self, ctx, member: discord.Member, süre: int = 30):
        try:
            await member.timeout(discord.utils.utcnow() + timedelta(minutes=süre))
            await ctx.send(f"✅ {member} {süre} dakika susturuldu!")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='susturma')
    @commands.has_permissions(moderate_members=True)
    async def susturma_kaldir(self, ctx, member: discord.Member):
        try:
            await member.timeout(None)
            await ctx.send(f"✅ {member} artık konuşabilir!")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='timeout')
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, süre: int, birim: str = "m", *, sebep: str = None):
        birim = birim.lower()
        
        if birim == "s":
            delta = timedelta(seconds=süre)
        elif birim == "m":
            delta = timedelta(minutes=süre)
        elif birim == "h":
            delta = timedelta(hours=süre)
        elif birim == "d":
            delta = timedelta(days=süre)
        else:
            await ctx.send("Geçersiz birim! (s, m, h, d)")
            return
        
        try:
            await member.timeout(delta, reason=sebep)
            
            embed = discord.Embed(
                title="⏰ Timeout",
                description=f"{member.mention} {süre}{birim} süresiyle timeout yedi!",
                color=discord.Color.red()
            )
            if sebep:
                embed.add_field(name="Sebep", value=sebep, inline=False)
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='oylama-sure')
    @commands.has_permissions(manage_messages=True)
    async def oylama_sureli(self, ctx, sure: int = None, *, soru: str = None):
        if not soru:
            await ctx.send("Bir soru belirt!")
            return
        
        embed = discord.Embed(
            title="📊 Oylama",
            description=f"**{soru}**",
            color=discord.Color.blue()
        )
        
        if sure:
            embed.set_footer(text=f"Süre: {sure} dakika")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await msg.add_reaction("🤷")
    
    @commands.command(name='rol-ver')
    @commands.has_permissions(manage_roles=True)
    async def rol_ver(self, ctx, member: discord.Member, *, role: discord.Role):
        try:
            await member.add_roles(role)
            await ctx.send(f"✅ {member.mention} rolü verildi: {role.mention}")
        except Exception as e:
            await ctx.send(f"Hata: {e}")
    
    @commands.command(name='rol-al')
    @commands.has_permissions(manage_roles=True)
    async def rol_al(self, ctx, member: discord.Member, *, role: discord.Role):
        try:
            await member.remove_roles(role)
            await ctx.send(f"✅ {member.mention} rolü alındı: {role.mention}")
        except Exception as e:
            await ctx.send(f"Hata: {e}")

class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='havale')
    async def havale(self, ctx, kullanıcı: discord.Member = None, miktar: int = 0):
        if not kullanıcı or miktar <= 0:
            await ctx.send("Kullanım: h!havale @kullanıcı <miktar>")
            return
        
        gonderen_veri = await self.bot.db.get_user(str(ctx.author.id))
        
        if gonderen_veri['balance'] < miktar:
            await ctx.send("Yetersiz bakiye!")
            return
        
        await self.bot.db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (miktar, str(ctx.author.id))
        )
        await self.bot.db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (miktar, str(kullanıcı.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"✅ {miktar} TL gönderildi!")
    
    @commands.command(name='zenginler')
    async def zenginler(self, ctx):
        cursor = await self.bot.db.execute(
            "SELECT * FROM users ORDER BY balance DESC LIMIT 20"
        )
        veriler = await cursor.fetchall()
        
        items_per_page = 10
        pages = []
        total_pages = math.ceil(len(veriler) / items_per_page)
        
        for i in range(0, len(veriler), items_per_page):
            page_veriler = veriler[i:i + items_per_page]
            embed = discord.Embed(
                title="💰 En Zenginler (Sayfa " + str(len(pages) + 1) + "/" + str(total_pages) + ")",
                color=discord.Color.gold()
            )
            
            for j, v in enumerate(page_veriler, i + 1):
                user = self.bot.get_user(int(v[1]))
                isim = user.name if user else v[1]
                embed.add_field(
                    name=f"#{j} {isim}",
                    value=f"{v[3]} TL",
                    inline=False
                )
            
            pages.append(embed)
        
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
        else:
            view = PaginationView(pages, ctx)
            await ctx.send(embed=pages[0], view=view)
    
    @commands.command(name='sıralama')
    async def siralama(self, ctx):
        cursor = await self.bot.db.execute(
            "SELECT * FROM levels WHERE server_id = ? ORDER BY level DESC, xp DESC LIMIT 20",
            (str(ctx.guild.id),)
        )
        veriler = await cursor.fetchall()
        
        if not veriler:
            return await ctx.send("Bu sunucuda seviye verisi yok!")
        
        items_per_page = 10
        pages = []
        total_pages = math.ceil(len(veriler) / items_per_page)
        
        for i in range(0, len(veriler), items_per_page):
            page_veriler = veriler[i:i + items_per_page]
            embed = discord.Embed(
                title="📊 Seviye Sıralaması (Sayfa " + str(len(pages) + 1) + "/" + str(total_pages) + ")",
                color=discord.Color.blue()
            )
            
            for j, v in enumerate(page_veriler, i + 1):
                user = self.bot.get_user(int(v[2]))
                isim = user.name if user else v[2]
                embed.add_field(
                    name=f"#{j} {isim}",
                    value=f"Seviye: {v[4]} | XP: {v[3]}",
                    inline=False
                )
            
            pages.append(embed)
        
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
        else:
            view = PaginationView(pages, ctx)
            await ctx.send(embed=pages[0], view=view)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='reactionrole', aliases=['rr'])
    @commands.has_permissions(manage_roles=True)
    async def reactionrole(self, ctx, emoji: str, role: discord.Role, *, message: str = None):
        if message:
            embed = discord.Embed(title="Rol Reaksiyon", description=message, color=discord.Color.blue())
            msg = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Rol Reaksiyon", description=f"Bu mesaja tıklayarak {role.mention} rolünü alabilirsin!", color=discord.Color.blue())
            msg = await ctx.send(embed=embed)
        
        await msg.add_reaction(emoji)
        
        await self.bot.db.execute(
            "INSERT INTO reaction_roles (message_id, server_id, emoji, role_id) VALUES (?, ?, ?, ?)",
            (str(msg.id), str(ctx.guild.id), str(emoji), str(role.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"✅ Rol reaksiyonu ayarlandı! Emoji: {emoji}, Rol: {role.mention}")
    
    @commands.command(name='reroles')
    async def reroles(self, ctx):
        cursor = await self.bot.db.execute(
            "SELECT * FROM reaction_roles WHERE server_id = ?", (str(ctx.guild.id),)
        )
        roles = await cursor.fetchall()
        
        if not roles:
            return await ctx.send("Bu sunucuda rol reaksiyonu yok!")
        
        embed = discord.Embed(title="📋 Rol Reaksiyonları", color=discord.Color.blue())
        
        for role in roles:
            try:
                role_obj = ctx.guild.get_role(int(role[4]))
                embed.add_field(
                    name=f"Mesaj ID: {role[1]}",
                    value=f"Emoji: {role[3]}\nRol: {role_obj.mention if role_obj else 'Silinmiş'}",
                    inline=False
                )
            except:
                pass
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        
        cursor = await self.bot.db.execute(
            "SELECT * FROM reaction_roles WHERE message_id = ? AND server_id = ?",
            (str(payload.message_id), str(payload.guild_id))
        )
        role_data = await cursor.fetchall()
        
        for rd in role_data:
            if str(rd[3]) == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                role = guild.get_role(int(rd[4]))
                
                if role and member:
                    try:
                        await member.add_roles(role)
                    except:
                        pass
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        cursor = await self.bot.db.execute(
            "SELECT * FROM reaction_roles WHERE message_id = ? AND server_id = ?",
            (str(payload.message_id), str(payload.guild_id))
        )
        role_data = await cursor.fetchall()
        
        for rd in role_data:
            if str(rd[3]) == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                role = guild.get_role(int(rd[4]))
                
                if role and member:
                    try:
                        await member.remove_roles(role)
                    except:
                        pass

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='logayarla')
    @commands.has_permissions(manage_guild=True)
    async def logayarla(self, ctx, kanal: discord.TextChannel):
        await self.bot.db.execute(
            "UPDATE servers SET log_channel = ? WHERE server_id = ?",
            (str(kanal.id), str(ctx.guild.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"✅ Log kanalı {kanal.mention} olarak ayarlandı!")
    
    @commands.command(name='modlog')
    @commands.has_permissions(manage_guild=True)
    async def modlog(self, ctx, kanal: discord.TextChannel):
        await self.bot.db.execute(
            "UPDATE servers SET mod_log_channel = ? WHERE server_id = ?",
            (str(kanal.id), str(ctx.guild.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"✅ Mod log kanalı {kanal.mention} olarak ayarlandı!")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        try:
            cursor = await self.bot.db.execute(
                "SELECT log_channel FROM servers WHERE server_id = ?", (str(message.guild.id),)
            )
            result = await cursor.fetchone()
            
            if result and result[0]:
                channel = self.bot.get_channel(int(result[0]))
                if channel:
                    embed = discord.Embed(
                        title="🗑️ Mesaj Silindi",
                        description=f"Kanal: {message.channel.mention}\nKullanıcı: {message.author}\n\nİçerik: {message.content[:1000]}",
                        color=discord.Color.red()
                    )
                    await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        
        if before.content == after.content:
            return
        
        try:
            cursor = await self.bot.db.execute(
                "SELECT log_channel FROM servers WHERE server_id = ?", (str(before.guild.id),)
            )
            result = await cursor.fetchone()
            
            if result and result[0]:
                channel = self.bot.get_channel(int(result[0]))
                if channel:
                    embed = discord.Embed(
                        title="✏️ Mesaj Düzenlendi",
                        description=f"Kanal: {before.channel.mention}\nKullanıcı: {before.author}\n\nEski: {before.content[:500]}\nYeni: {after.content[:500]}",
                        color=discord.Color.yellow()
                    )
                    await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            cursor = await self.bot.db.execute(
                "SELECT log_channel FROM servers WHERE server_id = ?", (str(before.guild.id),)
            )
            result = await cursor.fetchone()
            
            if not result or not result[0]:
                return
            
            channel = self.bot.get_channel(int(result[0]))
            if not channel:
                return
            
            if before.nick != after.nick:
                embed = discord.Embed(
                    title="📝 Nick Değişti",
                    description=f"Kullanıcı: {before}\nEski: {before.nick}\nYeni: {after.nick}",
                    color=discord.Color.blue()
                )
                await channel.send(embed=embed)
            
            if before.roles != after.roles:
                new_roles = [r for r in after.roles if r not in before.roles]
                removed_roles = [r for r in before.roles if r not in after.roles]
                
                if new_roles:
                    embed = discord.Embed(
                        title="➕ Rol Eklendi",
                        description=f"Kullanıcı: {before}\nEklenen roller: {', '.join([r.mention for r in new_roles])}",
                        color=discord.Color.green()
                    )
                    await channel.send(embed=embed)
                
                if removed_roles:
                    embed = discord.Embed(
                        title="➖ Rol Silindi",
                        description=f"Kullanıcı: {before}\nSilinen roller: {', '.join([r.mention for r in removed_roles])}",
                        color=discord.Color.red()
                    )
                    await channel.send(embed=embed)
        except:
            pass

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='dogrula')
    async def dogrula(self, ctx):
        guild = ctx.guild
        
        verify_role = discord.utils.get(guild.roles, name="Verified")
        if not verify_role:
            verify_role = await guild.create_role(name="Verified", color=discord.Color.green())
        
        embed = discord.Embed(
            title="✅ Doğrulama",
            description="Aşağıdaki butona tıklayarak doğrulama işlemini tamamlayabilirsin!",
            color=discord.Color.green()
        )
        
        view = discord.ui.View()
        button = discord.ui.Button(label="Doğrulan", style=discord.ButtonStyle.success, custom_id="verify")
        
        async def button_callback(interaction):
            if interaction.user.guild_permissions.manage_roles:
                await interaction.response.send_message("Zaten yetkilisin!", ephemeral=True)
                return
            
            try:
                await interaction.user.add_roles(verify_role)
                await interaction.response.send_message("✅ Başarıyla doğrulandın!", ephemeral=True)
            except:
                await interaction.response.send_message("Rol verme hatası!", ephemeral=True)
        
        button.callback = button_callback
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name='verify-kanal')
    @commands.has_permissions(manage_guild=True)
    async def verify_kanal(self, ctx):
        guild = ctx.guild
        
        verify_role = discord.utils.get(guild.roles, name="Verified")
        if not verify_role:
            verify_role = await guild.create_role(name="Verified", color=discord.Color.green())
        
        embed = discord.Embed(
            title="✅ Doğrulama",
            description="Aşağıdaki butona tıklayarak doğrulama işlemini tamamlayabilirsin!",
            color=discord.Color.green()
        )
        
        view = discord.ui.View()
        button = discord.ui.Button(label="Doğrulan", style=discord.ButtonStyle.success, custom_id="verify")
        
        async def button_callback(interaction):
            try:
                await interaction.user.add_roles(verify_role)
                await interaction.response.send_message("✅ Başarıyla doğrulandın!", ephemeral=True)
            except:
                await interaction.response.send_message("Rol verme hatası!", ephemeral=True)
        
        button.callback = button_callback
        view.add_item(button)
        
        msg = await ctx.send(embed=embed, view=view)
        
        await ctx.send(f"Doğrulama kanalı oluşturuldu! Bu mesajı istediğiniz kanala taşıyabilirsiniz.")

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='tag-ekle')
    @commands.has_permissions(manage_guild=True)
    async def tag_ekle(self, ctx, isim: str, *, icerik: str):
        await self.bot.db.execute(
            "INSERT OR REPLACE INTO custom_commands (server_id, command, response, created_by) VALUES (?, ?, ?, ?)",
            (str(ctx.guild.id), isim, icerik, str(ctx.author.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"✅ Tag `{isim}` eklendi!")
    
    @commands.command(name='tag-sil')
    @commands.has_permissions(manage_guild=True)
    async def tag_sil(self, ctx, isim: str):
        cursor = await self.bot.db.execute(
            "DELETE FROM custom_commands WHERE server_id = ? AND command = ?",
            (str(ctx.guild.id), isim)
        )
        await self.bot.db.commit()
        
        if cursor.rowcount > 0:
            await ctx.send(f"✅ Tag `{isim}` silindi!")
        else:
            await ctx.send(f"❌ Tag `{isim}` bulunamadı!")
    
    @commands.command(name='taglar')
    async def taglar(self, ctx):
        cursor = await self.bot.db.execute(
            "SELECT command FROM custom_commands WHERE server_id = ?",
            (str(ctx.guild.id),)
        )
        tags = await cursor.fetchall()
        
        if not tags:
            return await ctx.send("Bu sunucuda tag yok!")
        
        tag_list = [t[0] for t in tags]
        
        items_per_page = 20
        pages = []
        total_pages = math.ceil(len(tag_list) / items_per_page)
        
        for i in range(0, len(tag_list), items_per_page):
            page_tags = tag_list[i:i + items_per_page]
            embed = discord.Embed(
                title="📋 Sunucu Tagları (Sayfa " + str(len(pages) + 1) + "/" + str(total_pages) + ")",
                description=", ".join([f"`{t}`" for t in page_tags]),
                color=discord.Color.blue()
            )
            pages.append(embed)
        
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
        else:
            view = PaginationView(pages, ctx)
            await ctx.send(embed=pages[0], view=view)
    
    @commands.command(name='tag')
    async def tag(self, ctx, isim: str = None):
        if not isim:
            return await ctx.send("Kullanım: h!tag <isim>")
        
        cursor = await self.bot.db.execute(
            "SELECT response FROM custom_commands WHERE server_id = ? AND command = ?",
            (str(ctx.guild.id), isim)
        )
        result = await cursor.fetchone()
        
        if result:
            await ctx.send(result[0])
        else:
            await ctx.send(f"❌ Tag `{isim}` bulunamadı!")

async def setup(bot):
    await bot.add_cog(Images(bot))
    await bot.add_cog(Tools(bot))
    await bot.add_cog(Info(bot))
    await bot.add_cog(Moderasyon2(bot))
    await bot.add_cog(Eco(bot))
    await bot.add_cog(ReactionRoles(bot))
    await bot.add_cog(Logging(bot))
    await bot.add_cog(Verify(bot))
    await bot.add_cog(Tags(bot))
