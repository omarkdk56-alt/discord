import discord
from discord.ext import commands
import asyncio

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='seviye-goster')
    async def seviye(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        cursor = await self.bot.db.execute(
            "SELECT * FROM levels WHERE server_id = ? AND user_id = ?",
            (str(ctx.guild.id), str(member.id))
        )
        level_data = await cursor.fetchone()
        
        if not level_data:
            await ctx.send(f"{member} icin seviye verisi yok!")
            return
        
        xp = level_data[3]
        level = level_data[4]
        xp_gerekli = level * 100
        
        embed = discord.Embed(
            title=f"{member} Seviyesi",
            color=discord.Color.blue()
        )
        embed.add_field(name="Seviye", value=str(level), inline=True)
        embed.add_field(name="XP", value=f"{xp}/{xp_gerekli}", inline=True)
        embed.add_field(name="Mesaj", value=str(level_data[5]), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='siralama')
    @commands.guild_only()
    async def siralama(self, ctx):
        cursor = await self.bot.db.execute(
            "SELECT * FROM levels WHERE server_id = ? ORDER BY level DESC, xp DESC LIMIT 10",
            (str(ctx.guild.id),)
        )
        data = await cursor.fetchall()
        
        if not data:
            await ctx.send("Veri yok!")
            return
        
        embed = discord.Embed(
            title=f"🏆 {ctx.guild.name} Seviye Siralamasi",
            color=discord.Color.gold()
        )
        
        for i, d in enumerate(data, 1):
            user = self.bot.get_user(int(d[2]))
            name = user.name if user else f"ID: {d[2]}"
            embed.add_field(
                name=f"#{i} {name}",
                value=f"Seviye: {d[4]} | XP: {d[3]}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='xp')
    async def xp(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        cursor = await self.bot.db.execute(
            "SELECT * FROM levels WHERE server_id = ? AND user_id = ?",
            (str(ctx.guild.id), str(member.id))
        )
        level_data = await cursor.fetchone()
        
        if not level_data:
            await ctx.send(f"{member} icin XP verisi yok!")
            return
        
        embed = discord.Embed(
            title=f"{member} XP",
            description=f"Toplam XP: **{level_data[3]}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='setxp')
    @commands.has_permissions(administrator=True)
    async def setxp(self, ctx, member: discord.Member, xp: int):
        cursor = await self.bot.db.execute(
            "SELECT * FROM levels WHERE server_id = ? AND user_id = ?",
            (str(ctx.guild.id), str(member.id))
        )
        level_data = await cursor.fetchone()
        
        if level_data:
            await self.bot.db.execute(
                "UPDATE levels SET xp = ? WHERE server_id = ? AND user_id = ?",
                (xp, str(ctx.guild.id), str(member.id))
            )
        else:
            await self.bot.db.execute(
                "INSERT INTO levels (server_id, user_id, xp, level) VALUES (?, ?, ?, ?)",
                (str(ctx.guild.id), str(member.id), xp, 1)
            )
        
        await self.bot.db.commit()
        await ctx.send(f"{member} XP: {xp} olarak degistirildi!")
    
    @commands.command(name='setlevel')
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx, member: discord.Member, level: int):
        cursor = await self.bot.db.execute(
            "SELECT * FROM levels WHERE server_id = ? AND user_id = ?",
            (str(ctx.guild.id), str(member.id))
        )
        level_data = await cursor.fetchone()
        
        if level_data:
            await self.bot.db.execute(
                "UPDATE levels SET level = ? WHERE server_id = ? AND user_id = ?",
                (level, str(ctx.guild.id), str(member.id))
            )
        else:
            await self.bot.db.execute(
                "INSERT INTO levels (server_id, user_id, level, xp) VALUES (?, ?, ?, ?)",
                (str(ctx.guild.id), str(member.id), level, 0)
            )
        
        await self.bot.db.commit()
        await ctx.send(f"{member} Seviye: {level} olarak degistirildi!")

async def setup(bot):
    await bot.add_cog(Leveling(bot))
