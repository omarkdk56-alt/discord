import discord
from discord.ext import commands
import wavelink

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_load(self):
        try:
            node = wavelink.Node(
                identifier="main",
                uri="http://lavalink.orvn.me:443",
                password="orvn"
            )
            await wavelink.Pool.connect(nodes=[node], client=self.bot)
            print(f"Music node bağlandı!")
        except Exception as e:
            print(f"Music node bağlantı hatası: {e}")
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload):
        print(f"Music node connected: {payload.node.identifier}")
    
    @commands.command(name='cal', aliases=['play', 'çal', 'oynat'])
    async def cal(self, ctx, *, query: str):
        if not ctx.author.voice:
            await ctx.send("Önce bir ses kanalına gir!")
            return
        
        try:
            if not ctx.voice_client:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                player = ctx.voice_client
        except Exception as e:
            await ctx.send(f"Bağlantı hatası: {e}")
            return
        
        player.ctx = ctx
        
        query = query.strip()
        if not query.startswith("http"):
            query = f"ytsearch:{query}"
        
        try:
            tracks = await wavelink.Pool.fetch_tracks(query)
        except Exception as e:
            await ctx.send(f"Şarkı arama hatası: {e}")
            return
        
        if not tracks:
            await ctx.send("Şarkı bulunamadı!")
            return
        
        track = tracks[0]
        player.queue.put(track)
        embed = discord.Embed(
            title="🎵 Sıraya Eklendi",
            description=f"**{track.title}** sıraya eklendi",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
        if not player.playing:
            await player.play(await player.queue.get())
    
    @commands.command(name='dur', aliases=['stop', 'durdur'])
    async def dur(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Şu anda müzik çalmıyor!")
            return
        
        await ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Müzik durduruldu ve kanaldan çıkıldı!")
    
    @commands.command(name='gec', aliases=['skip', 'atla'])
    async def gec(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Şu anda müzik çalmıyor!")
            return
        
        player = ctx.voice_client
        
        if player.queue.is_empty:
            await ctx.send("Sırada başka şarkı yok!")
            return
        
        await player.skip()
        await ctx.send("⏭ Geçildi!")
    
    @commands.command(name='duraklat', aliases=['pause', 'beklet'])
    async def duraklat(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Şu anda müzik çalmıyor!")
            return
        
        player = ctx.voice_client
        
        if player.paused:
            await ctx.send("Müzik zaten durdurulmuş!")
            return
        
        await player.pause()
        await ctx.send("⏸️ Müzik durduruldu!")
    
    @commands.command(name='devamet', aliases=['resume', 'devam'])
    async def devamet(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Şu anda müzik çalmıyor!")
            return
        
        player = ctx.voice_client
        
        if not player.paused:
            await ctx.send("Müzik zaten çalıyor!")
            return
        
        await player.resume()
        await ctx.send("▶️ Müzik devam ediyor!")
    
    @commands.command(name='sira', aliases=['queue', 'liste'])
    async def sira(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Şu anda müzik çalmıyor!")
            return
        
        player = ctx.voice_client
        
        if player.queue.is_empty:
            await ctx.send("Sıra boş!")
            return
        
        embed = discord.Embed(
            title="📜 Şarkı Sırası",
            color=discord.Color.blue()
        )
        
        queue_list = list(player.queue)[:10]
        for i, track in enumerate(queue_list, 1):
            embed.add_field(
                name=f"{i}. {track.title[:50]}",
                value=f"Süre: {int(track.length // 60)}:{int(track.length % 60):02d}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='ses', aliases=['volume', 'vol'])
    async def ses(self, ctx, volume: int = None):
        if not ctx.voice_client:
            await ctx.send("Şu anda müzik çalmıyor!")
            return
        
        player = ctx.voice_client
        
        if volume is None:
            await ctx.send(f"🔊 Mevcut ses seviyesi: {player.volume}%")
            return
        
        if volume < 1 or volume > 100:
            await ctx.send("Ses seviyesi 1-100 arasında olmalı!")
            return
        
        await player.set_volume(volume)
        await ctx.send(f"🔊 Ses seviyesi {volume}% olarak ayarlandı!")
    
    @commands.command(name='np', aliases=['nowplaying', 'suan'])
    async def np(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Şu anda müzik çalmıyor!")
            return
        
        player = ctx.voice_client
        
        if not player.current:
            await ctx.send("Şu anda şarkı çalmıyor!")
            return
        
        track = player.current
        
        embed = discord.Embed(
            title="🎵 Şimdi Çalıyor",
            description=f"**{track.title}**",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='baglan', aliases=['join'])
    async def baglan(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Önce bir ses kanalına gir!")
            return
        
        if ctx.voice_client:
            await ctx.send("Zaten bir ses kanalındayım!")
            return
        
        player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await ctx.send(f"✅ {ctx.author.voice.channel} kanalına bağlandım!")
    
    @commands.command(name='cik', aliases=['leave', 'çık'])
    async def cik(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Bir ses kanalında değilim!")
            return
        
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Ses kanalından çıktım!")
    
    @commands.command(name='muzik', aliases=['müzik', 'musichelp', 'müzikyardım'])
    async def muzikyardim(self, ctx):
        embed = discord.Embed(
            title="🎵 Müzik Komutları",
            description=f"{self.bot.user.name} - Müzik Kategorisi",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        commands_list = """
**🎵 Çal**
`{p}cal <şarkı>` - Şarkı çal veya sıraya ek
Örnek: `{p}cal sad songs`

**⏹️ Dur**
`{p}dur` - Müziği durdur ve çık

**⏭️ Geç**
`{p}gec` - Sonraki şarkıya geç

**⏸️ Duraklat**
`{p}duraklat` - Müziği durdur

**▶️ Devam Et**
`{p}devamet` - Durdurulan müziği devam ettir

**📜 Sıra**
`{p}sira` - Şarkı listesini göster

**🔊 Ses**
`{p}ses [0-100]` - Ses seviyesini ayarla

**🎶 Şimdi Çalan**
`{p}np` - Şimdi çalan şarkıyı göster

**🔗 Bağlan**
`{p}baglan` - Ses kanalına bağlan

**👋 Çık**
`{p}cik` - Ses kanalından çık
""".format(p=self.bot.config['bot']['prefix'])
        
        embed.add_field(name="📜 Komut Listesi", value=commands_list, inline=False)
        embed.set_footer(text=f"Ana menü için: {self.bot.config['bot']['prefix']}yardim", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
