from datetime import datetime
from time import time

import nextcord
from nextcord import Member, Embed, Spotify
from nextcord.ext.commands import Cog, command, Context

from src.utility import util
from src.utility.bot import Vortex


class General(Cog, description="General commands of the bot."):
    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot

    async def determine_party_host(self, member, activity):
        idd = int(activity.party_id.split(":")[1])
        if idd != member.id:
            usr = await self.bot.fetch_user(idd)
            party = str(usr)
        else:
            party = "Not in a party"
        return party

    @command(name="ping", help="Displays bot latency in ms.")
    async def ping(self, ctx: Context):
        start = time()
        message = await ctx.send(f"DWSP latency: {self.bot.latency * 1000:,.0f}ms")
        end = time()
        await message.edit(content=f"DWSP latency: {self.bot.latency * 1000:,.0f}ms || Response time: {(end - start) * 1000:,.0f}ms")

    @command(name="userinfo", aliases=["ui"], brief="Shows a bunch of stuff about a user.")
    async def userinfo(self, ctx: Context, member: Member = None):
        member = member or ctx.author
        joined_days_ago = (datetime.today().replace(tzinfo=member.joined_at.tzinfo) - member.joined_at).days
        created_days_ago = (datetime.today().replace(tzinfo=member.joined_at.tzinfo) - member.created_at).days
        booster = member.premium_since.strftime("%H:%M:%S, %d.%m.%Y") if member.premium_since else "No boosts."
        nick = member.nick or "No custom nickname"

        colors = {"online": nextcord.Color.green(),
                  "idle": nextcord.Color.yellow(),
                  "dnd": nextcord.Color.red(),
                  "do_not_disturb": nextcord.Color.red(),
                  "offline": 0x696969,
                  "invisible": 0x696969
                  }

        userinfo = Embed(title=f"{member} || {member.id}", description=f"Avatar URL: {member.avatar.with_size(4096).url}", color=colors.get(member.raw_status))
        userinfo.set_thumbnail(url=member.avatar.with_size(4096).url)
        user = await self.bot.fetch_user(member.id)
        if user.banner:
            userinfo.set_image(user.banner.with_size(4096).url)
        userinfo.add_field(
            name="General",
            value=f"```Name: {member}\n"
            f"Status: {member.status} | Mobile: {member.is_on_mobile()}\n"
            f"Bot: {member.bot}\n"
            f"Joined Discord: {member.created_at.strftime('%H:%M:%S, %d.%m.%Y')} ({created_days_ago} days ago)\n```",
            inline=False,
        )
        userinfo.add_field(
            name="Server specific",
            value=f"```Nickname: {nick}\n"
            f"Boosting since: {booster}\n"
            f"Top Role: {member.top_role} (Color code: {member.top_role.color})\n"
            f"Joined server: {member.joined_at.strftime('%H:%M:%S, %d.%m.%Y')} ({joined_days_ago} days ago.)```",
            inline=False,
        )
        userinfo.add_field(name=f"Roles [{len(member.roles) - 1}]", value=" ".join([role.mention for role in member.roles[1:]]))
        if member.voice:
            userinfo.add_field(
                name="Voice activity",
                value=f"```Current channel: {member.voice.channel.name}\n"
                f"Bitrate: {member.voice.channel.bitrate / 1000}kbit/s\n"
                f"User limit: {member.voice.channel.user_limit}\n"
                f"Streams: {member.voice.self_stream}\n"
                f"Video: {member.voice.self_video}"
                f"Muted: {member.voice.self_mute}\n"
                f"Deafened: {member.voice.self_deaf}\n"
                f"AFK: {member.voice.afk}```",
                inline=False,
            )
        for activity in member.activities:
            if isinstance(activity, Spotify):
                party = await self.determine_party_host(member, activity)
                artists = ", ".join(activity.artists)
                userinfo.add_field(
                    name="Spotify",
                    value=f"```Song: {activity.title} - {artists} | ({activity.album})\n"
                    f"Duration: {activity.duration}\n"
                    f"Party-Host: {party}\n"
                    f"Track ID: spotify:track:{activity.track_id}```",
                    inline=False,
                )

        userinfo.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.with_size(4096).url)
        await ctx.send(embed=userinfo)

    @command(name="spotify", brief="Share what you are currently listening too on spotify.")
    async def spotify(self, ctx: Context, member: Member = None):
        member = member or ctx.author
        for activity in member.activities:
            if isinstance(activity, Spotify):
                party = await self.determine_party_host(member, activity)
                artists = ", ".join(artist for artist in activity.artists)
                spotify = Embed(
                    title=f"{activity.title} - {artists}",
                    description=f"from the album **{activity.album}**",
                    url=activity.track_url,
                    color=nextcord.Color.green(),
                )
                spotify.set_thumbnail(url=activity.album_cover_url)
                spotify.add_field(name="Duration", value=str(activity.duration).split(".")[0], inline=True)
                spotify.add_field(name="Party", value=party, inline=True)
                spotify.set_footer(text=f"Track: {activity.track_url}")
                await ctx.send(embed=spotify)

    @command(name="apod", brief="Astronomy picture of the day")
    async def apod(self, ctx: Context):
        base_url = "https://api.nasa.gov/planetary/apod"
        params = {"api_key": self.bot.NASA_API_KEY}
        async with self.bot.aiohttp_session.get(base_url, params=params) as r:
            if r.status == 200:
                data = await r.json()
            else:
                return await ctx.send(f"Fetching {base_url} failed.")

        if data:
            apod_embed = Embed(title=data.get("title"), description=data.get("explanation"), color=self.bot.main_color)

            author = f"Credits: {data.get('copyright', 'No credit found')}"
            apod_embed.set_footer(text=f"{author} | {util.format_date_from_string(data.get('date'))}")

            if data.get("media_type") == "image":
                apod_embed.url = data.get("hdurl")
                apod_embed.set_image(url=data["hdurl"])

                await ctx.send(embed=apod_embed)
            elif data.get("media_type") == "video":
                # https://www.youtube.com/embed/ts0Ek3nLHew?rel=0 --> https://www.youtube.com/watch?v=ts0Ek3nLHew
                url: str = data.get("url").replace("?rel=0", "").replace("embed/", "watch?v=")

                # https://www.youtube.com/embed/ts0Ek3nLHew
                # url = url.replace("?rel=0", "")

                # https://www.youtube.com/watch?v=ts0Ek3nLHew
                # url = url.replace("embed/", "watch?v=")

                apod_embed.url = url

                await ctx.send(url)
                await ctx.send(embed=apod_embed)
            else:
                await ctx.send(f"Unsupported media_type ({data.get('media_type')}), click link to see which data is present\n" f"<{base_url}?api_key=DEMO_KEY>")


def setup(bot: Vortex) -> None:
    print("General cog loaded.")
    bot.add_cog(General(bot))
