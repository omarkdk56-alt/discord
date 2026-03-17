import discord
from discord.ext import commands
import random
import asyncio

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conversations = {}
        
        self.responses = {
            'selam': [
                "Selam! 👋 Nasılsın?",
                "Aleykümselam! 🙌",
                "Selam dostum! 🔥",
                "Hoş geldin! ✨"
            ],
            'merhaba': [
                "Merhaba! 👋",
                "Selam! 🙌",
                "Hoş geldin! ✨"
            ],
            'napıyosun': [
                "İyiyim, sen napıyorsun? 😊",
                "Buradayım, seninle sohbet etmeyi bekliyorum! 💬",
                "İyiyim, sen nasılsın? 🌟"
            ],
            'nasılsın': [
                "İyiyim, sağ ol! Sen nasılsın? 😊",
                "Çok iyiyim, seni gördüğüme sevindim! 🙌",
                "Harika! Sen napıyorsun? 🌟"
            ],
            'ne yapıyosun': [
                "Seninle sohbet ediyorum! 💬",
                "Burada oturup seninle konuşmayı bekliyorum 😊",
                "Hiçbir şey yapmıyorum, seninle konuşmayı tercih ederim! 🌟"
            ],
            'yardım': [
                "Tabii ki yardımcı olurum! 🙌\n\n"
                "**h!yardim** yazarak tüm komutlarımı görebilirsin!\n"
                "Bana doğrudan yazabilirsin, sohbet edebiliriz! 💬",
                "Buradayım! 😊\n\n"
                "Tüm komutlarımı görmek için **h!yardim** yazabilirsin!"
            ],
            'yardim': [
                "Tabii ki yardımcı olurum! 🙌\n\n"
                "**h!yardim** yazarak tüm komutlarımı görebilirsin!\n"
                "Bana doğrudan yazabilirsin, sohbet edebiliriz! 💬"
            ],
            'sa': [
                "Aleykümselam! 🙌",
                "Selam! 👋",
                "Hoş geldin! ✨"
            ],
            'bb': [
                "Görüşürüz! 👋",
                "Bay bay! 😊",
                "Tekrar beklerim! 🌟"
            ],
            'byy': [
                "Görüşürüz! 👋",
                "Bay bay! 😊",
                "Tekrar beklerim! 🌟"
            ],
            'kral': [
                "Teşekkürler! 👑 Sen de kral'sın! 😎",
                "Eyvallah dostum! 💪",
                "Sağ ol! 🙏"
            ],
            'aşk': [
                "Aşk güzel bir şey! ❤️",
                "Kalpler! 💕",
                "Romantik misin? 😊"
            ],
            'sunucu': [
                "Bu sunucu harika! 🔥",
                "Sunucu çok güzel görünüyor! ✨",
                "Burada olmak güzel! 🙌"
            ],
            'bot': [
                "Ben bir Discord botuyum! 🤖\n"
                "h!yardim yazarak neler yapabileceğimi görebilirsin!",
                "İstersen sohbet edebiliriz! 💬"
            ],
            'hava': [
                "Hava nasıl bilmiyorum ama burada hava çok sıcak! 🔥",
                "Dışarıyı bilmiyorum ama burası çok sıcak! 🌡️",
                "Bot olduğum için dışarıyı göremiyorum ama sen nasılsın? 😊"
            ],
            'yemek': [
                "Yemek! 🍕 Ben yemek yiyemiyorum ama çok lezzetli olduğunu biliyorum!",
                "Hmm, yemek... Bot olduğum için tadını alamıyorum ama görünüşü güzel! 😋",
                "En sevdiğim yemek... aslında hiçbir şey yemiyorum! 🤖"
            ],
            'müzik': [
                "Müzik harika bir şey! 🎵\n"
                "h!cal <şarkı> yazarak müzik açabilirsin!",
                "Müzik dinlemeyi seviyorum! 🎶"
            ],
            'oyun': [
                "Oyun oynamayı seviyorum! 🎮",
                "Hangi oyunu oynuyorsun? 🎯",
                "Ben de oyun oynamayı seviyorum! 🔥"
            ],
            'kötü': [
                "Üzgünüm... 😢\n"
                "Bir sorun mu var? Yardımcı olabilir miyim? 💬",
                "Kötü hissediyorsan buradayım! 🙌"
            ],
            'sıkıldım': [
                "Sıkıldıysan sohbet edebiliriz! 💬\n"
                "Ya da h!oylama yaparak eğlence başlatabilirsin! 🎉",
                "Sıkıntıyı yenmek için bir şeyler yapalım! 🎮"
            ],
            'efendim': [
                "Buyur! 🙌\n"
                "Nasıl yardımcı olabilirim?",
                "Buradayım! 😊"
            ],
            'teşekkür': [
                "Rica ederim! 🙏\n"
                "Her zaman yardımcı olmaktan mutluluk duyarım! ✨",
                "Önemli değil! 🙌"
            ],
            'tşk': [
                "Rica ederim! 🙏",
                "Önemli değil! 🙌"
            ],
            'lol': [
                "Haha, güldürdün! 😂",
                "😂",
                "Çok komik! 😄"
            ],
            'wq': [
                "Haha, güldürdün! 😂",
                "😂",
                "Çok komik! 😄"
            ],
            'gel': [
                "Zaten buradayım! 😄",
                "Geliyorum! 🏃‍♂️",
                "Buradayım! 🙌"
            ],
            'git': [
                "Tamam, görüşürüz! 👋",
                "Güle güle! 😢",
                "Tekrar beklerim! 🌟"
            ],
            'ögle': [
                "Çay molası mı? ☕",
                "Yemek zamanı! 🍕",
                "Açlıktan ölüyorum... aslında bot olduğum için açlığım yok! 🤖"
            ],
            'gece': [
                "İyi geceler! 🌙",
                "Uyku zamanı mı? 😴",
                "Rüyalarında görüşürüz! 🌟"
            ],
            'sabah': [
                "Günaydın! ☀️",
                "Sabahın hayırlı olsun! 🌅",
                "Yeni bir gün başlıyor! ✨"
            ],
            'günaydın': [
                "Günaydın! ☀️",
                "Sabahın hayırlı olsun! 🌅",
                "Günaydın! Nasıl uyudun? 😴"
            ],
            'iyi geceler': [
                "İyi geceler! 🌙",
                "Rüya gör! 😴",
                "Görüşürüz! 👋"
            ],
        }
        
        self.random_responses = [
            "Anladım! 😊",
            "Evet, doğru! ✅",
            "Harika! 🔥",
            "İlginç! 🤔",
            "Gerçekten mi? 😮",
            "Çok güzel! ✨",
            "Bence de! 🙌",
            "Hmm, düşüneyim... 💭",
            "Kesinlikle! 💪",
            "Tabii ki! ✅",
            "Bu harika bir fikir! 🎉",
            "Süper! 😎",
            "Olabilir! 🤔",
            "Kim bilir? 🌟",
            "Belki! 😉"
        ]
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        content = message.content.lower()
        
        # Check if message starts with "h " or "h!"
        if content.startswith('h ') or content.startswith('h!'):
            return  # Let bot commands handle it
        
        # Check for AI chat triggers
        for trigger, responses in self.responses.items():
            if trigger in content:
                response = random.choice(responses)
                await message.channel.send(response)
                return
        
        # Random chance response for other messages
        if random.random() < 0.05:  # 5% chance
            response = random.choice(self.random_responses)
            await message.channel.send(response)
    
    @commands.command(name='sohbet', aliases=['chat', 'ai'])
    async def sohbet(self, ctx, *, message):
        """Yapay zeka ile sohbet et"""
        msg = message.lower()
        
        for trigger, responses in self.responses.items():
            if trigger in msg:
                response = random.choice(responses)
                await ctx.send(response)
                return
        
        # Default responses
        responses = [
            f"Anladım! '{message}' dedin. 🙌",
            f"Bu ilginç! '{message}' hakkında daha fazla şey öğrenmek isterim! 💬",
            f"Hmm, '{message}'... Çok derin! 🤔",
            f"Seni anlıyorum! 😊",
            f"Bu konuda daha fazla konuşabiliriz! 🌟"
        ]
        await ctx.send(random.choice(responses))
    
    @commands.command(name='sor')
    async def sor(self, ctx, *, soru):
        """Yapay zekaya soru sor"""
        await ctx.send(f"Soru: **{soru}**\n\nDüşünüyorum... 🤔")
        await asyncio.sleep(1)
        
        answers = [
            "Bu ilginç bir soru! Cevabını bilmiyorum ama araştırmam gerekiyor! 🔍",
            "Hmm, bu konuda kesin bir cevabım yok! Başka bir soru dene! 😊",
            f"'{soru}' hakkında düşünüyorum... Bir cevabım yok ama öğrenmeye çalışıyorum! 🤖",
            "Bu soruyu cevaplamak için daha fazla bilgiye ihtiyacım var! 💭",
            f"'{soru}' - Çok güzel bir soru! Ama şimdilik cevaplayamıyorum! 😅"
        ]
        await ctx.send(random.choice(answers))

async def setup(bot):
    await bot.add_cog(AIChat(bot))
