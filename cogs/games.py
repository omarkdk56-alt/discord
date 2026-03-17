import discord
from discord.ext import commands
import random
import asyncio
import aiohttp

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='savaş')
    async def savas(self, ctx, rakip: discord.Member = None):
        if not rakip:
            await ctx.send("Bir rakip etiketle!")
            return
        
        if rakip.id == ctx.author.id:
            await ctx.send("Kendinle savaşamazsın!")
            return
        
        oyuncu_can = 100
        rakip_can = 100
        sira = 0
        
        embed = discord.Embed(
            title="⚔️ SAVAŞ",
            description=f"{ctx.author} vs {rakip}\n\n🩵 {ctx.author}: {oyuncu_can}\n🩶 {rakip}: {rakip_can}",
            color=discord.Color.red()
        )
        msg = await ctx.send(embed=embed)
        
        while oyuncu_can > 0 and rakip_can > 0:
            await asyncio.sleep(1.5)
            
            if sira % 2 == 0:
                hasar = random.randint(15, 35)
                rakip_can -= hasar
                embed.description = f"{ctx.author} vs {rakip}\n\n🩵 {ctx.author}: {max(0, oyuncu_can)}\n🩶 {rakip}: {max(0, rakip_can)}\n\n⚔️ {ctx.author} {hasar} hasar vurdu!"
            else:
                hasar = random.randint(15, 35)
                oyuncu_can -= hasar
                embed.description = f"{ctx.author} vs {rakip}\n\n🩵 {ctx.author}: {max(0, oyuncu_can)}\n🩶 {rakip}: {max(0, rakip_can)}\n\n⚔️ {rakip} {hasar} hasar vurdu!"
            
            await msg.edit(embed=embed)
            sira += 1
        
        kazanan = ctx.author if oyuncu_can > rakip_can else rakip
        embed.title = f"🏆 {kazanan} KAZANDI!"
        embed.description = f"{ctx.author} vs {rakip}\n\n🩵 {ctx.author}: {max(0, oyuncu_can)}\n🩶 {rakip}: {max(0, rakip_can)}"
        await msg.edit(embed=embed)
    
    @commands.command(name='bilgiyarismasi')
    async def bilgi_yarismasi(self, ctx):
        sorular = [
            {"soru": "Türkiye'nin başkenti neresidir?", "cevap": "ankara"},
            {"soru": "Dünya'nın en büyük okyanusu hangisidir?", "cevap": "pasifik"},
            {"soru": "İnsan vücudunda kaç kemik vardır?", "cevap": "206"},
            {"soru": "Güneş sistemindeki en büyük gezegen hangisidir?", "cevap": "jüpiter"},
            {"soru": "Türkiye'nin en uzun nehri hangisidir?", "cevap": "fırat"},
        ]
        
        soru = random.choice(sorular)
        
        embed = discord.Embed(
            title="🧠 Bilgi Yarışması",
            description=f"**Soru:** {soru['soru']}\n\nCevap olarak yaz! (30 saniye)",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
            if msg.content.lower() == soru['cevap']:
                await ctx.send("✅ Doğru! +50 XP")
            else:
                await ctx.send(f"❌ Yanlış! Doğru cevap: {soru['cevap']}")
        except asyncio.TimeoutError:
            await ctx.send("⏰ Süre doldu!")
    
    @commands.command(name='adamasmaca')
    async def adamasmaca(self, ctx, kelime: str = None):
        if not kelime:
            await ctx.send("Bir kelime belirt!")
            return
        
        kelime = kelime.upper()
        gizli = ["_"] * len(kelime)
        can = 6
        tahminler = []
        
        embed = discord.Embed(
            title="🎭 Adam Asmaca",
            description=f"Kelime: `{' '.join(gizli)}`\n\nKalan can: {can}\nTahminler: {', '.join(tahminler) if tahminler else 'Yok'}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
        while can > 0 and "_" in gizli:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30)
                harf = msg.content.upper()
                
                if len(harf) != 1:
                    await ctx.send("Tek harf gir!")
                    continue
                
                if harf in tahminler:
                    await ctx.send("Bu harfi zaten söyledin!")
                    continue
                
                tahminler.append(harf)
                
                if harf in kelime:
                    for i, h in enumerate(kelime):
                        if h == harf:
                            gizli[i] = harf
                else:
                    can -= 1
                
                embed.description = f"Kelime: `{' '.join(gizli)}`\n\nKalan can: {can}\nTahminler: {', '.join(tahminler)}"
                await ctx.send(embed=embed)
            
            except asyncio.TimeoutError:
                await ctx.send("⏰ Süre doldu!")
                break
        
        if "_" not in gizli:
            await ctx.send(f"🎉 Kazandın! Kelime: {kelime}")
        else:
            await ctx.send(f"❌ Kaybettin! Kelime: {kelime}")
    
    @commands.command(name='kimlik')
    async def kimlik(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        isimler = ["Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Veli", "Zeynep", "Emre"]
        soyisimler = ["Yılmaz", "Kaya", "Demir", "Çelik", "Arslan", "Koç", "Erdoğan"]
        sehirler = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana"]
        meslekler = ["Mühendis", "Doktor", "Öğretmen", "Avukat", "Sanatçı", "Pilot"]
        
        kimlik = {
            "Ad": random.choice(isimler),
            "Soyad": random.choice(soyisimler),
            "Yaş": random.randint(18, 65),
            "Meslek": random.choice(meslekler),
            "Şehir": random.choice(sehirler),
            "Burç": random.choice(["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]),
            "Cinsiyet": random.choice(["Erkek", "Kadın"]),
        }
        
        embed = discord.Embed(
            title=f"🪪 {member} Kimliği",
            color=discord.Color.blue()
        )
        
        for key, value in kimlik.items():
            embed.add_field(name=key, value=value, inline=True)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='sansoyunu')
    async def sansoyunu(self, ctx):
        sayi = random.randint(1, 100)
        
        embed = discord.Embed(
            title="🎰 Sayı Tahmin Oyunu",
            description="1-100 arasında bir sayı tuttum!\n\nTahmin et!",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)
        
        for deneme in range(7):
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=15)
                tahmin = int(msg.content)
                
                if tahmin == sayi:
                    await ctx.send(f"🎉 Tebrikler! {deneme + 1}. denemede buldun!")
                    return
                elif tahmin < sayi:
                    await ctx.send(f"📈 Daha büyük bir sayı dene!")
                else:
                    await ctx.send(f"📉 Daha küçük bir sayı dene!")
            
            except asyncio.TimeoutError:
                await ctx.send(f"⏰ Süre doldu! Sayı: {sayi}")
                return
            except:
                await ctx.send("Geçerli bir sayı gir!")
        
        await ctx.send(f"❌ Hakların bitti! Sayı: {sayi}")
    
    @commands.command(name='emojiyap')
    async def emojiyap(self, ctx, emoji: str = None):
        if not emoji:
            await ctx.send("Bir emoji belirt!")
            return
        
        buyuk = ["😀","😂","😍","😎","🤔","😴","😭","😤","🥳","😱","🤯","🥵","🥶","🤡","👻","💀","👽","🤖","🎃","😺","🐶","🦊","🐻","🦁","🐸","🐔","🦄","🐝","🦋","🌸","🌺","🌻","🌹","🍕","🍔","🍟","🌭","🍿","🍩","🍪","☕","🍺","🍷","⚽","🏀","🎾","🎮","🎲","🎵","🎶","🎤","🎧","🎯","🎰","🎱","🏆","🥇","⭐","🌟","✨","💫","🔥","💥","💯","❤️","💔","💕","💖","💗","💙","💚","💛","🧡","💜","🖤","🤍","🤎","💪","👋","👍","👎","🙏","✌️","🤞","🫶","🤝","💅","💍","💎","👑","👒","🎩","🧢","🕶️","🎓","🎒","📱","💻","⌨️","🖱️","💾","💿","📷","📹","🎥","📺","📻","⏰","📅","🌐","🗺️","🚗","✈️","🚀","🛸","🏠","🏰","⛺","🌉","🏝️"]
        
        await ctx.send(random.choice(buyuk))
    
    @commands.command(name='kup')
    async def kup(self, ctx, renk: str = None):
        renkler = {"kırmızı": "🔴", "mavi": "🔵", "yeşil": "🟢", "sarı": "🟡", "turuncu": "🟠", "mor": "🟣", "siyah": "⚫", "beyaz": "⚪"}
        
        if not renk:
            await ctx.send(f"Renkler: {', '.join(renkler.keys())}")
            return
        
        if renk in renkler:
            await ctx.send(renkler[renk])
        else:
            await ctx.send("Bu renk desteklenmiyor!")

async def setup(bot):
    await bot.add_cog(Games(bot))
