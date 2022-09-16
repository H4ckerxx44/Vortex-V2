import logging
import os
import datetime
import time
from typing import Optional

import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot


class Vortex(Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=os.getenv("BOT_PREFIX"),
            case_insensitive=True,
            intents=nextcord.Intents.all(),
            strip_after_prefix=True,
        )
        self.aiohttp_session: Optional[aiohttp.ClientSession] = None
        self.icon = "https://cdn.discordapp.com/avatars/926513310642339891/36f01c4d80398bccdcf1ac094e6af7c4.png?size=1024"
        self.NASA_API_KEY = os.getenv("NASA_API_KEY")
        self.WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
        self.duration_types = {"s": 1, "m": 60, "h": 3600, "d": 86_400, "w": 604_800, "y": 31_536_000}
        self.aiohttp_session: Optional[aiohttp.ClientSession] = None
        self.token: Optional[str] = os.getenv("BOT_TOKEN")
        self.version: Optional[str] = os.getenv("BOT_VERSION")
        self.start_time = time.time()
        self.major_version = os.getenv("BOT_MAJOR_VERSION")
        self.minor_version = os.getenv("BOT_MINOR_VERSION")
        self.patch_version = os.getenv("BOT_PATCH_VERSION")
        self.main_color: int = 0xFFFFFF
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("BOT_PREFIX")), intents=nextcord.Intents().all(), owner_id=int(os.getenv("BOT_OWNER_ID"))
        )

    def get_uptime(self) -> datetime.timedelta:
        difference = int(time.time() - self.start_time)
        uptime = datetime.timedelta(seconds=difference)
        return uptime

    def load_dir(self, directory) -> None:
        files = [file[:-3] for file in os.listdir(directory) if not file.startswith("__")]
        for file in files:
            ext = f"{directory}.{file}"
            self.load_extension(ext)
            logging.info(f"{ext} loaded successfully")

    def load_cogs(self) -> None:
        self.load_dir("cogs")
        self.load_extension("jishaku")
        logging.info("loading extensions finished")

    def load_tasks(self) -> None:
        self.load_dir("tasks")
        logging.info("loading tasks finished")

    async def register_aiohttp_session(self) -> None:
        self.aiohttp_session = aiohttp.ClientSession()

    def run_bot(self) -> None:
        logging.info("starting up...")
        self.loop.create_task(self.register_aiohttp_session())
        self.load_cogs()
        self.load_tasks()
        super().run(self.token)

    # Events
    async def on_ready(self) -> None:
        logging.info(f"ready as {self.user} / {self.user.id}")

    async def catdog(self, url):
        async with self.aiohttp_session.get(url) as r:
            if r.status == 200:
                response = await r.json()
        return response[0].get("url")
