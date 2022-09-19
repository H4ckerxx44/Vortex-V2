import logging
from random import randint

from nextcord import Member, Embed
from nextcord.ext.commands import Cog, command, Context

from src.constants import CustomConstants
from src.utility.bot import Vortex


class Fun(Cog, description="Fun commands of the bot."):
    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot

    @command(name="penis", aliases=["pp", "cock", "dick"], brief="Get dick size")
    async def penis(self, ctx: Context, member: Member = None):
        member = member or ctx.author
        amount_cm = randint(0, 40)
        amount_inch = amount_cm / 2.54

        penis = Embed(
            title=f"{member.name}s dick is...", description=f"8{amount_cm * '='}D || {amount_cm} cm ({amount_inch:.3f} inch) long", color=self.bot.main_color
        )

        if amount_cm == 40:
            penis.set_footer(text="Big dick energy right here, absolute Chad.")
        elif amount_cm == 0:
            penis.set_footer(text="Take the L.")
        await ctx.send(embed=penis)

    @command(name="cat", aliases=["catto"], brief="Gives you a catto")
    async def cat(self, ctx: Context):
        cat = await self.bot.catdog(CustomConstants.CAT_URL)
        await ctx.send(str(cat))

    @command(name="dog", aliases=["doggo"], brief="Gives you a doggo")
    async def dog(self, ctx: Context):
        dog = await self.bot.catdog(CustomConstants.DOG_URL)
        await ctx.send(str(dog))

    @command(name="inspiro", brief="Generate a very deep and thought-about quote, totally not full of bullshit.")
    async def inspiro(self, ctx: Context):
        async with self.bot.aiohttp_session.get("https://inspirobot.me/api?generate=true") as r:
            if r.status == 200:
                link = await r.text()
                await ctx.send(str(link))

    @command(name="mock", brief="Mock a user.")
    async def mock(self, ctx: Context, *, msg):
        x = ""
        i = True
        for letter in msg:
            if i:
                x += letter.upper()
            else:
                x += letter.lower()
            if letter != " ":
                i = not i

        result = f"{x}, `~{ctx.author.nick if ctx.author.nick else ctx.author}`"
        if len(result) > 2000:
            return await ctx.send("This message is too long to send.")

        await ctx.send(f"{x} `~{ctx.author.nick if ctx.author.nick else ctx.author}`")
        await ctx.message.delete()


def setup(bot: Vortex) -> None:
    bot.add_cog(Fun(bot))
    logging.info(f"{Fun.__class__.__name__} cog loaded.")