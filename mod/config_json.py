from typing import Dict, Any, Union
from os import getenv,chdir,getcwd

import orjson as json
import aiofiles
import asyncio
import secrets


class Config:
    @property
    def get_webhook(self):
        return self.webhook

    js: Dict[str, Any]

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        loop.run_until_complete(self.load_config())
        self.bot_token: str = getenv("virustotal_bot_token")
        self.virus_total_token: str = getenv("virustotal_token")
        self.webhook: Dict[str, Union[str, int]] = self.js["webhook"]
        self.server: Dict[str, Union[str, int]] = self.js["server"]
        self.webook_url = f"{self.webhook['host']}/{secrets.token_urlsafe()}"

    @property
    def get_bot_token(self) -> str:
        return self.bot_token

    @property
    def get_virus_total_token(self) -> str:
        return self.virus_total_token

    @property
    def get_server(self) -> Dict[str, Union[str, int]]:
        return self.server

    @property
    def get_webhook_config(self) -> Dict[str, Union[str, int]] :
        return self.webhook

    @property
    def get_webhook_url(self):
        return self.webook_url

    async def load_config(self):
        async with aiofiles.open(f"{getcwd()}/mod/config/config.json", "rb") as f:
            self.js = json.loads(await f.read())



