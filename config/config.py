# Copyright (C) 2021-2022 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
Alexa is a Telegram Audio and video streaming bot
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want.
"""

import re
import sys
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


def _env(name: str, default=None):
    value = getenv(name, default)
    if value is None or value == "":
        return default
    return value


def _env_int(name: str, default=None, required: bool = False):
    raw = getenv(name)
    if raw is None or raw == "":
        if required:
            print(f"[ERROR] - {name} is missing. Please set it in your environment.")
            sys.exit()
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"[ERROR] - {name} must be an integer.")
        sys.exit()

API_ID = _env_int("API_ID", required=True)
API_HASH = _env("API_HASH")

BOT_TOKEN = _env("BOT_TOKEN")

MONGO_DB_URI = _env("MONGO_DB_URI", None)
SQLITE_DB_PATH = _env("SQLITE_DB_PATH", "data/alexa.sqlite3")

DURATION_LIMIT_MIN = _env_int("DURATION_LIMIT", 900)

SONG_DOWNLOAD_DURATION = _env_int("SONG_DOWNLOAD_DURATION_LIMIT", 180)

LOG_GROUP_ID = _env_int("LOG_GROUP_ID", required=True)

MUSIC_BOT_NAME = _env("MUSIC_BOT_NAME", "Hanzz")

OWNER_ID = _env_int("OWNER_ID", required=True)

if not API_HASH:
    print("[ERROR] - API_HASH is missing. Please set it in your environment.")
    sys.exit()

if not BOT_TOKEN:
    print("[ERROR] - BOT_TOKEN is missing. Please set it in your environment.")
    sys.exit()

HEROKU_API_KEY = _env("HEROKU_API_KEY")

BOT_ID = _env("BOT_ID")

HEROKU_APP_NAME = _env("HEROKU_APP_NAME")

UPSTREAM_REPO = _env("UPSTREAM_REPO", "https://github.com/boni7113/Musik")

UPSTREAM_BRANCH = _env("UPSTREAM_BRANCH", "master")

GIT_TOKEN = _env("GIT_TOKEN", None)

SUPPORT_CHANNEL = _env("SUPPORT_CHANNEL", "")

SUPPORT_GROUP = _env("SUPPORT_GROUP", "")

AUTO_LEAVING_ASSISTANT = _env("AUTO_LEAVING_ASSISTANT", "False")

AUTO_LEAVE_ASSISTANT_TIME = _env_int("ASSISTANT_LEAVE_TIME", 11500)

AUTO_SUGGESTION_TIME = _env_int("AUTO_SUGGESTION_TIME", 5400)

AUTO_DOWNLOADS_CLEAR = _env("AUTO_DOWNLOADS_CLEAR", "True")

AUTO_SUGGESTION_MODE = _env("AUTO_SUGGESTION_MODE", "False")

PRIVATE_BOT_MODE = _env("PRIVATE_BOT_MODE", None)

YOUTUBE_DOWNLOAD_EDIT_SLEEP = _env_int("YOUTUBE_EDIT_SLEEP", 3)

TELEGRAM_DOWNLOAD_EDIT_SLEEP = _env_int("TELEGRAM_EDIT_SLEEP", 5)

GITHUB_REPO = _env("GITHUB_REPO", "https://github.com/boni7113/Musik")

SPOTIFY_CLIENT_ID = _env("SPOTIFY_CLIENT_ID", None)

SPOTIFY_CLIENT_SECRET = _env("SPOTIFY_CLIENT_SECRET", None)

VIDEO_STREAM_LIMIT = _env_int("VIDEO_STREAM_LIMIT", 2)

SERVER_PLAYLIST_LIMIT = _env_int("SERVER_PLAYLIST_LIMIT", 50)

PLAYLIST_FETCH_LIMIT = _env_int("PLAYLIST_FETCH_LIMIT", 50)

CLEANMODE_DELETE_MINS = _env_int("CLEANMODE_MINS", 7)

TG_AUDIO_FILESIZE_LIMIT = _env_int("TG_AUDIO_FILESIZE_LIMIT", 104857600)

TG_VIDEO_FILESIZE_LIMIT = _env_int("TG_VIDEO_FILESIZE_LIMIT", 1073741824)
# https://www.gbmb.org/mb-to-bytes

COOKIES = _env("COOKIES", None)
# https://batbin.me

STRING1 = _env("STRING_SESSION", None)
STRING2 = _env("STRING_SESSION2", None)
STRING3 = _env("STRING_SESSION3", None)
STRING4 = _env("STRING_SESSION4", None)
STRING5 = _env("STRING_SESSION5", None)

BANNED_USERS = filters.user()
YTDOWNLOADER = 1
LOG = 2
LOG_FILE_NAME = "logs.txt"
adminlist = {}
lyrical = {}
chatstats = {}
userstats = {}
clean = {}

autoclean = []

START_IMG_URL = _env(
    "START_IMG_URL", "https://telegra.ph/file/d593c6064ff7657d0c714.jpg"
)

PING_IMG_URL = _env(
    "PING_IMG_URL",
    "assets/Ping.jpeg",
)

PLAYLIST_IMG_URL = _env(
    "PLAYLIST_IMG_URL",
    "assets/Playlist.jpeg",
)

GLOBAL_IMG_URL = _env(
    "GLOBAL_IMG_URL",
    "assets/Global.jpeg",
)

STATS_IMG_URL = _env(
    "STATS_IMG_URL",
    "assets/Stats.jpeg",
)

TELEGRAM_AUDIO_URL = _env(
    "TELEGRAM_AUDIO_URL",
    "assets/Audio.jpeg",
)

TELEGRAM_VIDEO_URL = _env(
    "TELEGRAM_VIDEO_URL",
    "assets/Video.jpeg",
)

STREAM_IMG_URL = _env(
    "STREAM_IMG_URL",
    "assets/Stream.jpeg",
)

SOUNCLOUD_IMG_URL = _env(
    "SOUNCLOUD_IMG_URL",
    "assets/Soundcloud.jpeg",
)

YOUTUBE_IMG_URL = _env(
    "YOUTUBE_IMG_URL",
    "assets/Youtube.jpeg",
)

SPOTIFY_ARTIST_IMG_URL = _env(
    "SPOTIFY_ARTIST_IMG_URL",
    "assets/SpotifyArtist.jpeg",
)

SPOTIFY_ALBUM_IMG_URL = _env(
    "SPOTIFY_ALBUM_IMG_URL",
    "assets/SpotifyAlbum.jpeg",
)

SPOTIFY_PLAYLIST_IMG_URL = _env(
    "SPOTIFY_PLAYLIST_IMG_URL",
    "assets/SpotifyPlaylist.jpeg",
)


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    print(
        "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()

if SUPPORT_GROUP and not re.match("(?:http|https)://", SUPPORT_GROUP):
    print(
        "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()

if UPSTREAM_REPO and not re.match("(?:http|https)://", UPSTREAM_REPO):
    print(
        "[ERROR] - Your UPSTREAM_REPO url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()

if GITHUB_REPO and not re.match("(?:http|https)://", GITHUB_REPO):
    print(
        "[ERROR] - Your GITHUB_REPO url is wrong. Please ensure that it starts with https://"
    )


if (
    PING_IMG_URL
    and PING_IMG_URL != "assets/Ping.jpeg"
    and not re.match("(?:http|https)://", PING_IMG_URL)
):
    print(
        "[ERROR] - Your PING_IMG_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()

if (
    PLAYLIST_IMG_URL
    and PLAYLIST_IMG_URL != "assets/Playlist.jpeg"
    and not re.match("(?:http|https)://", PLAYLIST_IMG_URL)
):
    print(
        "[ERROR] - Your PLAYLIST_IMG_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()

if (
    GLOBAL_IMG_URL
    and GLOBAL_IMG_URL != "assets/Global.jpeg"
    and not re.match("(?:http|https)://", GLOBAL_IMG_URL)
):
    print(
        "[ERROR] - Your GLOBAL_IMG_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()


if STATS_IMG_URL and (
    STATS_IMG_URL != "assets/Stats.jpeg"
    and not re.match("(?:http|https)://", STATS_IMG_URL)
):
    print(
        "[ERROR] - Your STATS_IMG_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()


if (
    TELEGRAM_AUDIO_URL
    and TELEGRAM_AUDIO_URL != "assets/Audio.jpeg"
    and not re.match("(?:http|https)://", TELEGRAM_AUDIO_URL)
):
    print(
        "[ERROR] - Your TELEGRAM_AUDIO_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()


if (
    STREAM_IMG_URL
    and STREAM_IMG_URL != "assets/Stream.jpeg"
    and not re.match("(?:http|https)://", STREAM_IMG_URL)
):
    print(
        "[ERROR] - Your STREAM_IMG_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()


if (
    SOUNCLOUD_IMG_URL
    and SOUNCLOUD_IMG_URL != "assets/Soundcloud.jpeg"
    and not re.match("(?:http|https)://", SOUNCLOUD_IMG_URL)
):
    print(
        "[ERROR] - Your SOUNCLOUD_IMG_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()

if (
    YOUTUBE_IMG_URL
    and YOUTUBE_IMG_URL != "assets/Youtube.jpeg"
    and not re.match("(?:http|https)://", YOUTUBE_IMG_URL)
):
    print(
        "[ERROR] - Your YOUTUBE_IMG_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()


if (
    TELEGRAM_VIDEO_URL
    and TELEGRAM_VIDEO_URL != "assets/Video.jpeg"
    and not re.match("(?:http|https)://", TELEGRAM_VIDEO_URL)
):
    print(
        "[ERROR] - Your TELEGRAM_VIDEO_URL url is wrong. Please ensure that it starts with https://"
    )
    sys.exit()
