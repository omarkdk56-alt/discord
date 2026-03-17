import discord
from discord.ext import commands
import random
import asyncio

class Fun2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = bot.config['bot']['prefix']
    
    # === KOMIK KOMUTLAR ===
    
    @commands.command(name='güzel')
    async def guzel(self, ctx):
        await ctx.send(f"😎 {ctx.author} çok güzel!")
    
    @commands.command(name='tatlı')
    async def tatlı(self, ctx):
        await ctx.send(f"🍬 {ctx.author} çok tatlı!")
    
    @commands.command(name='şirin')
    async def sirin(self, ctx):
        await ctx.send(f"🐹 {ctx.author} çok şirin!")
    
    @commands.command(name='cool')
    async def cool(self, ctx):
        await ctx.send(f"😎 {ctx.author} çok cool!")
    
    @commands.command(name='üzgün')
    async def uzgun(self, ctx):
        await ctx.send(f"😢 {ctx.author} üzgün görünüyor!")
    
    @commands.command(name='mutlu')
    async def mutlu(self, ctx):
        await ctx.send(f"😊 {ctx.author} çok mutlu!")
    
    @commands.command(name='sinirli')
    async def sinirli(self, ctx):
        await ctx.send(f"😠 {ctx.author} sinirli!")
    
    @commands.command(name='şaşkın')
    async def saskın(self, ctx):
        await ctx.send(f"😮 {ctx.author} şaşkın!")
    
    @commands.command(name=' düşünen')
    async def dusunen(self, ctx):
        await ctx.send(f"🤔 {ctx.author} düşünüyor!")
    
    @commands.command(name='ağlayan')
    async def aglayan(self, ctx):
        await ctx.send(f"😭 {ctx.author} ağlıyor!")
    
    @commands.command(name='gülümseyen')
    async def gulumsayan(self, ctx):
        await ctx.send(f"😊 {ctx.author} gülümsüyor!")
    
    @commands.command(name='uyuyan')
    async def uyuyan(self, ctx):
        await ctx.send(f"😴 {ctx.author} uyuyor!")
    
    @commands.command(name='oynayan')
    async def oynayan(self, ctx):
        await ctx.send(f"🎮 {ctx.author} oynuyor!")
    
    @commands.command(name='yiyen')
    async def yiyen(self, ctx):
        await ctx.send(f"🍕 {ctx.author} yiyor!")
    
    @commands.command(name='içen')
    async def icen(self, ctx):
        await ctx.send(f"☕ {ctx.author} içiyor!")
    
    @commands.command(name='koşan')
    async def kosan(self, ctx):
        await ctx.send(f"🏃 {ctx.author} koşuyor!")
    
    @commands.command(name='zıplayan')
    async def zıplayan(self, ctx):
        await ctx.send(f"🦘 {ctx.author} zıplıyor!")
    
    @commands.command(name='danseden')
    async def danseden(self, ctx):
        await ctx.send(f"💃 {ctx.author} dans ediyor!")
    
    @commands.command(name='şarkı-söyleyen')
    async def sarki_soyleyen(self, ctx):
        await ctx.send(f"🎤 {ctx.author} şarkı söylüyor!")
    
    @commands.command(name='uyaran')
    async def uyaran(self, ctx):
        await ctx.send(f"⏰ {ctx.author} uyarıyor!")
    
    @commands.command(name='korkutan')
    async def korkutan(self, ctx):
        await ctx.send(f"👻 {ctx.author} korkutuyor!")
    
    @commands.command(name='şaşırtan')
    async def sasırtan(self, ctx):
        await ctx.send(f"😱 {ctx.author} şaşırtıyor!")
    
    @commands.command(name='neşelendiren')
    async def neselendiren(self, ctx):
        await ctx.send(f"😄 {ctx.author} neşelendirdi!")
    
    @commands.command(name='sakinleştiren')
    async def sakinlestiren(self, ctx):
        await ctx.send(f"😌 {ctx.author} sakinleşti!")
    
    @commands.command(name='heyecanlı')
    async def heyecanlı(self, ctx):
        await ctx.send(f"🤩 {ctx.author} heyecanlı!")
    
    @commands.command(name='utangaç')
    async def utangac(self, ctx):
        await ctx.send(f"😳 {ctx.author} utangaç!")
    
    @commands.command(name='güvenilir')
    async def guvenilir(self, ctx):
        await ctx.send(f"🤝 {ctx.author} güvenilir!")
    
    @commands.command(name='tehlikeli')
    async def tehlikeli(self, ctx):
        await ctx.send(f"⚠️ {ctx.author} tehlikeli!")
    
    @commands.command(name='güçlü')
    async def guclu(self, ctx):
        await ctx.send(f"💪 {ctx.author} güçlü!")
    
    @commands.command(name='zayıf')
    async def zayıf(self, ctx):
        await ctx.send(f"💪 {ctx.author} zayıf!")
    
    @commands.command(name='hızlı')
    async def hızlı(self, ctx):
        await ctx.send(f"⚡ {ctx.author} hızlı!")
    
    @commands.command(name='yavaş')
    async def yavas(self, ctx):
        await ctx.send(f"🐢 {ctx.author} yavaş!")
    
    @commands.command(name='zeki')
    async def zeki(self, ctx):
        await ctx.send(f"🧠 {ctx.author} zeki!")
    
    @commands.command(name='aptal')
    async def aptal(self, ctx):
        await ctx.send(f"🤪 {ctx.author} aptal!")
    
    @commands.command(name='başarılı')
    async def basarili(self, ctx):
        await ctx.send(f"🏆 {ctx.author} başarılı!")
    
    @commands.command(name='başarısız')
    async def basarisiz(self, ctx):
        await ctx.send(f"❌ {ctx.author} başarısız!")
    
    @commands.command(name='aktif')
    async def aktif(self, ctx):
        await ctx.send(f"✅ {ctx.author} aktif!")
    
    @commands.command(name='pasif')
    async def pasif(self, ctx):
        await ctx.send(f"⏸️ {ctx.author} pasif!")
    
    @commands.command(name='gizli')
    async def gizli(self, ctx):
        await ctx.send(f"🤫 {ctx.author} gizli!")
    
    @commands.command(name='açık')
    async def acık(self, ctx):
        await ctx.send(f"🔓 {ctx.author} açık!")
    
    @commands.command(name='çirkin')
    async def cirkin(self, ctx):
        await ctx.send(f"😱 {ctx.author} çirkin!")
    
    @commands.command(name='tarih')
    async def tarih2(self, ctx):
        import datetime
        await ctx.send(f"📅 Bugün: {datetime.datetime.now().strftime('%d/%m/%Y')}")
    
    @commands.command(name='vakit')
    async def vakit(self, ctx):
        import datetime
        await ctx.send(f"⏰ Şimdi: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    @commands.command(name='yıl')
    async def yil(self, ctx):
        import datetime
        await ctx.send(f"📆 Yıl: {datetime.datetime.now().year}")
    
    @commands.command(name='ay')
    async def ay(self, ctx):
        import datetime
        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        await ctx.send(f"📆 Ay: {aylar[datetime.datetime.now().month - 1]}")
    
    @commands.command(name='gün')
    async def gun(self, ctx):
        import datetime
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        await ctx.send(f"📆 Gün: {gunler[datetime.datetime.now().weekday()]}")
    
    @commands.command(name='dakika')
    async def dakika(self, ctx):
        import datetime
        await ctx.send(f"⏰ Dakika: {datetime.datetime.now().minute}")
    
    @commands.command(name='saniye')
    async def saniye(self, ctx):
        import datetime
        await ctx.send(f"⏰ Saniye: {datetime.datetime.now().second}")
    
    @commands.command(name='milyenyıl')
    async def milenyil(self, ctx):
        import datetime
        await ctx.send(f"🎆 Yıl: {datetime.datetime.now().year} - Milenyum!")
    
    @commands.command(name='mevsim')
    async def mevsim(self, ctx):
        import datetime
        ay = datetime.datetime.now().month
        if ay in [12, 1, 2]:
            await ctx.send("❄️ Kış mevsimi!")
        elif ay in [3, 4, 5]:
            await ctx.send("🌸 İlkbahar mevsimi!")
        elif ay in [6, 7, 8]:
            await ctx.send("☀️ Yaz mevsimi!")
        else:
            await ctx.send("🍂 Sonbahar mevsimi!")
    
    @commands.command(name='tatil')
    async def tatil(self, ctx):
        await ctx.send(f"🏖️ {ctx.author} tatil istiyor!")
    
    @commands.command(name='uyku')
    async def uyku(self, ctx):
        await ctx.send(f"😴 {ctx.author} uyku istiyor!")
    
    @commands.command(name='içecek2')
    async def icecek2(self, ctx):
        icecekler = ["Kahve", "Çay", "Kola", "Ayran", "Limonata", "Su", "Portakal suyu", "Meyve suyu"]
        await ctx.send(f"🥤 {ctx.author} {random.choice(icecekler)} içmek istiyor!")
    
    @commands.command(name='müzik')
    async def muzik2(self, ctx):
        turler = ["Pop", "Rock", "Rap", "Türkçe", "Elektronik", "Jazz", "Klasik", "Metal"]
        await ctx.send(f"🎵 {ctx.author} {random.choice(turler)} müzik dinlemek istiyor!")
    
    @commands.command(name='film2')
    async def film2(self, ctx):
        turler = ["Aksiyon", "Komedi", "Dram", "Korku", "Bilim Kurgu", "Romantik", "Gerilim", "Animasyon"]
        await ctx.send(f"🎬 {ctx.author} {random.choice(turler)} film izlemek istiyor!")
    
    @commands.command(name='dizi2')
    async def dizi2(self, ctx):
        turler = ["Aksiyon", "Komedi", "Dram", "Korku", "Bilim Kurgu", "Romantik", "Gerilim", "Belgesel"]
        await ctx.send(f"📺 {ctx.author} {random.choice(turler)} dizi izlemek istiyor!")
    
    @commands.command(name='kitap')
    async def kitap(self, ctx):
        turler = ["Roman", "Hikaye", "Şiir", "Bilim", "Tarih", "Felsefe", "Biyografi", "Macera"]
        await ctx.send(f"📚 {ctx.author} {random.choice(turler)} kitap okumak istiyor!")
    
    @commands.command(name='spor')
    async def spor(self, ctx):
        sporlar = ["Futbol", "Basketbol", "Voleybol", "Tenis", "Yüzme", "Koşu", "Bisiklet", "Wrestling"]
        await ctx.send(f"⚽ {ctx.author} {random.choice(sporlar)} yapmak istiyor!")
    
    @commands.command(name='hayvan')
    async def hayvan(self, ctx):
        hayvanlar = ["Köpek", "Kedi", "Kuş", "Balık", "Tavşan", "Hamster", "Kaplumbağa", "Yılan", "Papağan", "Khameleon"]
        await ctx.send(f"🐾 {random.choice(hayvanlar)}!")
    
    @commands.command(name='renk2')
    async def renk2(self, ctx):
        renkler = ["Kırmızı", "Mavi", "Yeşil", "Sarı", "Turuncu", "Mor", "Pembe", "Siyah", "Beyaz", "Kahverengi"]
        await ctx.send(f"🎨 {random.choice(renkler)}!")
    
    @commands.command(name='ülke')
    async def ulke(self, ctx):
        ukeler = ["Türkiye", "ABD", "İngiltere", "Almanya", "Fransa", "İtalya", "İspanya", "Japonya", "Çin", "Rusya"]
        await ctx.send(f"🌍 {random.choice(ukeler)}!")
    
    @commands.command(name='şehir')
    async def sehir(self, ctx):
        sehirler = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Trabzon", "Erzurum", "Konya", "Adana", "Mersin"]
        await ctx.send(f"🏙️ {random.choice(sehirler)}!")
    
    @commands.command(name='yemek2')
    async def yemek3(self, ctx):
        await ctx.send("🍕 Lahmacun")
        await ctx.send("🍔 Burger")
        await ctx.send("🌮 Taco")
        await ctx.send("🍣 Sushi")
        await ctx.send("🍜 Noodle")
    
    @commands.command(name='mevsim2')
    async def mevsim2(self, ctx):
        await ctx.send("❄️ Kış")
        await ctx.send("🌸 İlkbahar")
        await ctx.send("☀️ Yaz")
        await ctx.send("🍂 Sonbahar")
    
    @commands.command(name='tatil2')
    async def tatil2(self, ctx):
        yerler = ["Antalya", "Marmaris", "Bodrum", "Kapadokya", "İstanbul", "Paris", "Roma", "Barselona"]
        await ctx.send(f"🏖️ {random.choice(yerler)}")
    
    @commands.command(name='dünya')
    async def dunya(self, ctx):
        await ctx.send("🌍 Dünya - Evimiz!")
    
    @commands.command(name='ay2')
    async def ay2(self, ctx):
        await ctx.send("🌙 Ay - Dünya'nın uydusu!")
    
    @commands.command(name='güneş')
    async def gunes(self, ctx):
        await ctx.send("☀️ Güneş - Yıldızımız!")
    
    @commands.command(name='galaksi')
    async def galaksi(self, ctx):
        await ctx.send("🌌 Galaksi - Samanyolu!")
    
    @commands.command(name='uzay')
    async def uzay(self, ctx):
        await ctx.send("🚀 Uzay - Sonsuz boşluk!")
    
    @commands.command(name='dünya2')
    async def dunya2(self, ctx):
        await ctx.send("🌍 Dünya - Evrendeki tek yaşam alanı!")
    
    @commands.command(name='mars')
    async def mars(self, ctx):
        await ctx.send("🔴 Mars - Kızıl gezegen!")
    
    @commands.command(name='venüs')
    async def venus(self, ctx):
        await ctx.send("💛 Venüs - Parlak gezegen!")
    
    @commands.command(name='jüpiter')
    async def jupiter(self, ctx):
        await ctx.send("🟤 Jüpiter - En büyük gezegen!")
    
    @commands.command(name='satürn')
    async def saturn(self, ctx):
        await ctx.send("🪐 Satürn - Halkalı gezegen!")
    
    @commands.command(name='neptün')
    async def neptun(self, ctx):
        await ctx.send("🔵 Neptün - Buz devi!")
    
    @commands.command(name='ürün')
    async def urun(self, ctx):
        urunler = ["Elma", "Armut", "Muz", "Portakal", "Üzüm", "Karpuz", "Kavun", "Çilek", "Kiraz", "Şeftali"]
        await ctx.send(f"🍎 {random.choice(urunler)}!")
    
    @commands.command(name='içecek3')
    async def icecek3(self, ctx):
        await ctx.send("☕ Kahve")
        await ctx.send("🍵 Çay")
        await ctx.send("🥤 Kola")
        await ctx.send("🍺 Bira")
    
    @commands.command(name='alkol')
    async def alkol(self, ctx):
        await ctx.send("❌ 18 yaş altı alkol tüketmemelidir!")
    
    @commands.command(name='sigara')
    async def sigara(self, ctx):
        await ctx.send("❌ Sigara sağlığa zararlıdır!")
    
    @commands.command(name='uyuşturucu')
    async def uyusturucu(self, ctx):
        await ctx.send("❌ Uyuşturucu kullanmak yasaktır ve zararlıdır!")
    
    @commands.command(name='internet')
    async def internet(self, ctx):
        await ctx.send("🌐 İnternet - Dünyayı birbirine bağlar!")
    
    @commands.command(name='telefon')
    async def telefon(self, ctx):
        await ctx.send("📱 Telefon - İletişim aracı!")
    
    @commands.command(name='bilgisayar')
    async def bilgisayar(self, ctx):
        await ctx.send("💻 Bilgisayar - Çalışma aracı!")
    
    @commands.command(name='araba')
    async def araba(self, ctx):
        await ctx.send("🚗 Araba - Ulaşım aracı!")
    
    @commands.command(name='uçak')
    async def ucak(self, ctx):
        await ctx.send("✈️ Uçak - Hızlı ulaşım!")
    
    @commands.command(name='gemi')
    async def gemi(self, ctx):
        await ctx.send("🚢 Gemi - Deniz taşıtı!")
    
    @commands.command(name='tren')
    async def tren(self, ctx):
        await ctx.send("🚂 Tren - Raylı ulaşım!")
    
    @commands.command(name='bisiklet')
    async def bisiklet(self, ctx):
        await ctx.send("🚲 Bisiklet - Sağlıklı ulaşım!")
    
    @commands.command(name='motor')
    async def motor(self, ctx):
        await ctx.send("🏍️ Motosiklet - Hızlı!")
    
    @commands.command(name='otel')
    async def otel(self, ctx):
        await ctx.send("🏨 Otel - Konaklama yeri!")
    
    @commands.command(name='restoran')
    async def restoran(self, ctx):
        await ctx.send("🍽️ Restoran - Yemek yeri!")
    
    @commands.command(name='okul')
    async def okul(self, ctx):
        await ctx.send("🏫 Okul - Eğitim yeri!")
    
    @commands.command(name='hastane')
    async def hastane(self, ctx):
        await ctx.send("🏥 Hastane - Sağlık yeri!")
    
    @commands.command(name='kütüphane')
    async def kutuphane(self, ctx):
        await ctx.send("📚 Kütüphane - Kitap yeri!")
    
    @commands.command(name='stadyum')
    async def stadyum(self, ctx):
        await ctx.send("🏟️ Stadyum - Maç yeri!")
    
    @commands.command(name='sinema')
    async def sinema(self, ctx):
        await ctx.send("🎬 Sinema - Film yeri!")
    
    @commands.command(name='tiyatro')
    async def tiyatro(self, ctx):
        await ctx.send("🎭 Tiyatro - Gösteri yeri!")
    
    @commands.command(name='konser')
    async def konser(self, ctx):
        await ctx.send("🎤 Konser - Müzik yeri!")
    
    @commands.command(name='plaj')
    async def plaj(self, ctx):
        await ctx.send("🏖️ Plaj - Deniz yeri!")
    
    @commands.command(name='dağ')
    async def dag(self, ctx):
        await ctx.send("🏔️ Dağ - Yüksek yer!")
    
    @commands.command(name='orman')
    async def orman(self, ctx):
        await ctx.send("🌲 Orman - Doğa yeri!")
    
    @commands.command(name='göl')
    async def gol(self, ctx):
        await ctx.send("🌊 Göl - Su yeri!")
    
    @commands.command(name='nehir')
    async def nehir(self, ctx):
        await ctx.send("🌊 Nehir - Akarsu!")
    
    @commands.command(name='şelale')
    async def selale(self, ctx):
        await ctx.send("💧 Şelale - Güzel manzara!")
    
    @commands.command(name='kanyon')
    async def kanyon(self, ctx):
        await ctx.send("🏞️ Kanyon - Doğa harikası!")
    
    @commands.command(name='volkan')
    async def volkan(self, ctx):
        await ctx.send("🌋 Volkan - Ateş dağı!")
    
    @commands.command(name='ada')
    async def ada(self, ctx):
        await ctx.send("🏝️ Ada - Su içinde kara!")
    
    @commands.command(name='yarımada')
    async def yarimada(self, ctx):
        await ctx.send("🏜️ Yarımada - Denize uzanan!")
    
    @commands.command(name='kıta')
    async def kita(self, ctx):
        await ctx.send("🌍 Kıta - Büyük toprak!")
    
    @commands.command(name='okyanus')
    async def okyanus(self, ctx):
        await ctx.send("🌊 Okyanus - Tüm sular!")
    
    @commands.command(name='deniz')
    async def deniz(self, ctx):
        await ctx.send("🌊 Deniz - Tuzlu su!")
    
    @commands.command(name='nehir2')
    async def nehir2(self, ctx):
        await ctx.send("🌊 Nehir - Tatlı su!")
    
    @commands.command(name='göl2')
    async def gol2(self, ctx):
        await ctx.send("🌊 Göl - Duran su!")
    
    @commands.command(name='akarsu')
    async def akarsu(self, ctx):
        await ctx.send("🌊 Akarsu - akan su!")
    
    @commands.command(name='baraj')
    async def baraj(self, ctx):
        await ctx.send("💧 Baraj - Su birikintisi!")
    
    @commands.command(name='havuz')
    async def havuz(self, ctx):
        await ctx.send("🏊 Havuz - Yüzme yeri!")
    
    @commands.command(name='plaj2')
    async def plaj2(self, ctx):
        await ctx.send("🏖️ Plaj - Kum ve deniz!")
    
    @commands.command(name='dalga')
    async def dalga(self, ctx):
        await ctx.send("🌊 Dalga - Deniz hareketi!")
    
    @commands.command(name='gelgit')
    async def gelgit(self, ctx):
        await ctx.send("🌊 Gelgit - Deniz yükselmesi!")
    
    @commands.command(name='tsunami')
    async def tsunami(self, ctx):
        await ctx.send("🌊 Tsunami - Büyük dalga!")
    
    @commands.command(name='fırtına')
    async def fırtına(self, ctx):
        await ctx.send("🌪️ Fırtına - Şiddetli rüzgar!")
    
    @commands.command(name='rüzgar')
    async def ruzgar(self, ctx):
        await ctx.send("💨 Rüzgar - Havanın hareketi!")
    
    @commands.command(name='yağmur')
    async def yagmur(self, ctx):
        await ctx.send("🌧️ Yağmur - Su damlaları!")
    
    @commands.command(name='kar')
    async def kar(self, ctx):
        await ctx.send("❄️ Kar - Beyaz kristaller!")
    
    @commands.command(name='dolu')
    async def dolu(self, ctx):
        await ctx.send("🌨️ Dolu - Buz topları!")
    
    @commands.command(name='gökkuşağı')
    async def gokkusagı(self, ctx):
        await ctx.send("🌈 Gökkuşağı - Renkli yay!")
    
    @commands.command(name='güneş2')
    async def gunes2(self, ctx):
        await ctx.send("☀️ Güneş - Isı ve ışık kaynağı!")
    
    @commands.command(name='ay3')
    async def ay3(self, ctx):
        await ctx.send("🌙 Ay - Gece ışığı!")
    
    @commands.command(name='yıldız2')
    async def yildiz2(self, ctx):
        await ctx.send("⭐ Yıldız - Uzaktaki güneşler!")
    
    @commands.command(name='gezegen')
    async def gezegen(self, ctx):
        await ctx.send("🪐 Gezegen - Yıldızların etrafında dönen!")
    
    @commands.command(name='uydu')
    async def uydu(self, ctx):
        await ctx.send("🛰️ Uydu - Uzay aracı!")
    
    @commands.command(name='roket')
    async def roket(self, ctx):
        await ctx.send("🚀 Roket - Uzaya giden!")
    
    @commands.command(name='istasyon')
    async def istasyon(self, ctx):
        await ctx.send("🛸 Uzay istasyonu - Uzayda yaşam!")
    
    @commands.command(name='astronot')
    async def astronot(self, ctx):
        await ctx.send("👨‍🚀 Astronot - Uzay gezgini!")
    
    @commands.command(name='uzaylı')
    async def uzaylı(self, ctx):
        await ctx.send("👽 Uzaylı - Uzaydaki yaşam!")
    
    @commands.command(name='galaksi2')
    async def galaksi2(self, ctx):
        await ctx.send("🌌 Galaksi - Yıldız topluluğu!")
    
    @commands.command(name='karadelik')
    async def karadelik(self, ctx):
        await ctx.send("⚫ Karadelik - Her şeyi yutan!")
    
    @commands.command(name='nebula')
    async def nebula(self, ctx):
        await ctx.send("🌫️ Nebula - Uzay bulutu!")
    
    @commands.command(name='kuyrukluyıldız')
    async def kuyrukluyildiz(self, ctx):
        await ctx.send("☄️ Kuyruklu yıldız - Gezegen!")

async def setup(bot):
    await bot.add_cog(Fun2(bot))
