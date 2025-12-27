# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


import asyncio
import importlib
from typing import Any

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from HanzzMusic import LOGGER, app, userbot
from HanzzMusic.core.call import Alexa
from HanzzMusic.misc import sudo
from HanzzMusic.plugins import ALL_MODULES
from HanzzMusic.utils.database import get_banned_users, get_gbanned
from HanzzMusic.core.cookies import save_cookies


async def init() -> None:
    # Check for at least one valid Pyrogram string session
    if all(not getattr(config, f"STRING{i}") for i in range(1, 6)):
        LOGGER("HanzzMusic").error("Add Pyrogram string session and then try...")
        exit()
    await sudo()
    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)
        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    await save_cookies()
    for module in ALL_MODULES:
        importlib.import_module(f"HanzzMusic.plugins{module}")
    LOGGER("HanzzMusic.plugins").info("Necessary Modules Imported Successfully.")
    await userbot.start()
    await Alexa.start()
    try:
        await Alexa.stream_call("https://telegra.ph/file/b60b80ccb06f7a48f68b5.mp4")
    except NoActiveGroupCall:
        LOGGER("HanzzMusic").warning(
            "No active group call in the log group; skipping startup stream check."
        )
    except Exception:
        LOGGER("HanzzMusic").warning("Startup stream check failed.", exc_info=True)
    await Alexa.decorators()
    LOGGER("HanzzMusic").info("Hanzz Music Bot Started Successfully")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("HanzzMusic").info("Stopping Hanzz Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
    LOGGER("HanzzMusic").info("Stopping Music Bot")
