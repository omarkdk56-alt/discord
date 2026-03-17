import discord
from discord.ext import commands
from discord import ui
import asyncio
import random

class TicketModal(ui.Modal, title="Ticket Oluştur"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.konu = ui.TextInput(label="Konu", placeholder="Ticket konusunu yaz...", required=True, max_length=100)
        self.mesaj = ui.TextInput(label="Mesaj", placeholder="Sorununu detaylı yaz...", required=True, max_length=1000, style=discord.TextStyle.paragraph)
        self.add_item(self.konu)
        self.add_item(self.mesaj)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        ticket_kanal = await interaction.guild.create_text_channel(
            f"destek-{interaction.user.name}",
            category=discord.utils.get(interaction.guild.categories, name="Tickets") or await interaction.guild.create_category("Tickets"),
            topic=f"Kullanıcı: {interaction.user} | Konu: {self.konu.value}"
        )
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
        }
        await ticket_kanal.edit(overwrites=overwrites)
        
        embed = discord.Embed(
            title="🎫 Destek Talebi",
            description=f"**Konu:** {self.konu.value}\n\n**Mesaj:**\n{self.mesaj.value}",
            color=discord.Color.blue()
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text="Ticket kapatmak için aşağıdaki butona tıkla!")
        
        view = TicketCloseView(self.bot, interaction.user, ticket_kanal)
        await ticket_kanal.send(embed=embed, content=interaction.user.mention, view=view)
        
        await interaction.followup.send(f"✅ Ticket oluşturuldu! {ticket_kanal.mention}", ephemeral=True)

class TicketButton(ui.Button):
    def __init__(self):
        super().__init__(label="🎫 Ticket Aç", style=discord.ButtonStyle.blurple, custom_id="ticket_open")
    
    async def callback(self, interaction: discord.Interaction):
        modal = TicketModal(interaction.client)
        await interaction.response.send_modal(modal)

class TicketCloseView(ui.View):
    def __init__(self, bot, user, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user
        self.channel = channel
        self.add_item(TicketCloseButton())

class TicketCloseButton(ui.Button):
    def __init__(self):
        super().__init__(label="🔒 Ticket Kapat", style=discord.ButtonStyle.red, custom_id="ticket_close")
    
    async def callback(self, interaction: discord.Interaction):
        view = self.view
        await interaction.response.send_message("⏳ Ticket kapatılıyor...", ephemeral=True)
        await asyncio.sleep(1)
        await view.channel.delete()

class TicketPanelView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tickets = {}
    
    @commands.command(name='ticketpanel')
    @commands.has_permissions(manage_guild=True)
    async def ticketpanel(self, ctx):
        embed = discord.Embed(
            title="🎫 Destek Sistemi",
            description="Bir sorunun mu var? **Ticket Aç** butonuna tıkla ve destek talebi oluştur!",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Destek ekibimiz en kısa sürede sana yardımcı olacak!")
        
        await ctx.send(embed=embed, view=TicketPanelView())
        await ctx.message.delete()
    
    @commands.command(name='ticket', aliases=['destek', 'talep'])
    async def ticket(self, ctx):
        ticket_kanal = await ctx.guild.create_text_channel(f"destek-{ctx.author.name}")
        
        embed = discord.Embed(
            title="🎫 Destek Talebi",
            description=f"Hoş geldin {ctx.author.mention}!\n\nDestek ekibimiz seninle ilgilenecektir.\nSorununu yaz burada!",
            color=discord.Color.blue()
        )
        
        view = TicketCloseView(self.bot, ctx.author, ticket_kanal)
        await ticket_kanal.send(embed=embed, content=ctx.author.mention, view=view)
        
        await ctx.send(f"✅ Ticket oluşturuldu! {ticket_kanal.mention}")
        
        self.tickets[ticket_kanal.id] = {
            "user": ctx.author.id,
            "channel": ticket_kanal.id
        }
    
    @commands.command(name='kapat', aliases=['ticket-kapat'])
    async def kapat(self, ctx):
        if ctx.channel.name.startswith("destek-"):
            await ctx.send("⏳ Bu ticket kapatılıyor...")
            await asyncio.sleep(1)
            await ctx.channel.delete()
        else:
            await ctx.send("❌ Bu komut bir ticket kanalında kullanılmalı!")

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='cekilis')
    @commands.has_permissions(manage_messages=True)
    async def cekilis(self, ctx, sure: int = None, *, odul: str = None):
        if not sure or not odul:
            await ctx.send("Kullanim: h!cekilis <sure_saniye> <odul>")
            return
        
        embed = discord.Embed(
            title="🎉 Cekilis!",
            description=f"**Odul:** {odul}\n**Sure:** {sure} saniye\n\nKatilmak icin 🎉 emojisine tikla!",
            color=discord.Color.gold()
        )
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎉')
        
        await self.bot.db.execute(
            "INSERT INTO giveaways (message_id, server_id, channel_id, prize, winners, ends_at, created_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (str(msg.id), str(ctx.guild.id), str(ctx.channel.id), odul, 1, int(discord.utils.utcnow().timestamp()) + sure, str(ctx.author.id))
        )
        await self.bot.db.commit()
        
        await asyncio.sleep(sure)
        
        msg = await ctx.channel.fetch_message(msg.id)
        for reaction in msg.reactions:
            if str(reaction.emoji) == '🎉':
                users = await reaction.users().flatten()
                users = [u for u in users if not u.bot]
                
                if users:
                    kazanan = discord.utils.choice(users)
                    await ctx.send(f"🎉 Tebrikler {kazanan}! **{odul}** kazandin!")
                else:
                    await ctx.send("Kazanan yok!")
                break

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='hosgeldin')
    @commands.has_permissions(manage_guild=True)
    async def hosgeldin(self, ctx, kanal: discord.TextChannel = None, *, mesaj: str = None):
        if not kanal:
            await ctx.send("Bir kanal belirt!")
            return
        
        server = await self.bot.db.get_server(str(ctx.guild.id))
        await self.bot.db.execute(
            "UPDATE servers SET welcome_channel = ?, welcome_message = ?, welcome_enabled = ? WHERE server_id = ?",
            (str(kanal.id), mesaj or "Hos geldin {user}!", 1, str(ctx.guild.id))
        )
        await self.bot.db.commit()
        
        await ctx.send(f"Hos geldin sistemi ayarlandi! Kanal: {kanal}")

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='antis')
    @commands.has_permissions(manage_guild=True)
    async def antis(self, ctx, tur: str = None):
        if not tur:
            await ctx.send("Kullanim: h!antis <spam/invite/link/caps>")
            return
        
        server = await self.bot.db.get_server(str(ctx.guild.id))
        
        if tur == "spam":
            yeni = 1 if server.get('anti_spam', 0) == 0 else 0
            await self.bot.db.execute(
                "UPDATE servers SET anti_spam = ? WHERE server_id = ?",
                (yeni, str(ctx.guild.id))
            )
            await ctx.send(f"Anti-spam {'aktif' if yeni else 'pasif'}!")
        elif tur == "invite":
            yeni = 1 if server.get('anti_invite', 0) == 0 else 0
            await self.bot.db.execute(
                "UPDATE servers SET anti_invite = ? WHERE server_id = ?",
                (yeni, str(ctx.guild.id))
            )
            await ctx.send(f"Anti-invite {'aktif' if yeni else 'pasif'}!")
        elif tur == "link":
            yeni = 1 if server.get('anti_link', 0) == 0 else 0
            await self.bot.db.execute(
                "UPDATE servers SET anti_link = ? WHERE server_id = ?",
                (yeni, str(ctx.guild.id))
            )
            await ctx.send(f"Anti-link {'aktif' if yeni else 'pasif'}!")
        elif tur == "caps":
            yeni = 1 if server.get('anti_caps', 0) == 0 else 0
            await self.bot.db.execute(
                "UPDATE servers SET anti_caps = ? WHERE server_id = ?",
                (yeni, str(ctx.guild.id))
            )
            await ctx.send(f"Anti-caps {'aktif' if yeni else 'pasif'}!")
        
        await self.bot.db.commit()

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='yenile')
    @commands.is_owner()
    async def yenile(self, ctx, cog: str = None):
        if cog:
            try:
                await self.bot.reload_extension(f"cogs.{cog}")
                await ctx.send(f"{cog} yenilendi!")
            except Exception as e:
                await ctx.send(f"Hata: {e}")
        else:
            cogs = ['moderation', 'economy', 'fun', 'utility', 'leveling']
            for c in cogs:
                try:
                    await self.bot.reload_extension(f"cogs.{c}")
                except:
                    pass
            await ctx.send("Tum cogs yenilendi!")
    
    @commands.command(name='stats')
    @commands.is_owner()
    async def stats(self, ctx):
        embed = discord.Embed(
            title="Bot Istatistikleri",
            color=discord.Color.blue()
        )
        embed.add_field(name="Sunucu", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Kullanici", value=str(sum(g.member_count for g in self.bot.guilds)), inline=True)
        embed.add_field(name="Kanal", value=str(len(self.bot.channels)), inline=True)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='sunucular')
    @commands.is_owner()
    async def sunucular(self, ctx):
        if not self.bot.guilds:
            await ctx.send("Sunucu yok!")
            return
        
        embed = discord.Embed(
            title="Sunucular",
            color=discord.Color.blue()
        )
        
        for g in self.bot.guilds[:10]:
            embed.add_field(name=g.name, value=f"Uye: {g.member_count}", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='eval')
    @commands.is_owner()
    async def eval(self, ctx, *, code: str = None):
        if not code:
            await ctx.send("Kod belirt!")
            return
        
        try:
            result = eval(code)
            await ctx.send(f"```\n{result}\n```")
        except Exception as e:
            await ctx.send(f"Hata: {e}")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
    await bot.add_cog(Giveaways(bot))
    await bot.add_cog(Welcome(bot))
    await bot.add_cog(AutoMod(bot))
    await bot.add_cog(Owner(bot))
