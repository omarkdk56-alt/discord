import discord
from discord.ext import commands
import asyncio
from typing import List, Union
import math

class PaginationView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed], ctx: commands.Context, timeout: float = 120):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.ctx = ctx
        self.current_page = 0
        self.total_pages = len(embeds)
        
        self.prev_button.disabled = True
        if self.total_pages == 1:
            self.next_button.disabled = True
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            await self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.message.delete()
    
    async def update_buttons(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.total_pages - 1

class SimplePagination:
    def __init__(self, bot):
        self.bot = bot
    
    async def paginate(self, ctx: commands.Context, content: List[str], title: str = None, color: discord.Color = None, timeout: float = 120):
        if not content:
            return await ctx.send("Gosterilecek icerik yok!")
        
        if len(content) == 1:
            embed = discord.Embed(title=title, description=content[0], color=color or discord.Color.blue())
            return await ctx.send(embed=embed)
        
        items_per_page = 10
        pages = []
        total_pages = math.ceil(len(content) / items_per_page)
        
        for i in range(0, len(content), items_per_page):
            page_content = "\n".join(content[i:i + items_per_page])
            embed = discord.Embed(
                title=title or "Liste",
                description=page_content,
                color=color or discord.Color.blue()
            )
            embed.set_footer(text=f"Sayfa {len(pages) + 1}/{total_pages}")
            pages.append(embed)
        
        view = PaginationView(pages, ctx, timeout)
        await ctx.send(embed=pages[0], view=view)
        return view
    
    async def paginate_fields(self, ctx: commands.Context, fields: List[dict], title: str = None, color: discord.Color = None, items_per_page: int = 10, timeout: float = 120):
        if not fields:
            return await ctx.send("Gosterilecek icerik yok!")
        
        pages = []
        total_pages = math.ceil(len(fields) / items_per_page)
        
        for page_num in range(total_pages):
            embed = discord.Embed(
                title=title or "Liste",
                color=color or discord.Color.blue()
            )
            start = page_num * items_per_page
            end = start + items_per_page
            
            for field in fields[start:end]:
                embed.add_field(
                    name=field.get("name", "\u200b"),
                    value=field.get("value", "\u200b"),
                    inline=field.get("inline", False)
                )
            
            embed.set_footer(text=f"Sayfa {page_num + 1}/{total_pages}")
            pages.append(embed)
        
        view = PaginationView(pages, ctx, timeout)
        await ctx.send(embed=pages[0], view=view)
        return view
    
    async def send_long_message(self, ctx: commands.Context, content: str, title: str = None, color: discord.Color = None, max_chars: int = 2000):
        if len(content) <= max_chars:
            embed = discord.Embed(title=title, description=content, color=color or discord.Color.blue())
            return await ctx.send(embed=embed)
        
        lines = content.split("\n")
        pages = []
        current_page = ""
        
        for line in lines:
            if len(current_page) + len(line) + 1 <= max_chars:
                current_page += line + "\n"
            else:
                if current_page:
                    pages.append(current_page)
                current_page = line + "\n"
        
        if current_page:
            pages.append(current_page)
        
        embeds = []
        for i, page_content in enumerate(pages):
            embed = discord.Embed(
                title=f"{title} - Sayfa {i+1}/{len(pages)}" if title else f"Sayfa {i+1}/{len(pages)}",
                description=page_content,
                color=color or discord.Color.blue()
            )
            embeds.append(embed)
        
        view = PaginationView(embeds, ctx)
        await ctx.send(embed=embeds[0], view=view)
        return view

class ConfirmView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: float = 30):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.result = None
    
    @discord.ui.button(label="✅ Evet", style=discord.ButtonStyle.success)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.result = True
        self.stop()
        await interaction.message.delete()
    
    @discord.ui.button(label="❌ Hayır", style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.result = False
        self.stop()
        await interaction.message.delete()

class DropdownView(discord.ui.View):
    def __init__(self, options: List[dict], ctx: commands.Context, timeout: float = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.result = None
        
        dropdown = discord.ui.Select(
            placeholder="Seceneklerden birini secin...",
            options=[
                discord.SelectOption(label=opt["label"], value=opt["value"], description=opt.get("description"))
                for opt in options
            ]
        )
        
        async def callback(interaction: discord.Interaction):
            self.result = dropdown.values[0]
            self.stop()
            await interaction.message.delete()
        
        dropdown.callback = callback
        self.add_item(dropdown)

class ButtonView(discord.ui.View):
    def __init__(self, buttons: List[dict], ctx: commands.Context, timeout: float = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.result = None
        
        for btn in buttons:
            button = discord.ui.Button(
                label=btn["label"],
                style=discord.ButtonStyle[btn.get("style", "primary")],
                custom_id=btn.get("custom_id", btn["label"])
            )
            
            async def button_callback(interaction: discord.Interaction, btn=btn):
                self.result = btn.get("label")
                self.stop()
                await interaction.message.delete()
            
            button.callback = button_callback
            self.add_item(button)

async def confirm(ctx: commands.Context, message: str, timeout: float = 30) -> bool:
    embed = discord.Embed(title="Onay", description=message, color=discord.Color.yellow())
    view = ConfirmView(ctx, timeout)
    msg = await ctx.send(embed=embed, view=view)
    
    await view.wait()
    return view.result

async def select_option(ctx: commands.Context, options: List[dict], title: str = "Secenekler") -> str:
    embed = discord.Embed(title=title, description="Asagidaki seceneklerden birini secin:", color=discord.Color.blue())
    view = DropdownView(options, ctx)
    msg = await ctx.send(embed=embed, view=view)
    
    await view.wait()
    return view.result

async def show_buttons(ctx: commands.Context, buttons: List[dict], title: str = "Secenekler") -> str:
    embed = discord.Embed(title=title, description="Asagidaki butonlardan birini secin:", color=discord.Color.blue())
    view = ButtonView(buttons, ctx)
    msg = await ctx.send(embed=embed, view=view)
    
    await view.wait()
    return view.result
