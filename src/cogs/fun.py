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


def setup(bot: Vortex) -> None:
    print("Fun cog loaded.")
    bot.add_cog(Fun(bot))
