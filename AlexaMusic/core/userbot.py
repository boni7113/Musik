# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

import sys
from pyrogram import Client
import config
from ..logging import LOGGER

assistantids = []

class Userbot(Client):
    def __init__(self):
        super().__init__(
            name="AlexaOne",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistant Client...")
        if not config.STRING1:
            LOGGER(__name__).error("No session string (STRING1) provided in config.")
            sys.exit()

        await super().start()
        try:
            await self.join_chat("jsisjsjskw")  # Ganti/isi channel yang diinginkan, atau hapus baris ini jika tidak perlu
        except Exception:
            pass

        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                "ᴀssɪsᴛᴀɴᴛ sᴛᴀʀᴛᴇᴅ, ɴᴏᴡ ɪᴛ's ᴛɪᴍᴇ ᴛᴏ ᴇɴᴊᴏʏ ᴍᴜsɪᴄ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏᴄʜᴀᴛs.",
            )
        except Exception:
            LOGGER(__name__).error(
                f"Assistant account failed to access the log group. "
                "Make sure that you have added your assistant to your log group and promoted as admin!"
            )
            sys.exit()

        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        assistantids.append(get_me.id)
        self.name = f"{get_me.first_name} {get_me.last_name}" if get_me.last_name else get_me.first_name
        LOGGER(__name__).info(f"Assistant Started as {self.name}")
