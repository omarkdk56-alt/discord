import discord
from discord.ext import commands
import random
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='8ball')
    async def eightball(self, ctx, *, soru=None):
        if not soru:
            await ctx.send("Bir soru sor!")
            return
        
        cevaplar = [
            "Kesinlikle evet!", "Evet!", "Olabilir...", 
            "Bilmiyorum", "Hayir", "Kesinlikle hayir!",
            "Tekrar sor!", "Tabii ki!", "Maalesef"
        ]
        
        embed = discord.Embed(
            title="🎱 8ball",
            description=f"Soru: {soru}\n\nCevap: **{random.choice(cevaplar)}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='yazitura')
    async def yazitura(self, ctx):
        sonuc = random.choice(["Tura", "Yazi"])
        embed = discord.Embed(
            title="🪙 Yazı Tura",
            description=f"**{sonuc}** geldi!",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='zar')
    async def zar(self, ctx, adet: int = 1):
        if adet < 1:
            adet = 1
        if adet > 10:
            adet = 10
        
        sonuclar = [random.randint(1, 6) for _ in range(adet)]
        toplam = sum(sonuclar)
        
        emojiler = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
        zar_emojiler = ' '.join([emojiler[s-1] for s in sonuclar])
        
        embed = discord.Embed(
            title="🎲 Zar",
            description=f"Sonuclar: {zar_emojiler}\nToplam: **{toplam}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='kaçcm', aliases=['kaccm', 'cm', 'kaç'])
    async def kac_cm(self, ctx, member: discord.Member = None):
        if not member:
            # Random cm
            cm = random.randint(1, 20)
            embed = discord.Embed(
                title="📏 Kaç CM?",
                description=f" Senin pipin **{cm} cm**!",
                color=discord.Color.random()
            )
            embed.set_image(url="https://media.discordapp.net/attachments/123456789/987654321/kac.gif")
            await ctx.send(embed=embed)
            return
        
        if member.id == ctx.author.id:
            await ctx.send("Kendi pipini ölçmek için aynaya bak!")
            return
        
        cm = random.randint(1, 25)
        
        embed = discord.Embed(
            title="📏 Kaç CM?",
            description=f"**{member.name}**'in pipi **{cm} cm**!",
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='+18', aliases=['yasin', 'adult'])
    async def adult(self, ctx):
        isimler = ["Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia", "Harper", "Evelyn",
                   "Abigail", "Emily", "Elizabeth", "Sofia", "Avery", "Ella", "Scarlett", "Grace", "Chloe", "Victoria",
                   "Riley", "Aria", "Lily", "Aurora", "Zoey", "Penelope", "Layla", "Brooklyn", "Alexa", "Zoe",
                   "Nora", "Camila", "Hannah", "Lillian", "Addison", "Aubrey", "Ellie", "Stella", "Natalie", "Katherine",
                   "Lucy", "Paisley", "Bella", "Claire", "Skylar", "Parker", "Valeria", "Madison", "Luna", "Kylie",
                   "Alexandra", "Hazel", "Violet", "Aurora", "Savannah", "Audrey", "Brooklyn", "Bella", "Claire", "Lexi",
                   "Jenna", "Lisa", "Mia", "Riley", "Asa", "Stoya", "Sasha", "Traci", "Nikki", "Angela",
                   "Lana", "Alexis", "Kendra", "Johnny", "Manuel", "Mick", "John", "James", "Mike", "Chris",
                   "David", "Daniel", "Matt", "Tony", "Steve", "Mark", "Paul", "Kevin", "Brian", "Jason"]
        
        soyisimler = ["Jameson", "Ann", "Khalifa", "Reid", "Rhoades", "Akira", "Stoya", "Grey", "Lords", "Benz",
                      "Texas", "Sunderland", "White", "Fox", "Sins", "Ferrari", "Rossi", "Moretti", "Romano", "Costa",
                      "Esposito", "Ricci", "Marino", "Greco", "Bruno", "Conti", "Costa", "Giordano", "Mancini", "Rizzo",
                      "Lombardi", "Mozart", "Bach", "Beethoven", "Wagner", "Verdi", "Puccini", "Vivaldi", "Chopin", "Liszt",
                      "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                      "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                      "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                      "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                      "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
                      "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
                      "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
                      "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
                      "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
                      "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
                      "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson",
                      "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Patterson", "Jordan", "Reynolds", "Hamilton",
                      "Graham", "George", "Stone", "Morrison", "Kennedy", "Warren", "Dixon", "Hunt", "Palmer", "Burke",
                      "Carr", "Fisher", "Hamilton", "Graham", "Richards", "Stevens", "Murray", "Ford", "Marshall", "Owens",
                      "Mcdonald", "Harrison", "Ruiz", "Kennedy", "Wells", "Alvarez", "Woods", "Mendoza", "Castillo", "Olson",
                      "Freeman", "Wells", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter",
                      "Hunter", "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks",
                      "Holmes", "Warner", "Carpenter", "Lawrence", "Sanders", "Cruz", "Stephens", "Gardner", "Payne", "Grant",
                      "Dunn", "Kelley", "Spencer", "Hawkins", "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos",
                      "Hart", "Bradley", "Knight", "Elliott", "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll", "Lane"]
        
        ulkeler = ["ABD", "Japonya", "Brezilya", "Almanya", "Fransa", "İngiltere", "İtalya", "İspanya", "Rusya", "Kanada",
                   "Avustralya", "Meksika", "Arjantin", "Hollanda", "Belçika", "İsveç", "Norveç", "Danimarka", "Finlandiya", "Polonya",
                   "Ukrayna", "Romanya", "Macaristan", "Avusturya", "İsviçre", "Yunanistan", "Portekiz", "Çekya", "Güney Kore", "Hindistan",
                   "Kolombiya", "Şili", "Peru", "Venezuela", "Filipinler", "Endonezya", "Tayland", "Vietnam", "Malezya", "Singapur"]
        
        yaslar = list(range(18, 55))
        
        isim = f"{random.choice(isimler)} {random.choice(soyisimler)}"
        
        embed = discord.Embed(
            title="🔞 +18 - Yetişkin Film Yıldızı",
            description=f"**🎭 {isim}**\n\n"
                        f"📅 Yaş: {random.choice(yaslar)}\n"
                        f"📍 Ülke: {random.choice(ulkeler)}\n"
                        f"🎬 Film sayısı: {random.randint(50, 500)}\n"
                        f"⭐ Rating: {random.randint(80, 100)}%",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text="Bu komut sadece eğlence amaçlıdır! 😄")
        await ctx.send(embed=embed)
    
    @commands.command(name='hack')
    async def hack(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("Bir kullanici etiketle!")
            return
        
        if member.id == ctx.author.id:
            await ctx.send("Kendini hackleyemezsin!")
            return
        
        msg = await ctx.send(f"Hackleniyor...")
        
        for _ in range(5):
            await asyncio.sleep(0.8)
            await msg.edit(content=f"Hackleniyor... {random.choice(['IP bulunuyor', 'Sifre kırılıyor', 'Email bulunuyor', 'Veri indiriliyor'])}")
        
        emailler = ["hack@darkweb.com", "anonim@tormail.net"]
        sifreler = ["password123", "admin123", "qwerty"]
        
        embed = discord.Embed(
            title="✅ Hack Tamamlandi!",
            description=f"**{member}** hacklendi! (Saka)",
            color=discord.Color.green()
        )
        embed.add_field(name="Email", value=f"||{random.choice(emailler)}||", inline=True)
        embed.add_field(name="Sifre", value=f"||{random.choice(sifreler)}||", inline=True)
        await msg.edit(content=None, embed=embed)
    
    @commands.command(name='ship')
    async def ship(self, ctx, member1: discord.Member = None, member2: discord.Member = None):
        if not member1:
            await ctx.send("Bir kullanici etiketle!")
            return
        
        if not member2:
            member2 = random.choice([m for m in ctx.guild.members if not m.bot and m != member1])
        
        if member1.id == member2.id:
            await ctx.send("Kendinle evlenemezsin!")
            return
        
        yuzde = random.randint(0, 100)
        
        if yuzde > 80:
            durum = "Ask 💕"
        elif yuzde > 60:
            durum = "Sevgi 🥰"
        elif yuzde > 40:
            durum = "Arkadaşlık 😊"
        else:
            durum = "Dostluk 💔"
        
        kalpler = "❤️" * (yuzde // 20 + 1)
        
        embed = discord.Embed(
            title="💕 Asik Hesaplayici",
            description=f"{member1} ❤️ {member2}",
            color=discord.Color.pink()
        )
        embed.add_field(name="Yuzde", value=f"**{yuzde}%** {kalpler}", inline=False)
        embed.add_field(name="Durum", value=durum, inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='sans')
    async def sans(self, ctx):
        yuzde = random.randint(0, 100)
        
        if yuzde > 80:
            durum = "Cok Sanslisin!"
        elif yuzde > 50:
            durum = "Sanslisin"
        else:
            durum = "Sanssiz"
        
        embed = discord.Embed(
            title="🍀 Sans Olcer",
            description=f"**{yuzde}%** - {durum}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='saka')
    async def saka(self, ctx):
        sakalar = [
            "Neden programci deniz kiyisina gitti? - HTML'de 'sea' yok!",
            "Python neyi sever? - while True: eat()",
            "Bir programci neden zayifladi? - Ctrl+C ve Ctrl+V yapiyordu!",
            "Git nedir? - Sinir yapma!",
            "JavaScript developerlar para biriktiremiyor - Hep 'undefined' oluyorlar!"
        ]
        
        embed = discord.Embed(
            title="😂 Saka",
            description=random.choice(sakalar),
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='tkm')
    async def tkm(self, ctx, secim: str = None):
        if not secim:
            await ctx.send("Tas, kagit veya makas sec!\nOrnek: h!tkm tas")
            return
        
        secimler = ['tas', 'kagit', 'makas']
        secim = secim.lower()
        
        if secim not in secimler:
            await ctx.send("Tas, kagit veya makas sec!")
            return
        
        bilgisayar = random.choice(secimler)
        
        sonuclar = {
            ('tas', 'makas'): 'kazandin',
            ('makas', 'kagit'): 'kazandin',
            ('kagit', 'tas'): 'kazandin',
            ('tas', 'tas'): 'berabere',
            ('kagit', 'kagit'): 'berabere',
            ('makas', 'makas'): 'berabere'
        }
        
        sonuc = sonuclar.get((secim, bilgisayar), 'kaybettin')
        
        emojiler = {'tas': '🪨', 'kagit': '📄', 'makas': '✂️'}
        
        embed = discord.Embed(
            title="✊✋✌️ Tas Kagit Makas",
            description=f"Sen: {emojiler[secim]} {secim}\nBot: {emojiler[bilgisayar]} {bilgisayar}\n\nSonuc: **{sonuc.upper()}**",
            color=discord.Color.green() if sonuc == 'kazandin' else discord.Color.red() if sonuc == 'kaybettin' else discord.Color.greyple()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='ascii')
    async def ascii(self, ctx, *, yazi=None):
        if not yazi:
            await ctx.send("Bir yazi yaz!")
            return
        
        if len(yazi) > 30:
            yazi = yazi[:30]
        
        ascii_chars = {
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓',
            'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏',
            'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠽',
            'z': '⠼', ' ': ' '
        }
        
        sonuc = ''.join(ascii_chars.get(c.lower(), c) for c in yazi)
        
        embed = discord.Embed(
            title="✡️ ASCII",
            description=f"```\n{sonuc}\n```",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='bilgi2')
    async def bilgi2(self, ctx):
        bilgiler = [
            "Penguenler dizlerinin uzerinde yuruyemez.",
            "Ahtapotların 3 kalbi vardir.",
            "Insan beyni %75 sudur.",
            "Kelebekler tat alma duyusu ayaklarındadır.",
            "Ay'ın diger adi 'Selene' dir."
        ]
        
        embed = discord.Embed(
            title="💡 Bilgi",
            description=random.choice(bilgiler),
            color=discord.Color.teal()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='renk')
    async def renk(self, ctx):
        renkler = [
            ("Kirmizi", discord.Color.red()),
            ("Mavi", discord.Color.blue()),
            ("Yesil", discord.Color.green()),
            ("Sarı", discord.Color.yellow()),
            ("Mor", discord.Color.purple()),
            ("Turuncu", discord.Color.orange())
        ]
        
        adi, renk = random.choice(renkler)
        
        embed = discord.Embed(
            title="🌈 Rastgele Renk",
            description=f"**{adi}**",
            color=renk
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='dilek')
    async def dilek(self, ctx, *, dilek=None):
        if not dilek:
            await ctx.send("Bir dilek tut!")
            return
        
        embed = discord.Embed(
            title="🌟 Dilek Tutuldu!",
            description=f"Dilek: **{dilek}**\n\nGokyuzune gonderildi!",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
    
    # === PROFİL KOMUTLARI ===
    
    @commands.command(name='profil')
    async def profil(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"👤 {member}",
            color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Bot mu?", value="Evet" if member.bot else "Hayır", inline=True)
        embed.add_field(name="Rol Sayısı", value=str(len(member.roles)), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='kullanıcıbilgi', aliases=['kb', 'üye-bilgi', 'userinfo'])
    async def kullanici_bilgi(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"👤 {member}",
            color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Sunucu Adı", value=member.display_name, inline=True)
        embed.add_field(name="Bot mu?", value="Evet" if member.bot else "Hayır", inline=True)
        embed.add_field(name="Hesap Oluşturulma", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Sunucuya Katılma", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Bilinmiyor", inline=True)
        embed.add_field(name="Rol Sayısı", value=str(len(member.roles)), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='sunucubilgi', aliases=['sunucu', 'serverinfo', 'sb'])
    async def sunucubilgi(self, ctx):
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue()
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Üye Sayısı", value=guild.member_count, inline=True)
        embed.add_field(name="Kanal Sayısı", value=len(guild.channels), inline=True)
        embed.add_field(name="Rol Sayısı", value=len(guild.roles), inline=True)
        embed.add_field(name="Emoji Sayısı", value=len(guild.emojis), inline=True)
        embed.add_field(name="Oluşturulma", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Sahip", value=guild.owner.mention if guild.owner else "Bilinmiyor", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='roller', aliases=['rol-liste', 'rol-list'])
    async def roller(self, ctx):
        roller = [r.mention for r in ctx.guild.roles[1:]]
        if not roller:
            await ctx.send("Sunucuda rol yok!")
            return
        
        embed = discord.Embed(title="📋 Roller", color=discord.Color.blue())
        for i in range(0, len(roller), 10):
            chunk = roller[i:i+10]
            embed.add_field(name=f"Roller ({i+1}-{min(i+10, len(roller))})", value=", ".join(chunk), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='emojiler', aliases=['emoji-liste', 'emoji-list'])
    async def emojiler(self, ctx):
        emojiler = [str(e) for e in ctx.guild.emojis]
        if not emojiler:
            await ctx.send("Sunucuda emoji yok!")
            return
        
        embed = discord.Embed(title="😀 Emojiler", color=discord.Color.blue())
        for i in range(0, len(emojiler), 20):
            chunk = emojiler[i:i+20]
            embed.add_field(name=f"Emojiler ({i+1}-{min(i+20, len(emojiler))})", value=" ".join(chunk), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='kanallar', aliases=['kanal-liste', 'channel-list'])
    async def kanallar(self, ctx):
        yazi = [c.mention for c in ctx.guild.text_channels]
        ses = [c.mention for c in ctx.guild.voice_channels]
        
        embed = discord.Embed(title="📁 Kanallar", color=discord.Color.blue())
        if yazi:
            embed.add_field(name="Yazı Kanalları", value=", ".join(yazi[:10]), inline=False)
        if ses:
            embed.add_field(name="Ses Kanalları", value=", ".join(ses[:10]), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='yetkiler', aliases=['izin', 'permissions'])
    async def yetkiler(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        perms = []
        if member.guild_permissions.administrator: perms.append("👑 Administrator")
        if member.guild_permissions.manage_guild: perms.append("🌐 Sunucu Yönet")
        if member.guild_permissions.manage_channels: perms.append("📁 Kanal Yönet")
        if member.guild_permissions.manage_roles: perms.append("🎭 Rol Yönet")
        if member.guild_permissions.manage_messages: perms.append("💬 Mesaj Yönet")
        if member.guild_permissions.kick_members: perms.append("🦶 At")
        if member.guild_permissions.ban_members: perms.append("🚫 Yasakla")
        if member.guild_permissions.mute_members: perms.append("🔇 Sustur")
        if member.guild_permissions.move_members: perms.append("🔀 Taşı")
        
        embed = discord.Embed(title=f"🔐 {member} Yetkileri", color=member.color)
        embed.add_field(name="Yetkiler", value="\n".join(perms) if perms else "Özel yetki yok", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='kanalbilgi')
    async def kanalbilgi(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        
        embed = discord.Embed(title=f"📁 #{channel.name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Tür", value=str(channel.type), inline=True)
        embed.add_field(name="Oluşturulma", value=str(channel.created_at)[:10], inline=True)
        if channel.topic:
            embed.add_field(name="Konu", value=channel.topic, inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("🏓 Pong! `calculating...`")
    
    @commands.command(name='pong2')
    async def pong2(self, ctx):
        await ctx.send("🏓 Ping! `calculating...`")
    
    @commands.command(name='bot', aliases=['botbilgi', 'botinfo'])
    async def bot(self, ctx):
        embed = discord.Embed(title="🤖 Huh Bot", color=discord.Color.blue())
        embed.add_field(name="Sunucu Sayısı", value="100+", inline=True)
        embed.add_field(name="Kullanıcı Sayısı", value="10000+", inline=True)
        embed.add_field(name="Komut Sayısı", value="750+", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='uptime')
    async def uptime(self, ctx):
        await ctx.send("⏰ Bot çalışıyor!")
    
    @commands.command(name='istatistik', aliases=['stats', 'istatistikler'])
    async def istatistik(self, ctx):
        embed = discord.Embed(title="📊 İstatistikler", color=discord.Color.blue())
        embed.add_field(name="Sunucu", value="100+", inline=True)
        embed.add_field(name="Kullanıcı", value="10000+", inline=True)
        embed.add_field(name="Kanal", value="500+", inline=True)
        embed.add_field(name="Komut", value="750+", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='link', aliases=['davet', 'invite'])
    async def link(self, ctx):
        embed = discord.Embed(title="🔗 Davet Linki", color=discord.Color.blue())
        embed.description = "https://discord.com/oauth2/authorize?client_id=1452460095085744238&permissions=8&scope=bot"
        await ctx.send(embed=embed)
    
    @commands.command(name='davet2')
    async def davet2(self, ctx):
        if ctx.guild.me.guild_permissions.create_instructions:
            link = await ctx.channel.create_invite(max_age=0, max_uses=0)
            await ctx.send(f"🔗 Davet linki: {link.url}")
        else:
            await ctx.send("Davet linki oluşturma yetkim yok!")
    
    @commands.command(name='say')
    async def say(self, ctx, *, mesaj):
        await ctx.message.delete()
        await ctx.send(mesaj)
    
    @commands.command(name='yaz')
    async def yaz(self, ctx, *, mesaj):
        await ctx.send(mesaj)
    
    @commands.command(name='embed')
    async def embedyaz(self, ctx, *, mesaj):
        embed = discord.Embed(description=mesaj, color=discord.Color.blue())
        await ctx.send(embed=embed)
    
    # === EĞLENCE SAYFA 2-5 KOMUTLARI ===
    
    @commands.command(name='kapismac')
    async def kapismac(self, ctx):
        takımlar = ["Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor", "Ankaragücü"]
        t1, t2 = random.sample(takımlar, 2)
        s1, s2 = random.randint(0, 5), random.randint(0, 5)
        embed = discord.Embed(title="⚽ Futbol Maçı", color=discord.Color.green())
        embed.add_field(name=t1, value=f"{s1} gol", inline=True)
        embed.add_field(name=t2, value=f"{s2} gol", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='dortbasamak')
    async def dortbasamak(self, ctx):
        sayi = random.randint(1000, 9999)
        embed = discord.Embed(title="🎲 4 Basamaklı Sayı", description=f"**{sayi}**", color=discord.Color.blue())
        await ctx.send(embed=embed)
    
    @commands.command(name='zarat')
    async def zarat(self, ctx):
        z1 = random.randint(1, 6)
        z2 = random.randint(1, 6)
        await ctx.send(f"🎲 Zar: **{z1}** ve **{z2}** (Toplam: {z1+z2})")
    
    @commands.command(name='sec')
    async def sec(self, ctx, *args):
        if not args:
            await ctx.send("Seçenek belirt!")
            return
        await ctx.send(f"🎯 Seçtim: **{random.choice(args)}**")
    
    @commands.command(name='dovus')
    async def dovus(self, ctx):
        oyuncu = random.randint(1, 100)
        dusman = random.randint(1, 100)
        if oyuncu > dusman:
            sonuc = f"🎮 Kazandın! ({oyuncu} vs {dusman})"
        elif dusman > oyuncu:
            sonuc = f"🎮 Kaybettin! ({oyuncu} vs {dusman})"
        else:
            sonuc = f"🎮 Berabere! ({oyuncu} vs {dusman})"
        await ctx.send(sonuc)
    
    @commands.command(name='bilgi')
    async def bilgi(self, ctx):
        bilgiler = [
            "Penguenler dizlerinin üzerinde yürüyemez.",
            "Ahtapotların 3 kalbi vardır.",
            "İnsan beyni %75 sudur.",
            "Kelebekler tat alma duyusu ayaklarındadır.",
            "Ay'ın diğer adı 'Selene'dir.",
            "Arılar dans ederek haberleşir.",
            "Dünya'nın en yüksek dağı Everest'tir.",
            "Su 100°C'de kaynar."
        ]
        await ctx.send(f"💡 **{random.choice(bilgiler)}**")
    
    @commands.command(name='ascii')
    async def ascii(self, ctx, *, yazi):
        if len(yazi) > 20:
            await ctx.send("Çok uzun yazı!")
            return
        await ctx.send(f"```\n{yazi}\n```")
    
    @commands.command(name='emojiyap')
    async def emojiyap(self, ctx, *, yazi):
        emojis = ["😀", "😂", "🤣", "😊", "😍", "🤔", "😎", "🥳", "😇", "🤩"]
        sonuc = " ".join([random.choice(emojis) for _ in yazi])
        await ctx.send(sonuc)
    
    @commands.command(name='kupacevir')
    async def kupacevir(self, ctx):
        await ctx.send(random.choice(["🪙 Yazı", "🪙 Tura"]))
    
    @commands.command(name='savasp')
    async def savasp(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("Kiminle savaşacaksın?")
            return
        p1 = random.randint(1, 100)
        p2 = random.randint(1, 100)
        if p1 > p2:
            sonuc = f"🎮 {ctx.author.mention} kazandı! ({p1} vs {p2})"
        elif p2 > p1:
            sonuc = f"🎮 {member.mention} kazandı! ({p1} vs {p2})"
        else:
            sonuc = f"🎮 Berabere! ({p1} vs {p2})"
        await ctx.send(sonuc)
    
    @commands.command(name='taşkağıt')
    async def taskagit(self, ctx, secim: str = None):
        if not secim:
            await ctx.send("Taş, kağıt veya makas seç!\nÖrnek: h!taskagit taş")
            return
        secim = secim.lower()
        if secim not in ["taş", "kağıt", "makas"]:
            await ctx.send("Taş, kağıt veya makas seç!")
            return
        secenekler = ["taş", "kağıt", "makas"]
        bot_secim = random.choice(secenekler)
        
        kazandi = (secim == "taş" and bot_secim == "makas") or \
                  (secim == "kağıt" and bot_secim == "taş") or \
                  (secim == "makas" and bot_secim == "kağıt")
        
        if secim == bot_secim:
            await ctx.send(f"Berabere! Sen: {secim}, Bot: {bot_secim}")
        elif kazandi:
            await ctx.send(f"🎉 Kazandın! Sen: {secim}, Bot: {bot_secim}")
        else:
            await ctx.send(f"😢 Kaybettin! Sen: {secim}, Bot: {bot_secim}")
    
    @commands.command(name='alkışla')
    async def alkışla(self, ctx):
        await ctx.send("👏" * random.randint(5, 20))
    
    @commands.command(name='emoji')
    async def emoji(self, ctx, sayi: int = 1):
        if sayi > 20:
            sayi = 20
        emojiler = ["😀", "😂", "🤣", "😊", "😍", "🤔", "😎", "🥳", "😇", "🤩", "😋", "😜", "🤪", "😝", "🙃"]
        await ctx.send("".join(random.choices(emojiler, k=sayi)))
    
    @commands.command(name='yazıtura')
    async def yazitura(self, ctx):
        await ctx.send(random.choice(["🪙 Yazı", "🪙 Tura"]))
    
    @commands.command(name='şaka')
    async def saka(self, ctx):
        sakalar = [
            "Bana bir kitap aldın mı? - Hangi kitap? - Sevdiğim biri! 😂",
            "Seni bir kareye sığdırabilir miyim? - Tabii! - O zaman poz ver! 😂",
            "Adın ne? - Sorun. - Sorun ne? - Adım Sorun! 😂",
            "Neden kitap okumuyorsun? - Çünkü kelime dağarcığım yeterince trajik! 😂"
        ]
        await ctx.send(random.choice(sakalar))
    
    @commands.command(name='fıkra')
    async def fıkra(self, ctx):
        fıkralar = [
            "Adam pilav ısmarlamış. Garson sormuş: 'Pirinç mi, bulgur mu?' Adam: 'Buldurmak!' 😂",
            "Temel ile Dursun araba kullanıyormuş. Temel: 'Frene bas!' Dursun: 'Hangi frene?' Temel: 'Bütün frenlere!' 😂",
            "Öğretmen: '2+2 kaç eder?' Öğrenci: '4' Öğretmen: 'Aferin!' Öğrenci: 'Teşekkürler!' 😂"
        ]
        await ctx.send(random.choice(fıkralar))
    
    @commands.command(name='komik')
    async def komik(self, ctx):
        resimler = [
            "https://i.imgflip.com/1g8my4.jpg",
            "https://i.imgflip.com/1h7in3.jpg",
            "https://i.imgflip.com/261o3j.jpg"
        ]
        await ctx.send(random.choice(resimler))
    
    @commands.command(name='gif')
    async def gif(self, ctx):
        gifs = [
            "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
            "https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif",
            "https://media.giphy.com/media/l0MYGb1LuZ3n7dRnO/giphy.gif"
        ]
        await ctx.send(random.choice(gifs))
    
    @commands.command(name='dans')
    async def dans(self, ctx):
        danslar = ["💃", "🕺", "💃🕺", "💃🏻🕺🏻", "💃🏿🕺🏿"]
        await ctx.send(random.choice(danslar) * random.randint(3, 8))
    
    @commands.command(name='alkis')
    async def alkis(self, ctx):
        await ctx.send("👏" * random.randint(10, 50))
    
    @commands.command(name='hayvan')
    async def hayvan(self, ctx):
        hayvanlar = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐙"]
        await ctx.send(random.choice(hayvanlar))
    
    @commands.command(name='yemek')
    async def yemek(self, ctx):
        yemekler = ["🍕", "🍔", "🌮", "🍟", "🍣", "🍜", "🥗", "🍝", "🥘", "🧁", "🍰", "🍦"]
        await ctx.send(random.choice(yemekler))
    
    @commands.command(name='içecek')
    async def icecek(self, ctx):
        icecekler = ["☕", "🍵", "🧃", "🥤", "🍺", "🍷", "🥛", "🧋", "🍹", "🧉"]
        await ctx.send(random.choice(icecekler))
    
    @commands.command(name='meyve')
    async def meyve(self, ctx):
        meyveler = ["🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍒", "🍑", "🥭", "🍍"]
        await ctx.send(random.choice(meyveler))
    
    @commands.command(name='spor')
    async def spor(self, ctx):
        sporlar = ["⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🏉", "🎱", "🏓", "🏸", "🥊", "🥋"]
        await ctx.send(random.choice(sporlar))
    
    @commands.command(name='araba')
    async def araba(self, ctx):
        arabalar = ["🚗", "🚙", "🏎️", "🚓", "🚑", "🚒", "🚌", "🚲", "🛵", "🚕", "🚚", "🚜"]
        await ctx.send(random.choice(arabalar))
    
    @commands.command(name='müzik2')
    async def muzik(self, ctx):
        await ctx.send("🎵 Şarkı çalmak için h!cal <şarkı> kullan!")
    
    @commands.command(name='film')
    async def film(self, ctx):
        filmler = ["The Matrix", "Inception", "Interstellar", "Titanic", "Avatar", "Avengers", "Joker", "Batman"]
        await ctx.send(f"🎬 Önerim: **{random.choice(filmler)}**")
    
    @commands.command(name='dizi')
    async def dizi(self, ctx):
        diziler = ["Breaking Bad", "Game of Thrones", "La Casa de Papel", "Stranger Things", "The Witcher", "Sherlock"]
        await ctx.send(f"📺 Önerim: **{random.choice(diziler)}**")
    
    @commands.command(name='renk2')
    async def renk2(self, ctx):
        await ctx.send("🌈 Rastgele renk için h!renk komutunu dene!")
    
    @commands.command(name='ascii2')
    async def ascii2(self, ctx, *, yazi):
        if len(yazi) > 15:
            await ctx.send("Çok uzun!")
            return
        await ctx.send(f"```\n{yazi.upper()}\n{yazi}\n{yazi.upper()}\n```")

async def setup(bot):
    await bot.add_cog(Fun(bot))
