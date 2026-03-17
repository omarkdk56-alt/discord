import discord
from discord.ext import commands
from discord import ui
from typing import List

class HelpSelectView(ui.View):
    def __init__(self, bot, prefix, ctx):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix
        self.ctx = ctx
        
        options = [
            discord.SelectOption(label="🏠 Ana Menü", value="home", emoji="🏠"),
            discord.SelectOption(label="🛡️ Moderasyon", value="mod", emoji="🛡️"),
            discord.SelectOption(label="💰 Ekonomi", value="eko", emoji="💰"),
            discord.SelectOption(label="🎮 Eğlence", value="eglence", emoji="🎮"),
            discord.SelectOption(label="⚙️ Genel", value="genel", emoji="⚙️"),
            discord.SelectOption(label="📊 Seviye", value="seviye", emoji="📊"),
            discord.SelectOption(label="🎫 Sistem", value="sistem", emoji="🎫"),
            discord.SelectOption(label="🎵 Müzik", value="muzik", emoji="🎵"),
            discord.SelectOption(label="🎲 Oyun", value="oyun", emoji="🎲"),
            discord.SelectOption(label="🔧 Ayarlar", value="ayar", emoji="🔧"),
            discord.SelectOption(label="🌟 Özel", value="ozel", emoji="🌟"),
        ]
        
        self.select = ui.Select(placeholder="📚 Kategori seç...", options=options, min_values=1, max_values=1)
        self.select.callback = self.select_callback
        self.add_item(self.select)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Bu senin komutun değil!", ephemeral=True)
            return False
        return True
    
    async def select_callback(self, interaction: discord.Interaction):
        value = self.select.values[0]
        help_cog = self.bot.get_cog('Help')
        if help_cog:
            await help_cog.show_category(self.ctx, value, interaction)

class HelpPaginationView(ui.View):
    def __init__(self, embeds: List[discord.Embed], ctx, category_name: str, prefix: str):
        super().__init__(timeout=300)
        self.embeds = embeds
        self.ctx = ctx
        self.current_page = 0
        self.total_pages = len(embeds)
        self.category_name = category_name
        self.prefix = prefix
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Bu senin komutun değil!", ephemeral=True)
            return False
        return True

    @ui.button(label="◀", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def prev_button(self, interaction: discord.Interaction, button: ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        else:
            await interaction.response.defer()

    @ui.button(label="▶", style=discord.ButtonStyle.primary, emoji="➡️")
    async def next_button(self, interaction: discord.Interaction, button: ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        else:
            await interaction.response.defer()

    @ui.button(label="🏠", style=discord.ButtonStyle.secondary, emoji="🏠")
    async def home_button(self, interaction: discord.Interaction, button: ui.Button):
        help_cog = self.ctx.bot.get_cog('Help')
        if help_cog:
            await help_cog.send_main_menu(self.ctx, interaction)
        else:
            await interaction.response.defer()

    @ui.button(label="🗑️", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def stop_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.message.delete()
        self.stop()

    def update_buttons(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_pages - 1

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = bot.config['bot']['prefix']
        
    async def send_main_menu(self, ctx, interaction=None):
        p = self.prefix
        embed = discord.Embed(
            title="🤖 Huh Bot - En Kapsamlı Discord Botu",
            description=f"""
**Prefix:** `{p}` | **Toplam Komut:** {len(self.bot.commands)}+
**Sunucu:** {len(self.bot.guilds)} | **Kullanıcı:** {sum(g.member_count for g in self.bot.guilds)}

📌 **Huh Bot** - Discord'un en kapsamlı botu!
✨ +100 Komut | 🎵 Müzik | 💰 Ekonomi | 🎮 Eğlence
🛡️ Moderasyon | 📊 Seviye | 🎫 Ticket | 🎉 Çekiliş

Aşağıdan bir kategori seç veya butonları kullan!
            """,
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        categories = """
🛡️ **Moderasyon** - Kick, Ban, Mute, Warn, Temizle, Lock...
💰 **Ekonomi** - Bakiye, Banka, Slot, Çalış, Market...
🎮 **Eğlence** - 8ball, Zar, Hack, Ship, TKM, Waifu...
⚙️ **Genel** - Ping, Avatar, Profil, AFK, SunucuBilgi...
📊 **Seviye** - XP, Sıralama, Rank, Ödüller...
🎫 **Sistem** - Ticket, Çekiliş, Anket, Duyuru...
🎵 **Müzik** - Çal, Dur, Atla, Ses, Liste...
🎲 **Oyun** - TicTacToe, Savaş, Quiz, AdamAsmaca...
🔧 **Ayarlar** - Welcome, Log, Otorol, AntiSpam...
🌟 **Özel** - Yetkili Komutları, Özel Sistemler...
        """
        embed.add_field(name="📋 Kategoriler", value=categories, inline=False)
        
        embed.add_field(
            name="⚡ Popüler Komutlar",
            value=f"""
`{p}yardim` - Bu menüyü göster
`{p}ping` - Bot pingini göster
`{p}avatar` - Avatarını göster
`{p}bakiye` - Paranı göster
`{p}seviye-goster` - Seviyeni göster
`{p}8ball <soru>` - Evet/Hayır sor
`{p}slot <miktar>` - Slot oyna
`{p}cal` - Müzik çal
            """,
            inline=False
        )
        
        embed.set_footer(text="Huh Bot | Discord'un En Kapsamlı Botu | +100 Komut", icon_url=self.bot.user.display_avatar.url)
        
        view = HelpSelectView(self.bot, self.prefix, ctx)
        
        if interaction:
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await ctx.send(embed=embed, view=view)
    
    async def show_category(self, ctx, category, interaction=None):
        p = self.prefix
        embeds = []
        
        if category == "home":
            await self.send_main_menu(ctx, interaction)
            return
        
        elif category == "mod":
            for i in range(0, 40, 10):
                embed = discord.Embed(
                    title="🛡️ Moderasyon Komutları",
                    description=f"{self.bot.user.name} - Moderasyon (Sayfa {i//10+1})",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                
                cmds1 = [
                    f"`{p}kick <üye> [sebep]` - Üyeyi sunucudan at",
                    f"`{p}ban <üye> [gün> [sebep]` - Üyeyi banla",
                    f"`{p}unban <user_id>` - Banı kaldır",
                    f"`{p}softban <üye> [sebep]` - Soft ban",
                    f"`{p}mute <üye> <dakika> [sebep]` - Sustur",
                    f"`{p}unmute <üye>` - Susturmayı kaldır",
                    f"`{p}vmute <üye> [sebep]` - Ses susturma",
                    f"`{p}vunmute <üye>` - Ses susturmayı kaldır",
                    f"`{p}tempmute <üye> <süre>` - Geçici susturma",
                    f"`{p}warn <üye> [sebep]` - Uyarı ver",
                ][i:i+10]
                
                cmds2 = [
                    f"`{p}warns [üye]` - Uyarıları göster",
                    f"`{p}warnsil <üye> <sayı>` - Uyarı sil",
                    f"`{p}sil <miktar>` - Mesajları sil",
                    f"`{p}sil <sayı> <kanal>` - Kanalda sil",
                    f"`{p}slowmode [saniye]` - Yavaşmod",
                    f"`{p}lock [kanal]` - Kanalı kilitle",
                    f"`{p}unlock [kanal]` - Kanalı aç",
                    f"`{p}lockall` - Tüm kanalları kilitle",
                    f"`{p}unlockall` - Tüm kanalları aç",
                    f"`{p}nuke` - Kanalı sıfırla",
                ][i:i+10] if i < 30 else []
                
                embed.add_field(name="🔨 Yetkili", value="\n".join(cmds1), inline=False)
                if cmds2:
                    embed.add_field(name="🔒 Kanal", value="\n".join(cmds2), inline=False)
                
                embed.set_footer(text=f"Sayfa {i//10+1}/4 | Ana: {p}yardim", icon_url=self.bot.user.display_avatar.url)
                embeds.append(embed)
        
        elif category == "eko":
            for i in range(0, 50, 10):
                embed = discord.Embed(
                    title="💰 Ekonomi Komutları",
                    description=f"{self.bot.user.name} - Ekonomi (Sayfa {i//10+1})",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                
                cmds1 = [
                    f"`{p}bakiye [üye]` - Paranı göster",
                    f"`{p}banka` - Banka durumu",
                    f"`{p}banka para <miktar>` - Para yatır",
                    f"`{p}banka cek <miktar>` - Para çek",
                    f"`{p}gunluk` - Günlük para (24s)",
                    f"`{p}haftalık` - Haftalık para (7g)",
                    f"`{p}aylık` - Aylık para (30g)",
                    f"`{p}calis` - Çalış para kazan",
                    f"`{p}soyledin` - Şarkı söyle para kazan",
                    f"`{p}paraver <üye> <miktar>` - Para gönder",
                ][i:i+10]
                
                cmds2 = [
                    f"`{p}slot <miktar>` - Slot makinesi",
                    f"`{p}zar <miktar>` - Zar at",
                    f"`{p}blackjack <miktar>` - Blackjack oyna",
                    f"`{p}coinflip <miktar> <yazı/tura>` - Coin flip",
                    f"`{p}market` - Marketi göster",
                    f"`{p}al <eşya>` - Eşya satin al",
                    f"`{p}envanter` - Eşyalarını göster",
                    f"`{p}market-satan <eşya>` - Eşya sat",
                    f"`{p}borc <üye> <miktar>` - Borç ver",
                    f"`{p}borcöde <üye>` - Borç öde",
                ][i:i+10] if i < 40 else []
                
                cmds3 = [
                    f"`{p}çalış-tren` - Tren çalış",
                    f"`{p}çalış-maden` - Madencilik",
                    f"`{p}çalış-çiftlik` - Çiftlik",
                    f"`{p}iş-ilanları` - İş ilanları",
                    f"`{p}iş-başvuru <iş>` - İşe başvur",
                    f"`{p}maaş` - Maaşını al",
                    f"`{p}zenginler` - En zenginler",
                    f"`{p}harcama <miktar>` - Para harca",
                    f"`{p}vergi` - Vergi öde",
                    f"`{p}faiz` - Banka faizi al",
                ][i:i+10] if i < 40 else []
                
                embed.add_field(name="💵 Para", value="\n".join(cmds1), inline=False)
                if cmds2:
                    embed.add_field(name="🎰 Kumar", value="\n".join(cmds2), inline=False)
                if cmds3 and i >= 40:
                    embed.add_field(name="💼 İş", value="\n".join(cmds3), inline=False)
                
                embed.set_footer(text=f"Sayfa {i//10+1}/5 | Ana: {p}yardim", icon_url=self.bot.user.display_avatar.url)
                embeds.append(embed)
        
        elif category == "eglence":
            for i in range(0, 50, 10):
                embed = discord.Embed(
                    title="🎮 Eğlence Komutları",
                    description=f"{self.bot.user.name} - Eğlence (Sayfa {i//10+1})",
                    color=discord.Color.purple()
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                
                cmds1 = [
                    f"`{p}8ball <soru>` - Evet/hayır cevap",
                    f"`{p}yazitura` - Yazı tura at",
                    f"`{p}zar` - 1-6 arası zar at",
                    f"`{p}rastgele <şey1> <şey2>...` - Rastgele seç",
                    f"`{p}hack <üye>` - (şaka) Hackle",
                    f"`{p}ship <üye1> <üye2>` - Eşleştir",
                    f"`{p}kaçcm <üye>` - (şaka) Ölç",
                    f"`{p}saka` - Rastgele şaka",
                    f"`{p}yemek` - Yemek öner",
                    f"`{p}şiir` - Rastgele şiir",
                ][i:i+10]
                
                cmds2 = [
                    f"`{p}tkm <taş/kağıt/makas>` - TKM oyna",
                    f"`{p}ascii <metin>` - ASCII sanatı",
                    f"`{p}fallar` - Kahve falı",
                    f"`{p}fal` - Tarot falı",
                    f"`{p}rol [kategori]` - Rastgele rol",
                    f"`{p}cool` - Coolluk ölçer",
                    f"`{p}waifu` - Random waifu",
                    f"`{p}nefret` - Nefret ölçer",
                    f"`{p}aşkölçer <üye>` - Aşk ölçer",
                    f"`{p}randomüye` - Rastgele üye",
                ][i:i+10] if i < 40 else []
                
                cmds3 = [
                    f"`{p}bilgi` - Bilgi yarışması",
                    f"`{p}matematik` - Matematik oyunu",
                    f"`{p}tahmin <sayı>` - Sayı tahmin",
                    f"`{p}fbi` - FBI OPEN UP",
                    f"`{p}np` - Şu an çalan şarkı",
                    f"`{p}qrcode <text>` - QR code oluştur",
                    f"`{p}steam <oyun>` - Steam arama",
                    f"`{p}mcskin <nick>` - MC skin göster",
                    f"`{p}wikipedia <konu>` - Wikipedia ara",
                    f"`{p}youtube <ara>` - YouTube ara",
                ][i:i+10] if i < 40 else []
                
                # Sayfa 2 (i=10) - Yeni komutlar
                if i == 10:
                    cmds1 = [
                        f"`{p}kapismac` - Futbol maçı simülasyonu",
                        f"`{p}dortbasamak` - 4 basamaklı rastgele sayı",
                        f"`{p}zarat` - Zar at (2 zar)",
                        f"`{p}sec <seçenek1> <seçenek2>` - Rastgele seçim",
                        f"`{p}dovus` - Dövüş oyunu",
                        f"`{p}bilgi` - Rastgele ilginç bilgi",
                        f"`{p}saka` - Komik şaka",
                        f"`{p}ascii <yazı>` - ASCII sanat",
                        f"`{p}emojiyap <yazı>` - Emojiye çevir",
                        f"`{p}kupacevir` - Yazı tura",
                    ]
                    cmds2 = [
                        f"`{p}sans <oran>` - Şansını dene (1-100)",
                        f"`{p}savasp <üye>` - Savaş simülasyonu",
                        f"`{p}taskagit <taş/kağıt/makas>` - TKM oyna",
                        f"`{p}alkışla` - Alkış emoji",
                        f"`{p}emoji <sayı>` - Rastgele emoji",
                        f"`{p}fıkra` - Komik fıkra",
                        f"`{p}komik` - Komik resim",
                        f"`{p}gif` - Rastgele GIF",
                        f"`{p}dans` - Dans animasyonu",
                        f"`{p}alkis` - Alkış animasyonu",
                    ]
                    cmds3 = []
                
                # Sayfa 3 (i=20)
                if i == 20:
                    cmds1 = [
                        f"`{p}hayvan` - Rastgele hayvan",
                        f"`{p}yemek` - Yemek emoji",
                        f"`{p}içecek` - İçecek emoji",
                        f"`{p}meyve` - Meyve emoji",
                        f"`{p}spor` - Spor emoji",
                        f"`{p}araba` - Araba emoji",
                        f"`{p}müzik2` - Müzik önerisi",
                        f"`{p}film` - Film önerisi",
                        f"`{p}dizi` - Dizi önerisi",
                        f"`{p}renk2` - Renk önerisi",
                    ]
                    cmds2 = []
                    cmds3 = []
                
                # Sayfa 4 (i=30)
                if i == 30:
                    cmds1 = [
                        f"`{p}sec <şey1> <şey2>` - Seçim yap",
                        f"`{p}şaka` - Rastgele şaka",
                        f"`{p}fıkra` - Türk fıkrası",
                        f"`{p}komik` - Komik içerik",
                        f"`{p}dans` - Dans et",
                        f"`{p}alkis` - Alkış",
                        f"`{p}renk` - Rastgele renk",
                        f"`{p}dilek <dilek>` - Dilek tut",
                        f"`{p}emojiyap <yazı>` - Emoji yap",
                        f"`{p}kupacevir` - Yazı tura",
                    ]
                    cmds2 = []
                    cmds3 = []
                
                embed.add_field(name="🎱 Eğlence", value="\n".join(cmds1), inline=False)
                if cmds2:
                    embed.add_field(name="🎭 Şaka", value="\n".join(cmds2), inline=False)
                if cmds3 and i >= 40:
                    embed.add_field(name="🔍 Araçlar", value="\n".join(cmds3), inline=False)
                
                embed.set_footer(text=f"Sayfa {i//10+1}/5 | Ana: {p}yardim", icon_url=self.bot.user.display_avatar.url)
                embeds.append(embed)
        
        elif category == "genel":
            for i in range(0, 40, 10):
                embed = discord.Embed(
                    title="⚙️ Genel Komutlar",
                    description=f"{self.bot.user.name} - Genel (Sayfa {i//10+1})",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                
                # Sayfa 1 (i=0)
                if i == 0:
                    cmds1 = [
                        f"`{p}ping` - Bot gecikmesi",
                        f"`{p}pong` - Ping pong",
                        f"`{p}bot` - Bot bilgileri",
                        f"`{p}uptime` - Bot uptime",
                        f"`{p}istatistik` - İstatistikler",
                        f"`{p}link` - Davet linki",
                        f"`{p}davet` - Davet bilgi",
                        f"`{p}say` - Bot söyle",
                        f"`{p}yaz <mesaj>` - Yazdır",
                        f"`{p}embed <mesaj>` - Embed yaz",
                    ]
                    cmds2 = [
                        f"`{p}avatar [üye]` - Avatar göster",
                        f"`{p}profil [üye]` - Profil göster",
                        f"`{p}banner [üye]` - Banner göster",
                        f"`{p}kullanıcıbilgi [üye]` - Kullanıcı bilgi",
                        f"`{p}sunucubilgi` - Sunucu bilgileri",
                        f"`{p}roller` - Rol listesi",
                        f"`{p}emojiler` - Emoji listesi",
                        f"`{p}kanallar` - Kanal listesi",
                        f"`{p}yetkiler [üye]` - Yetkileri göster",
                        f"`{p}kanalbilgi [kanal]` - Kanal bilgi",
                    ]
                    cmds3 = []
                
                # Sayfa 2 (i=10)
                elif i == 10:
                    cmds1 = [
                        f"`{p}saat` - Şu anki saat",
                        f"`{p}takvim` - Bugünün tarihi",
                        f"`{p}afk [sebep]` - AFK moduna gir",
                        f"`{p}şifre [uzunluk]` - Rastgele şifre",
                        f"`{p}rolbilgi <rol>` - Rol bilgi",
                        f"`{p}emoji-bilgi <emoji>` - Emoji bilgi",
                        f"`{p}randomemoji` - Rastgele emoji",
                        f"`{p}toplamüye` - Toplam üye",
                        f"`{p}davetbilgi` - Davet bilgi",
                        f"`{p}sunucuicon` - Sunucu ikonu",
                    ]
                    cmds2 = []
                    cmds3 = []
                
                else:
                    cmds1 = [
                        f"`{p}ping` - Bot gecikmesi",
                        f"`{p}pong` - Ping pong",
                        f"`{p}bot` - Bot bilgileri",
                        f"`{p}uptime` - Bot uptime",
                        f"`{p}istatistik` - İstatistikler",
                        f"`{p}link` - Davet linki",
                        f"`{p}davet` - Davet bilgi",
                        f"`{p}say` - Bot söyle",
                        f"`{p}yaz <mesaj>` - Yazdır",
                        f"`{p}embed <mesaj>` - Embed yaz",
                    ][:10]
                    cmds2 = []
                    cmds3 = []
                
                embed.add_field(name="🔗 Bot", value="\n".join(cmds1), inline=False)
                if cmds2:
                    embed.add_field(name="👤 Kullanıcı", value="\n".join(cmds2), inline=False)
                if cmds3:
                    embed.add_field(name="⏰ Diğer", value="\n".join(cmds3), inline=False)
                
                embed.set_footer(text=f"Sayfa {i//10+1}/2 | Ana: {p}yardim", icon_url=self.bot.user.display_avatar.url)
                embeds.append(embed)
        
        elif category == "seviye":
            for i in range(0, 20, 10):
                embed = discord.Embed(
                    title="📊 Seviye Sistemi",
                    description=f"{self.bot.user.name} - Seviye (Sayfa {i//10+1})",
                    color=discord.Color.orange()
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                
                cmds1 = [
                    f"`{p}seviye-goster [üye]` - Seviyeni göster",
                    f"`{p}siralama` - En iyiler sıralaması",
                    f"`{p}xp [üye]` - XP göster",
                    f"`{p}rank [üye]` - Rank göster",
                    f"`{p}setxp <üye> <xp>` - XP ayarla (admin)",
                    f"`{p}setlevel <üye> <seviye>` - Seviye ayarla",
                    f"`{p}seviye-sifirla` - Seviyeni sıfırla",
                    f"`{p}xp-ekle <üye> <xp>` - XP ekle",
                    f"`{p}xp-sil <üye> <xp>` - XP sil",
                    f"`{p}seviye-ödül` - Ödülleri göster",
                ][i:i+10]
                
                cmds2 = [
                    f"🎖️ Seviye 5 → Acemi",
                    f"🎖️ Seviye 10 → Amatör",
                    f"🎖️ Seviye 20 → Orta",
                    f"🎖️ Seviye 30 → Uzman",
                    f"🎖️ Seviye 50 → Efsane",
                    f"🎖️ Seviye 75 → Master",
                    f"🎖️ Seviye 100 → Legend",
                    f"🎖️ Seviye 150 → Efsane",
                    f"🎖️ Seviye 200 → Titan",
                    f"🎖️ Seviye 500 → Tanrı",
                ][i:i+10] if i < 10 else []
                
                embed.add_field(name="📈 Komutlar", value="\n".join(cmds1), inline=False)
                if cmds2:
                    embed.add_field(name="🎖️ Ödüller", value="\n".join(cmds2), inline=False)
                
                embed.set_footer(text=f"Sayfa {i//10+1}/2 | Ana: {p}yardim", icon_url=self.bot.user.display_avatar.url)
                embeds.append(embed)
        
        elif category == "sistem":
            for i in range(0, 40, 10):
                embed = discord.Embed(
                    title="🎫 Sistem Komutları",
                    description=f"{self.bot.user.name} - Sistem (Sayfa {i//10+1})",
                    color=discord.Color.teal()
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                
                cmds1 = [
                    f"`{p}ticket-olustur` - Ticket aç",
                    f"`{p}ticket-kapat` - Ticket kapat",
                    f"`{p}ticket-panel` - Panel oluştur",
                    f"`{p}ticket-kanal <kanal>` - Ticket kanalı ayarla",
                    f"`{p}cekilis <süre> <kazanan> <ödül>` - Çekiliş",
                    f"`{p}cekilis-bitir <mesaj>` - Çekilişi bitir",
                    f"`{p}cekilis-liste` - Aktif çekilişler",
                    f"`{p}anket <soru>` - Anket yap",
                    f"`{p}oylama <soru>` - Oylama yap",
                    f"`{p}duyuru <mesaj>` - Duyuru yap",
                ][i:i+10]
                
                cmds2 = [
                    f"`{p}embed-olustur` - Embed oluştur",
                    f"`{p}buton-olustur` - Butonlu mesaj",
                    f"`{p}dropdown-olustur` - Dropdown menü",
                    f"`{p}reactionrole` - Reaction role",
                    f"`{p}reroles` - Aktif roller",
                    f"`{p}dogrula` - Doğrulama sistemi",
                    f"`{p}verify-kanal <kanal>` - Verify kanalı",
                    f"`{p}logayarla <kanal>` - Log kanalı",
                    f"`{p}modlog <kanal>` - Mod log",
                    f"`{p}sayaç <sayı>` - Sayaç sistemi",
                ][i:i+10] if i < 30 else []
                
                cmds3 = [
                    f"`{p}otocevap-ekle <kelime> <cevap>` - Oto cevap",
                    f"`{p}otocevap-sil <kelime>` - Oto cevap sil",
                    f"`{p}otocevap-liste` - Oto cevaplar",
                    f"`{p}sayaç-kanal <kanal>` - Sayaç kanalı",
                    f"`{p}sayaç-mesaj <mesaj>` - Sayaç mesajı",
                    f"`{p}otosil <kelime>` - Otomatik silme",
                    f"`{p}otoembed <kelime> <mesaj>` - Auto embed",
                    f"`{p}otoemoji <kelime> <emoji>` - Auto emoji",
                    f"`{p}otoses <kelime> <ses>` - Auto ses",
                    f"`{p}otooylama <kelime>` - Auto oylama",
                ][i:i+10] if i < 30 else []
                
                embed.add_field(name="🎟️ Ticket", value="\n".join(cmds1[:5]), inline=False)
                embed.add_field(name="📢 Duyuru", value="\n".join(cmds1[5:]), inline=False)
                if cmds2:
                    embed.add_field(name="🔧 Özel", value="\n".join(cmds2), inline=False)
                if cmds3 and i >= 30:
                    embed.add_field(name="🤖 Otomatik", value="\n".join(cmds3), inline=False)
                
                embed.set_footer(text=f"Sayfa {i//10+1}/4 | Ana: {p}yardim", icon_url=self.bot.user.display_avatar.url)
                embeds.append(embed)
        
        elif category == "muzik":
            embed = discord.Embed(
                title="🎵 Müzik Komutları",
                description=f"{self.bot.user.name} - Müzik Sistemi",
                color=discord.Color.magenta()
            )
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.add_field(
                name="🎶 Çalma",
                value=f"""
`{p}cal <url/şarkı>` - Şarkı çal
`{p}dur` - Durdur
`{p}durdur` - Tamamen durdur
`{p}atla` - Sonraki şarkı
`{p}onceki` - Önceki şarkı
`{p}liste` - Şarkı listesi
`{p}sıra` - Kuyruk
`{p}kuyruk <şarkı>` - Kuyruğa ekle
`{p}karistir` - Karıştır
`{p}tekrar` - Tekrar modu
                """,
                inline=False
            )
            embed.add_field(
                name="🔊 Kontrol",
                value=f"""
`{p}ses [0-100]` - Ses seviyesi
`{p}dakika` - Mevcut süre
`{p}ileri <saniye>` - İlerle
`{p}geri <saniye>` - Geri al
`{p}loop` - Döngü modu
`{p}shuffle` - Karıştır
`{p}bass <0-10>` - Bass boost
`{p}equalizer` - Eşitleyici
`{p}filtre <mod>` - Ses filtresi
`{p}kapat` - Müziği kapat
                """,
                inline=False
            )
            embed.add_field(
                name="📋 Playlist",
                value=f"""
`{p}playlist-ekle <isim> <url>` - Playlist ekle
`{p}playlist-sil <isim>` - Playlist sil
`{p}playlistler` - Playlist listele
`{p}playlist-cal <isim>` - Playlist çal
`{p}playlist-ekle-şarkı <pl> <url>` - Şarkı ekle
`{p}playlist-sil-şarkı <pl> <sıra>` - Şarkı sil
                """,
                inline=False
            )
            embed.set_footer(text=f"Ana menü: {p}yardim", icon_url=self.bot.user.display_avatar.url)
            embeds.append(embed)
        
        elif category == "oyun":
            for i in range(0, 30, 10):
                embed = discord.Embed(
                    title="🎲 Oyun Komutları",
                    description=f"{self.bot.user.name} - Oyun (Sayfa {i//10+1})",
                    color=discord.Color.dark_gold()
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                
                cmds1 = [
                    f"`{p}tictactoe` - Tic Tac Toe",
                    f"`{p}tictactoe <üye>` - TTT 2 kişi",
                    f"`{p}savas <üye>` - Savaş oyunu",
                    f"`{p}bilgi` - Bilgi yarışması",
                    f"`{p}adamasmaca` - Adam Asmaca",
                    f"`{p}quiz` - Quiz oyunu",
                    f"`{p}matematik` - Matematik oyunu",
                    f"`{p}tahmin <sayı>` - Sayı tahmin",
                    f"`{p}xox` -amatris oyunu",
                    f"`{p}hafıza` - Hafıza oyunu",
                ][i:i+10]
                
                cmds2 = [
                    f"`{p}kelime` - Kelime oyunu",
                    f"`{p}rusruleti` - Rus ruleti",
                    f"`{p}sansoyunu` - Şans oyunu",
                    f"`{p}darts` - Darts oyunu",
                    f"`{p}basketbol` - Basketbol",
                    f"`{p}futbol` - Futbol",
                    f"`{p}penaltı` - Penaltı",
                    f"`{p}satranç` - Satranç",
                    f"`{p}go` - Go oyunu",
                    f"`{p}mancala` - Mancala",
                ][i:i+10] if i < 20 else []
                
                embed.add_field(name="🎮 Oyunlar", value="\n".join(cmds1), inline=False)
                if cmds2:
                    embed.add_field(name="🕹️ Diğer", value="\n".join(cmds2), inline=False)
                
                embed.set_footer(text=f"Sayfa {i//10+1}/3 | Ana: {p}yardim", icon_url=self.bot.user.display_avatar.url)
                embeds.append(embed)
        
        elif category == "ayar":
            embed = discord.Embed(
                title="🔧 Ayarlar",
                description=f"{self.bot.user.name} - Ayarlar",
                color=discord.Color.dark_gray()
            )
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.add_field(
                name="👋 Hoş Geldin",
                value=f"""
`{p}hosgeldin-ayarla <kanal>` - Hoş geldin kanalı
`{p}hosgeldin-mesaj <mesaj>` - Hoş geldin mesajı
`{p}hosgeldin-sil` - Hoş geldini kaldır
`{p}gulegule-ayarla <kanal>` - Gidenler kanalı
`{p}gulegule-mesaj <mesaj>` - Gidenler mesajı
`{p}otorol <rol>` - Otorol ayarla
`{p}otorol-sil` - Otorolu kaldır
`{p}bot-rol <rol>` - Bot rolü ayarla
                """,
                inline=False
            )
            embed.add_field(
                name="🛡️ Güvenlik",
                value=f"""
`{p}anti-raid` - Anti-raid aç/kapa
`{p}anti-raid-sayı <sayı>` - Raid sayısı
`{p}anti-spam` - Anti-spam aç/kapa
`{p}anti-spam-süre <süre>` - Spam süresi
`{p}anti-link` - Anti-link aç/kapa
`{p}caps-lock-engel` - Caps engeli aç/kapa
`{p}kelime-filtresi <kelime>` - Kelime ekle
`{p}kelime-filtresi-sil <kelime>` - Kelime sil
                """,
                inline=False
            )
            embed.add_field(
                name="📊 Diğer",
                value=f"""
`{p}sayaç-ayarla <sayı>` - Sayaç
`{p}sayaç-kanal <kanal>` - Sayaç kanalı
`{p}sayaç-mesaj <mesaj>` - Sayaç mesajı
`{p}sayaç-sil` - Sayaç kaldır
`{p}prefix-ayarla <prefix>` - Prefix değiştir
`{p}prefix-sifirla` - Prefix sıfırla
`{p}dil-ayarla <tr/en>` - Dil ayarla
`{p}sifirla` - Tüm ayarları sıfırla
                """,
                inline=False
            )
            embed.set_footer(text=f"Ana menü: {p}yardim", icon_url=self.bot.user.display_avatar.url)
            embeds.append(embed)
        
        elif category == "ozel":
            embed = discord.Embed(
                title="🌟 Özel Komutlar",
                description=f"{self.bot.user.name} - Özel Sistemler",
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            embed.add_field(
                name="👑 Owner Komutları",
                value=f"""
`{p}eval <kod>` - Kod çalıştır
`{p}shell <komut>` - Shell komutu
`{p}reload` - Botu yenile
`{p}stop` - Botu durdur
`{p}restart` - Botu yeniden başlat
`{p}guilds` - Sunucu listesi
`{p}leave <sunucu>` - Sunucudan çık
`{p}dm <üye> <mesaj>` - DM at
                """,
                inline=False
            )
            embed.add_field(
                name="🎁 Özel Sistemler",
                value=f"""
`{p}premium` - Premium bilgi
`{p}premium-ekle <üye> <gün>` - Premium ekle
`{p}premium-sil <üye>` - Premium sil
`{p}destek` - Destek sunucusu
`{p}OyVer` - Oy ver linki
`{p}oyver` - Oy ver
`{p}Davet` - Bot davet
`{p}kod` - Kaynak kod
                """,
                inline=False
            )
            embed.add_field(
                name="🎉 Etkinlik",
                value=f"""
`{p}etkinlik-baslat <tür>` - Etkinlik başlat
`{p}etkinlik-bitir` - Etkinlik bitir
`{p}etkinlik-katıl` - Etkinliğe katıl
`{p}etkinlik-ödül` - Ödül ayarla
`{p}etrehber` - Etkinlik rehberi
`{p}youtuber <isim>` - YouTuber bilgi
`{p}twitch <isim>` - Twitch bilgi
`{p}steam <isim>` - Steam bilgi
                """,
                inline=False
            )
            embed.set_footer(text=f"Ana menü: {p}yardim", icon_url=self.bot.user.display_avatar.url)
            embeds.append(embed)
        
        if embeds:
            view = HelpPaginationView(embeds, ctx, category, p)
            if interaction:
                await interaction.response.edit_message(embed=embeds[0], view=view)
            else:
                await ctx.send(embed=embeds[0], view=view)
    
    @commands.command(name='yardim', aliases=['yardım', 'help', 'h', 'yardimlar'])
    async def yardim(self, ctx):
        await self.send_main_menu(ctx)
    
    @commands.command(name='mod', aliases=['modyardim', 'mod-help'])
    async def mod_help(self, ctx):
        await self.show_category(ctx, "mod")
    
    @commands.command(name='eko', aliases=['ekonomiyardim', 'eko-help'])
    async def economy_help(self, ctx):
        await self.show_category(ctx, "eko")
    
    @commands.command(name='eglence', aliases=['funyardim', 'fun-help'])
    async def fun_help(self, ctx):
        await self.show_category(ctx, "eglence")
    
    @commands.command(name='genel', aliases=['utilityyardim', 'genel-help'])
    async def utility_help(self, ctx):
        await self.show_category(ctx, "genel")
    
    @commands.command(name='seviye', aliases=['levelyardim', 'seviye-help'])
    async def level_help(self, ctx):
        await self.show_category(ctx, "seviye")
    
    @commands.command(name='sistem', aliases=['systemyardim', 'sistem-help'])
    async def system_help(self, ctx):
        await self.show_category(ctx, "sistem")
    
    @commands.command(name='muzik', aliases=['musicyardim', 'muzik-help'])
    async def music_help(self, ctx):
        await self.show_category(ctx, "muzik")
    
    @commands.command(name='oyun', aliases=['gamesyardim', 'oyun-help'])
    async def games_help(self, ctx):
        await self.show_category(ctx, "oyun")
    
    @commands.command(name='ayar', aliases=['settingsyardim', 'ayar-help'])
    async def settings_help(self, ctx):
        await self.show_category(ctx, "ayar")
    
    @commands.command(name='ozel', aliases=['special', 'ozel-help'])
    async def special_help(self, ctx):
        await self.show_category(ctx, "ozel")

async def setup(bot):
    await bot.add_cog(Help(bot))
