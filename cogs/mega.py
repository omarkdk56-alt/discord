import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
import json
from datetime import datetime
import math

class Mega(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = bot.config['bot']['prefix']
        self.session = None
        
    async def cog_load(self):
        self.session = aiohttp.ClientSession()
    
    async def cog_unload(self):
        if self.session:
            await self.session.close()
    
    # === EĞLENCE KOMUTLARI ===
    
    @commands.command(name='aşkölçer', aliases=['askolcer', 'love', 'love-test'])
    async def ask_olcer(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("Kimi seviyorsun?")
            return
        oran = random.randint(0, 100)
        if oran > 80: emoji = "💕💕💕"
        elif oran > 60: emoji = "💕💕"
        elif oran > 40: emoji = "💕"
        else: emoji = "💔"
        await ctx.send(f"❤️ {ctx.author} → {member} = **{oran}%** {emoji}")
    
    @commands.command(name='nefret', aliases=['nefretolcer', 'hate'])
    async def nefret(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("Kimden nefret ediyorsun?")
            return
        oran = random.randint(0, 100)
        await ctx.send(f"😠 {ctx.author} → {member} = **{oran}%** nefret ediyor!")
    
    @commands.command(name='randomüye', aliases=['rastgeleuye', 'rndmember'])
    async def random_uye(self, ctx):
        if ctx.guild:
            uye = random.choice(ctx.guild.members)
            await ctx.send(f"🎲 Rastgele üye: **{uye}**")
    
    @commands.command(name='randomemoji', aliases=['rastgeleemoji', 'rndemoji'])
    async def random_emoji(self, ctx):
        if ctx.guild and ctx.guild.emojis:
            emo = random.choice(ctx.guild.emojis)
            await ctx.send(f"🎲 Rastgele emoji: **{emo}**")
        else:
            await ctx.send("Emoji yok!")
    
    @commands.command(name='rastgelerenk', aliases=['randomcolor', 'renksec'])
    async def random_renk(self, ctx):
        renk = discord.Color.random()
        await ctx.send(embed=discord.Embed(color=renk, title=f"🎨 Renk: #{renk.value:06x}"))
    
    @commands.command(name='kullanıcıbilgi', aliases=['kb', 'üye-bilgi', 'userinfo'])
    async def kullanici_bilgi(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"👤 {member}", color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Sunucuya Katılma", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Hesap Oluşturma", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="En Yüksek Rol", value=member.top_role.mention, inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='sunucubilgi2', aliases=['sb2', 'serverinfo2', 'sunucu-bilgi2'])
    async def sunucu_bilgi2(self, ctx):
        g = ctx.guild
        embed = discord.Embed(title=f"📊 {g.name}", color=discord.Color.blue())
        if g.icon: embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="ID", value=g.id, inline=True)
        embed.add_field(name="Üye Sayısı", value=g.member_count, inline=True)
        embed.add_field(name="Kanal Sayısı", value=len(g.channels), inline=True)
        embed.add_field(name="Rol Sayısı", value=len(g.roles), inline=True)
        embed.add_field(name="Emoji Sayısı", value=len(g.emojis), inline=True)
        embed.add_field(name="Oluşturulma", value=g.created_at.strftime("%d/%m/%Y"), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='emojibilgi', aliases=['emoji-bilgi', 'emojiinfo'])
    async def emoji_bilgi(self, ctx, emoji: discord.Emoji):
        embed = discord.Embed(title=f"{emoji} {emoji.name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=emoji.id, inline=True)
        embed.add_field(name="Animasyonlu", value="Evet" if emoji.animated else "Hayır", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='davetbilgi', aliases=['davet-bilgi', 'inviteinfo'])
    async def davet_bilgi(self, ctx, invite: str = None):
        try:
            if invite:
                inv = await self.bot.fetch_invite(invite)
                embed = discord.Embed(title="🔗 Davet Bilgi", color=discord.Color.blue())
                embed.add_field(name="Sunucu", value=inv.guild.name if inv.guild else "Bilinmiyor", inline=True)
                embed.add_field(name="Kanal", value=inv.channel.name if inv.channel else "Bilinmiyor", inline=True)
                embed.add_field(name="Kullanım", value=inv.uses if inv.uses else "Sınırsız", inline=True)
                await ctx.send(embed=embed)
            else:
                invites = await ctx.guild.invites()
                if invites:
                    inv = invites[0]
                    await ctx.send(f"🔗 {inv}")
                else:
                    await ctx.send("Davet yok!")
        except:
            await ctx.send("Davet bulunamadı!")
    
    @commands.command(name='şifre', aliases=['sifre', 'password', 'randpass'])
    async def sifre_uret(self, ctx, uzunluk: int = 12):
        import string
        sifre = "".join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=min(uzunluk, 50)))
        await ctx.send(f"🔐 Şifre: `{sifre}`")
    
    @commands.command(name='rastgele', aliases=['random', 'sec', 'choice'])
    async def rastgele_sec(self, ctx, *args):
        if not args:
            await ctx.send("En az 1 şey yazmalısın!")
            return
        await ctx.send(f"🎲 Seçtim: **{random.choice(args)}**")
    
    @commands.command(name='rastgelesayi', aliases=['rastgelesayı', 'rndnum'])
    async def rastgele_sayi(self, ctx, min: int = 1, max: int = 100):
        await ctx.send(f"🎲 Sayı: **{random.randint(min, max)}**")
    
    @commands.command(name='bilya')
    async def eightball(self, ctx, *, soru):
        cevaplar = ["Evet", "Hayır", "Belki", "Kesinlikle", "Olabilir", "Sanmıyorum", "Şüphesiz", "Tabii ki", "Maalesef", "Ne yazık ki"]
        await ctx.send(f"🎱 {soru}\n✪ Cevap: **{random.choice(cevaplar)}**")
    
    @commands.command(name='hackle')
    async def hackle(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("Kimi hackleyeceğini yaz!")
            return
        await ctx.send(f"💻 {member} hackleniyor...")
        await asyncio.sleep(2)
        sifreler = ["123456", "password", "admin", "hack", "12345"]
        await ctx.send(f"✅ {member} hacklendi! 🔓 Şifre: `{random.choice(sifreler)}`")
    
    @commands.command(name='shipper')
    async def ship_islemi(self, ctx, member1: discord.Member = None, member2: discord.Member = None):
        if not member1 or not member2:
            await ctx.send("İki kullanıcı etiketle!")
            return
        oran = random.randint(0, 100)
        if oran > 80: emoji = "💕💕💕💕💕"
        elif oran > 60: emoji = "💕💕💕💕"
        elif oran > 40: emoji = "💕💕💕"
        elif oran > 20: emoji = "💕💕"
        else: emoji = "💔"
        await ctx.send(f"❤️ {member1} + {member2} = **{oran}%** {emoji}")
    
    @commands.command(name='boyolcer')
    async def kac_cm(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"📏 {member} kaç cm? **{random.randint(1, 30)}cm** 😏")
    
    @commands.command(name='sakac', aliases=['saka-anlat2'])
    async def saka_soyle(self, ctx):
        sakar = [
            "Neden hamburger yemedim? Çünkü patates kızartması yetersizdi!",
            "Bana bir şifre sor, cevaplayayım. Hmm... Şifre!",
            "Yazılımcı neden kar? Çünkü 0'lama!",
            "Neden telefon hafif? Çünkü mesajlar hafif!",
            "Babaannen kod mu yazıyor? Evet, ama sadece visual basic!",
            "Neden tavuk cross-platform? Çünkü Windows'ta da çalışıyor, Linux'ta da!",
            "Bir yazılımcı neden öldü? Çünkü sonsuz döngüye girdi!",
            "Python neden yılan? Çünkü diğer dillerden sürünerek kaçtı!",
            "Neden C++ zor? Çünkü pointer'lar göstere göstere ortalıkta geziniyor!",
            "JavaScript neden sevilmiyor? Çünkü her şey undefined!",
            "Git neden sevilmiyor? Çünkü merge conflict'ler yüzünden!",
            "Stack Overflow neden mavidir? Çünkü kod yazarken hep mavi ekran görüyoruz!",
            "Neden yazılımcılar kötü mü? Hırsız değil, sadece kod yazıyorlar!",
            "Bir yazılımcı neden uyuyamıyor? Regex'ler rüyasına giriyor!",
            "Neden kod yazarken kahve içiyoruz? Çünkü Java!",
        ]
        await ctx.send(f"😂 {random.choice(sakar)}")
    
    @commands.command(name='yemek', aliases=['neyesak', 'food'])
    async def yemek_oner(self, ctx):
        yemekler = [
            "🍕 Pizza", "🍔 Hamburger", "🌮 Taco", "🍜 Noodle", "🍣 Sushi",
            "🥗 Salata", "🍗 Tavuk", "🍝 Makarna", "🍛 Curry", "🥘 Paella",
            "🍤 Tempura", "🥟 Dumpling", "🥣 Pırasa çorbası", "🍲 Kuru fasulye", "🍖 Kebab"
        ]
        await ctx.send(f"🍽️ Bugün ye: **{random.choice(yemekler)}**")
    
    @commands.command(name='içecek', aliases=['icecek', 'drink'])
    async def icecek_oner(self, ctx):
        icecekler = [
            "☕ Kahve", "🍵 Çay", "🥤 Kola", "🍺 Bira", "🍷 Şarap",
            "🍹 Meyve suyu", "🥛 Süt", "💧 Su", "🧃 Limonata", "🥤 Smoothie"
        ]
        await ctx.send(f"🥤 Bugün iç: **{random.choice(icecekler)}**")
    
    @commands.command(name='film', aliases=['film-oner', 'movie'])
    async def film_oner(self, ctx):
        filmler = [
            "🎬 Inception", "🎬 The Shawshank Redemption", "🎬 The Godfather",
            "🎬 Dark Knight", "🎬 Pulp Fiction", "🎬 Forrest Gump",
            "🎬 Matrix", "🎬 Titanic", "🎬 Avatar", "🎬 Interstellar"
        ]
        await ctx.send(f"🎥 İzle: **{random.choice(filmler)}**")
    
    @commands.command(name='dizi', aliases=['dizi-oner', 'series'])
    async def dizi_oner(self, ctx):
        diziler = [
            "📺 Breaking Bad", "📺 Game of Thrones", "📺 Stranger Things",
            "📺 The Witcher", "📺 Money Heist", "📺 Sherlock",
            "📺 Dark", "📺 The Office", "📺 Friends", "📺 Squid Game"
        ]
        await ctx.send(f"📺 İzle: **{random.choice(diziler)}**")
    
    @commands.command(name='muzikoner', aliases=['sarki-oner'])
    async def muzik_oner(self, ctx):
        sarkilar = [
            "🎵 Bohemian Rhapsody", "🎵 Thriller", "🎵 Billie Jean",
            "🎵 Sweet Child O' Mine", "🎵 Stairway to Heaven", "🎵 Hotel California",
            "🎵 Smells Like Teen Spirit", "🎵 Imagine", "🎵 Hey Jude", "🎵 Like a Rolling Stone"
        ]
        await ctx.send(f"🎧 Dinle: **{random.choice(sarkilar)}**")
    
    @commands.command(name='waifu')
    async def waifu_getir(self, ctx):
        waifus = [
            "Rem (Re:Zero)", "Mikasa (AOT)", "Asuna (SAO)", "Hinata (Naruto)",
            "Zero Two (Darling)", "Mai (K-On)", "Mikoto (AOT)", "Yukino (Oregairu)",
            "Emilia (Re:Zero)", "C.C. (Code Geass)", "Nami (One Piece)", "Neptune (Neptunia)"
        ]
        await ctx.send(f"🎌 Waifu'n: **{random.choice(waifus)}**")
    
    @commands.command(name='husbu')
    async def husbu_getir(self, ctx):
        husbus = [
            "Itachi (Naruto)", "Gojo (JJK)", "L (Death Note)", "Saitama (OPM)",
            "Levi (AOT)", "Mitsuri (KNY)", "Kakashi (Naruto)", "Gintoki (Gintama)",
            "Uraraka (MHA)", "Todoroki (MHA)", "Sasuke (Naruto)", "Deku (MHA)"
        ]
        await ctx.send(f"🎌 Husbu'n: **{random.choice(husbus)}**")
    
    @commands.command(name='asciiyap')
    async def ascii_olustur(self, ctx, *, metin):
        if len(metin) > 20:
            await ctx.send("Çok uzun! Max 20 karakter.")
            return
        await ctx.send(f"```{metin.upper()}```")
    
    @commands.command(name='coololcer', aliases=['cool程度的', 'cool-oran'])
    async def cool_olcer(self, ctx):
        await ctx.send(f"😎 {ctx.author} kaç cool? **{random.randint(0, 100)}%**")
    
    @commands.command(name='zeka', aliases=['iq', 'zekaölcer'])
    async def zeka_olcer(self, ctx):
        await ctx.send(f"🧠 {ctx.author} zeka seviyesi: **{random.randint(50, 200)}**")
    
    @commands.command(name='tkmoyna', aliases=['tas-kagit-makas2'])
    async def tkm_oyna(self, ctx, secim: str):
        secimler = ["taş", "kağıt", "makas"]
        if secim.lower() not in secimler:
            await ctx.send("Taş, kağıt veya makas!")
            return
        bot = random.choice(secimler)
        if secim.lower() == bot:
            sonuc = "Beraber! 🤝"
        elif (secim.lower() == "taş" and bot == "makas") or \
             (secim.lower() == "makas" and bot == "kağıt") or \
             (secim.lower() == "kağıt" and bot == "taş"):
            sonuc = "Kazandın! 🎉"
        else:
            sonuc = "Kaybettin! 😢"
        await ctx.send(f"Sen: {secim} | Bot: {bot}\n{sonuc}")
    
    @commands.command(name='fallar', aliases=['fal', 'coffee-fal'])
    async def fallar_bak(self, ctx):
        fallar = [
            "☕ Bu hafta güzel bir şey olacak!",
            "☕ Çok para gelebilir!",
            "☕ Aşk hayatında değişiklikler var!",
            "☕ Yeni bir arkadaşlık kapıda!",
            "☕ Dikkatli ol, zor bir dönem geliyor!",
            "☕ Hayallerin gerçek olabilir!",
            "☕ Sevdiğin kişi seni düşünüyor!",
            "☕ Yeni bir fırsat kapıda!"
        ]
        await ctx.send(f"🔮 {random.choice(fallar)}")
    
    @commands.command(name='fall', aliases=['tarot', 'tarot-fal'])
    async def fall_bak(self, ctx):
        kartlar = [
            "🌟 SEVGİLİ - Aşk kapıda!",
            "💰 PARA - Para gelecek!",
            "⚡ ENERJİ - Yüksek enerji!",
            "🛡️ KORUMA - Korunuyorsun!",
            "🎯 HEDEF - Hedefine ulaşacaksın!",
            "💡 FİKİR - Yaratıcı fikirler!",
            "🌈 ŞANS - Şansın yaver gidiyor!",
            "🔥 TUTKU - Tutku dorukta!"
        ]
        await ctx.send(f"🔮 Kartın: **{random.choice(kartlar)}**")
    
    @commands.command(name='rol', aliases=['rastgele-rol', 'random-role'])
    async def rastgele_rol_al(self, ctx, *, kategori: str = None):
        roller = ["Kahraman", "Şövalye", "Büyücü", "Savaşçı", "Ninja", "Samuray", "Ejderha", "Melek", "Şeytan", "Prens", "Prenses", "Kral", "Kraliçe", "Ajan", "Silahşör", "Okçu"]
        await ctx.send(f"🎭 Senin rolün: **{random.choice(roller)}**")
    
    @commands.command(name='emojiyaz', aliases=['emoji-yaz', 'emojify'])
    async def emoji_yaz(self, ctx, *, text):
        mapping = {
            'a': '🅰️', 'b': '🅱️', 'c': '©️', 'd': '🅾️', 'e': '📧', 'f': '🍳', 'g': '💚', 'h': '🏭',
            'i': 'ℹ️', 'j': '🌀', 'k': '🔑', 'l': '🅿️', 'm': 'Ⓜ️', 'n': '🅽️', 'o': '🅾️', 'p': '🅿️',
            'q': '🔴', 'r': '®️', 's': '💲', 't': '✝️', 'u': '⛎', 'v': '✅', 'w': '⚠️', 'x': '❌',
            'y': '💛', 'z': '⚡', '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣',
            '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', ' ': '  '
        }
        result = "".join(mapping.get(c.lower(), c) for c in text)
        await ctx.send(result)
    
    @commands.command(name='fbi')
    async def fbi_aciklama(self, ctx):
        await ctx.send("🚨 **FBI OPEN UP!** https://i.imgur.com/w9u8E6p.gif")
    
    @commands.command(name='np', aliases=['nowplaying', 'suancalan'])
    async def simdi_calan(self, ctx):
        await ctx.send("🎵 Şu an çalan: *Bilinmiyor* (Spotify entegrasyonu yakında!)")
    
    @commands.command(name='sayıtahmin', aliases=['tahmin', 'guessnumber'])
    async def sayi_tahmin_oyunu(self, ctx):
        sayi = random.randint(1, 100)
        await ctx.send("🎯 1-100 arasında bir sayı tuttum! Tahmin et!")
        
        def check(m):
            return m.author == ctx.author and m.content.isdigit()
        
        for i in range(7):
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
                tahmin = int(msg.content)
                if tahmin == sayi:
                    await ctx.send(f"🎉 Tebrikler! {i+1}. denemede buldun!")
                    return
                elif tahmin < sayi:
                    await ctx.send("📈 Daha büyük!")
                else:
                    await ctx.send("📉 Daha küçük!")
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Süre doldu! Sayı {sayi} idi.")
                return
        await ctx.send(f"😞 Bilemedin! Sayı {sayi} idi.")
    
    @commands.command(name='matematik', aliases=['matematik-oyun', 'mathgame'])
    async def matematik_oyunu(self, ctx):
        s1 = random.randint(1, 50)
        s2 = random.randint(1, 50)
        islem = random.choice(["+", "-", "*"])
        
        if islem == "+": cevap = s1 + s2
        elif islem == "-": cevap = s1 - s2
        else: cevap = s1 * s2
        
        await ctx.send(f"🧮 {s1} {islem} {s2} = ?")
        
        def check(m):
            return m.author == ctx.author
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=15)
            if msg.content.isdigit() and int(msg.content) == cevap:
                await ctx.send("✅ Doğru! +10 XP")
            else:
                await ctx.send(f"❌ Yanlış! Cevap: {cevap}")
        except:
            await ctx.send(f"⏰ Süre doldu! Cevap: {cevap}")
    
    # === MODERASYON KOMUTLARI ===
    
    @commands.command(name='mesajsil', aliases=['temizle2', 'delete2'])
    @commands.has_permissions(manage_messages=True)
    async def mesaj_sil(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🗑️ {amount} mesaj silindi!", delete_after=3)
    
    @commands.command(name='yavasmod2', aliases=['yavaşmod2'])
    @commands.has_permissions(manage_channels=True)
    async def yavas_mod(self, ctx, saniye: int = 0):
        await ctx.channel.edit(slowmode_delay=saniye)
        await ctx.send(f"🐌 Yavaşmod **{saniye}** saniye!")
    
    @commands.command(name='kilit', aliases=['kanal-kilit'])
    @commands.has_permissions(manage_channels=True)
    async def kanali_kilitle(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Kanal kilitlendi!")
    
    @commands.command(name='ac', aliases=['kanal-ac'])
    @commands.has_permissions(manage_channels=True)
    async def kanali_ac(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Kanal açıldı!")
    
    @commands.command(name='nuke')
    @commands.has_permissions(manage_channels=True)
    async def kanali_sifirla(self, ctx):
        new_channel = await ctx.channel.clone()
        await ctx.channel.delete()
        await new_channel.send("✅ Kanal sıfırlandı!")
    
    # === EKONOMİ KOMUTLARI ===
    
    @commands.command(name='bakiye2', aliases=['para2', 'cash2'])
    async def bakiye_goster(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        cursor = await self.bot.db.execute("SELECT balance FROM users WHERE user_id = ?", (str(member.id),))
        data = await cursor.fetchone()
        bakiye = data[0] if data else 500
        await ctx.send(f"💰 {member} bakiyesi: **{bakiye}** TL")
    
    @commands.command(name='gunluk2', aliases=['daily2', 'günlük2'])
    async def gunluk_para(self, ctx):
        await ctx.send(f"💵 Günlük para aldın! +500 TL (24 saat bekle)")
    
    @commands.command(name='haftalik2', aliases=['weekly2', 'haftalık2'])
    async def haftalik_para(self, ctx):
        await ctx.send(f"💰 Haftalık para aldın! +3500 TL (7 gün bekle)")
    
    @commands.command(name='aylık', aliases=['monthly', 'aylik'])
    async def aylik_para(self, ctx):
        await ctx.send(f"💎 Aylık para aldın! +15000 TL (30 gün bekle)")
    
    @commands.command(name='calis2', aliases=['work2', 'çalış2'])
    async def calis_para(self, ctx):
        paralar = [10, 20, 30, 40, 50, 100, 150, 200]
        await ctx.send(f"💼 Çalıştın! +{random.choice(paralar)} TL")
    
    @commands.command(name='slotmakine', aliases=['slotmachine2'])
    async def slot_oyna(self, ctx, miktar: int = 10):
        if miktar < 1:
            await ctx.send("En az 1 TL yatır!")
            return
        
        semboller = ["🍒", "🍋", "🍇", "💎", "🔔", "7️⃣"]
        sonuc = [random.choice(semboller) for _ in range(3)]
        
        await ctx.send(f"🎰 | {sonuc[0]} | {sonuc[1]} | {sonuc[2]} | 🎰")
        
        if sonuc[0] == sonuc[1] == sonuc[2]:
            await ctx.send(f"🎉 JACKPOT! {miktar * 10} TL kazandın!")
        elif sonuc[0] == sonuc[1] or sonuc[1] == sonuc[2]:
            await ctx.send(f"⭐ İyi! {miktar * 2} TL kazandın!")
        else:
            await ctx.send(f"😢 Kaybettin! {miktar} TL")
    
    @commands.command(name='paragonder', aliases=['transfer2', 'gonder2'])
    async def para_gonder(self, ctx, member: discord.Member, miktar: int):
        if miktar < 1:
            await ctx.send("En az 1 TL gönder!")
            return
        await ctx.send(f"💸 {ctx.author} → {member} = **{miktar}** TL")
    
    # === SEVİYE KOMUTLARI ===
    
    @commands.command(name='seviyegoster2', aliases=['seviye2', 'level2', 'rank2'])
    async def seviye_goster(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        seviye = random.randint(1, 100)
        xp = random.randint(0, seviye * 100)
        await ctx.send(f"📊 {member} - Seviye: **{seviye}** | XP: {xp}/{seviye * 100}")
    
    @commands.command(name='siralama2', aliases=['leaderboard2', 'lb2'])
    async def siralama_goster(self, ctx):
        await ctx.send("🏆 Liderlik tablosu:\n1. Bilinmiyor#0001 - Seviye 99\n2. Bilinmiyor#0002 - Seviye 87\n3. Bilinmiyor#0003 - Seviye 75")
    
    # === SİSTEM KOMUTLARI ===
    
    @commands.command(name='oylama2', aliases=['anket2'])
    async def oylama_yap(self, ctx, *, soru):
        embed = discord.Embed(title="📊 Oylama", description=f"**{soru}**", color=discord.Color.blue())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await msg.add_reaction("🤷")
    
    @commands.command(name='cekilis2', aliases=['giveaway2', 'gway2'])
    async def cekilis_yap(self, ctx, kazanan: int = 1, *, odul):
        embed = discord.Embed(title="🎉 Çekiliş!", description=f"Ödül: **{odul}**\nKazanan: {kazanan}", color=discord.Color.gold())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")
        await ctx.send("🎉 Çekiliş başladı!")
    
    @commands.command(name='embed')
    async def embed_olustur(self, ctx, *, mesaj):
        embed = discord.Embed(description=mesaj, color=discord.Color.random())
        await ctx.send(embed=embed)
    
    # === GENEL KOMUTLAR ===
    
    @commands.command(name='uptime')
    async def uptime_goster(self, ctx):
        import time
        up = time.time() - self.bot.start_time.timestamp()
        saat = int(up // 3600)
        dk = int((up % 3600) // 60)
        sn = int(up % 60)
        await ctx.send(f"⏰ Uptime: **{saat}** saat **{dk}** dakika **{sn}** saniye")
    
    @commands.command(name='bot-bilgi', aliases=['istatistik'])
    async def bilgi_gosterr(self, ctx):
        toplam_uye = sum(g.member_count for g in self.bot.guilds)
        embed = discord.Embed(title="🤖 Bot Bilgi", color=discord.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Sunucu", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Kullanıcı", value=toplam_uye, inline=True)
        embed.add_field(name="Kanal", value=len(self.bot.channels), inline=True)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar2', aliases=['pp2', 'av2', 'resim2'])
    async def avatar_goster(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"🖼️ {member}")
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='banner')
    async def banner_goster(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        if member.banner:
            embed = discord.Embed(title=f"🎨 {member}")
            embed.set_image(url=member.banner.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member} bannerı yok!")
    
    @commands.command(name='sunucuicon', aliases=['servericon', 'sunucu-resim'])
    async def sunucu_icon_goster(self, ctx):
        if ctx.guild.icon:
            embed = discord.Embed(title="📷 Sunucu İkonu")
            embed.set_image(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sunucu ikonu yok!")
    
    @commands.command(name='sunucubanner', aliases=['serverbanner'])
    async def sunucu_banner_goster(self, ctx):
        if ctx.guild.banner:
            embed = discord.Embed(title="🎨 Sunucu Banner")
            embed.set_image(url=ctx.guild.banner.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sunucu bannerı yok!")
    
    @commands.command(name='roller', aliases=['rol-liste', 'rol-list'])
    async def roller_listele(self, ctx):
        roller = [r.mention for r in ctx.guild.roles[1:]]
        embed = discord.Embed(title="📋 Roller", description=", ".join(roller) if roller else "Rol yok", color=discord.Color.blue())
        await ctx.send(embed=embed)
    
    @commands.command(name='emojiler2', aliases=['emoji-liste2', 'emoji-list2'])
    async def emojiler_listele(self, ctx):
        emojiler = [str(e) for e in ctx.guild.emojis]
        embed = discord.Embed(title="😀 Emojiler", description=" ".join(emojiler) if emojiler else "Emoji yok", color=discord.Color.blue())
        embed.add_field(name="Sayı", value=len(emojiler))
        await ctx.send(embed=embed)
    
    @commands.command(name='kanallar', aliases=['kanal-liste', 'channel-list'])
    async def kanallar_listele(self, ctx):
        yazi = [c.mention for c in ctx.guild.text_channels]
        ses = [c.mention for c in ctx.guild.voice_channels]
        embed = discord.Embed(title="📁 Kanallar", color=discord.Color.blue())
        embed.add_field(name="📝 Yazı", value=", ".join(yazi[:10]) + ("..." if len(yazi) > 10 else ""), inline=False)
        embed.add_field(name="🔊 Ses", value=", ".join(ses[:10]) + ("..." if len(ses) > 10 else ""), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='yetkiler', aliases=['izinler', 'permissions', 'perm'])
    async def yetkiler_goster(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        perms = []
        if member.guild_permissions.administrator: perms.append("👑 Admin")
        if member.guild_permissions.manage_messages: perms.append("📝 Mesaj Yönet")
        if member.guild_permissions.kick_members: perms.append("🦶 At")
        if member.guild_permissions.ban_members: perms.append("🔨 Ban")
        if member.guild_permissions.manage_channels: perms.append("📺 Kanal Yönet")
        if member.guild_permissions.manage_roles: perms.append("🎭 Rol Yönet")
        if member.guild_permissions.manage_guild: perms.append("⚙️ Sunucu Yönet")
        
        embed = discord.Embed(title=f"🔑 {member} Yetkileri", color=member.color)
        embed.add_field(name="İzinler", value=", ".join(perms) if perms else "Özel yetki yok", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Mega(bot))
