import discord
from discord.ext import commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='bakiye')
    async def bakiye(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"💰 {member} Bakiyesi",
            color=discord.Color.gold()
        )
        embed.add_field(name="Nakit", value="**500** TL", inline=True)
        embed.add_field(name="Banka", value="**1000** TL", inline=True)
        embed.add_field(name="Toplam", value="**1500** TL", inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='gunluk')
    async def gunluk(self, ctx):
        embed = discord.Embed(
            title="🎁 Günlük Ödül!",
            description="**500** TL kazandın!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='haftalik')
    async def haftalik(self, ctx):
        embed = discord.Embed(
            title="🎁 Haftalık Ödül!",
            description="**3500** TL kazandın!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='calis')
    async def calis(self, ctx):
        isler = ["Tamirci", "Kurye", "Garson", "Yazılımcı", "Öğretmen", "Doktor", "Avukat"]
        is_ad = random.choice(isler)
        kazanc = random.randint(50, 200)
        embed = discord.Embed(
            title="💼 Çalıştın!",
            description=f"**{is_ad}** olarak çalıştın ve **{kazanc}** TL kazandın!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='soyledin')
    async def soyledin(self, ctx):
        sozler = [
            "Bugün hava çok güzel!",
            "Bu bot harika!",
            "Selam herkese!",
            "Nasılsınız?",
            "İyi günler!"
        ]
        soz = random.choice(sozler)
        kazanc = random.randint(10, 50)
        embed = discord.Embed(
            title="🎤 Şarkı Söyledin!",
            description=f'"{soz}" dedin ve **{kazanc}** TL kazandın!',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='paraver')
    async def paraver(self, ctx, member: discord.Member = None, miktar: int = 0):
        if not member or miktar <= 0:
            await ctx.send("Kullanım: `h!paraver @kullanıcı <miktar>`")
            return
        
        embed = discord.Embed(
            title="💸 Para Gönderildi!",
            description=f"**{ctx.author}** → **{member}**\nMiktar: **{miktar}** TL",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='banka')
    async def banka(self, ctx, miktar: str = None):
        embed = discord.Embed(
            title="🏦 Banka",
            description="Banka bakiyesi: **1000** TL\n\nKomutlar:\n`h!banka para <miktar>` - Para yatır\n`h!banka çek <miktar>` - Para çek",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='slot')
    async def slot(self, ctx, miktar: int = 10):
        if miktar < 1:
            await ctx.send("En az 1 TL yatır!")
            return
        
        semboller = ['🍒', '🍋', '🍇', '💎', '🔔', '7️⃣']
        satir = [random.choice(semboller) for _ in range(3)]
        
        embed = discord.Embed(title="🎰 Slot", color=discord.Color.gold())
        embed.add_field(name="Sonuç", value=f"| {satir[0]} | {satir[1]} | {satir[2]} |", inline=False)
        
        if satir[0] == satir[1] == satir[2]:
            kazanc = miktar * 3
            embed.add_field(name="🎉 JACKPOT!", value=f"**{kazanc}** TL kazandın!", inline=False)
        elif satir[0] == satir[1] or satir[1] == satir[2]:
            kazanc = int(miktar * 1.5)
            embed.add_field(name="⭐ İyi!", value=f"**{kazanc}** TL kazandın!", inline=False)
        else:
            embed.add_field(name="😢 Kaybettin!", value=f"**{miktar}** TL", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='market')
    async def market(self, ctx):
        embed = discord.Embed(
            title="🛒 Market",
            description="Satın almak için: `h!al <numara>`",
            color=discord.Color.gold()
        )
        embed.add_field(name="1. VIP", value="500 TL - Özel VIP rolü", inline=True)
        embed.add_field(name="2. Premium", value="1000 TL - Premium rolü", inline=True)
        embed.add_field(name="3. Oyuncu", value="250 TL - Oyuncu rolü", inline=True)
        embed.add_field(name="4. Müzik", value="150 TL - Müzik rolü", inline=True)
        embed.add_field(name="5. Teknoloji", value="300 TL - Teknoloji rolü", inline=True)
        embed.add_field(name="6. Yemek", value="100 TL - Yemek rolü", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='al')
    async def al(self, ctx, id: int = 0):
        if id <= 0:
            await ctx.send("Kullanım: `h!al <numara>`")
            return
        
        items = {
            1: {"name": "VIP", "price": 500},
            2: {"name": "Premium", "price": 1000},
            3: {"name": "Oyuncu", "price": 250},
            4: {"name": "Müzik", "price": 150},
            5: {"name": "Teknoloji", "price": 300},
            6: {"name": "Yemek", "price": 100}
        }
        
        if id not in items:
            await ctx.send("Geçersiz ürün!")
            return
        
        item = items[id]
        embed = discord.Embed(
            title="✅ Satın Alındı!",
            description=f"**{item['name']}** satın alındı! (-{item['price']} TL)",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='zar-oyna')
    async def zar(self, ctx, miktar: int = 10):
        if miktar < 1:
            await ctx.send("En az 1 TL!")
            return
        
        bot_zar = random.randint(1, 6)
        user_zar = random.randint(1, 6)
        
        embed = discord.Embed(title="🎲 Zar", color=discord.Color.blue())
        embed.add_field(name=f"{ctx.author}", value=f"**{user_zar}**", inline=True)
        embed.add_field(name="Bot", value=f"**{bot_zar}**", inline=True)
        
        if user_zar > bot_zar:
            kazanc = miktar * 2
            embed.add_field(name="🎉 Kazandın!", value=f"**{kazanc}** TL", inline=False)
        elif user_zar < bot_zar:
            embed.add_field(name="😢 Kaybettin!", value=f"**{miktar}** TL", inline=False)
        else:
            embed.add_field(name="🤝 Beraber!", value="Para iade", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='zenginler')
    async def zenginler(self, ctx):
        embed = discord.Embed(
            title="🏆 En Zenginler",
            description="""
1. 👑 Bilinmiyor#0001 - 1,500,000 TL
2. 👑 Bilinmiyor#0002 - 980,000 TL
3. 👑 Bilinmiyor#0003 - 750,000 TL
4. 👑 Bilinmiyor#0004 - 520,000 TL
5. 👑 Bilinmiyor#0005 - 350,000 TL
            """,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
