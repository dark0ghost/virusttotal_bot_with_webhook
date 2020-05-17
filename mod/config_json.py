from typing import Dict, Any, Union

import orjson as json
import aiofiles
import asyncio


class Config:
    js: Dict[str, Any]

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        loop.run_until_complete(self.load_config())
        self.bot_token: str = self.js["token"]["bot"]
        self.virus_total_token: str = self.js["token"]["virustotal"]
        self.webhookconfig: Dict[str, Union[str, int]] = self.js["webhook"]

    @property
    def get_bot_token(self) -> str:
        return self.bot_token

    @property
    def get_virus_total_token(self) -> str:
        return self.virus_total_token

    async def load_config(self):
        async with aiofiles.open("config/config.json", "rb") as f:
            self.js = json.loads(await f.read())
