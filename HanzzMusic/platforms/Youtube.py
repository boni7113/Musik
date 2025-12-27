# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""

import asyncio
import os
import re
import json
from typing import Any, Dict, Union

from yt_dlp import YoutubeDL
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

import config
from HanzzMusic import LOGGER
from HanzzMusic.utils.database import is_on_off
from HanzzMusic.utils.formatters import seconds_to_min, time_to_seconds


def cookiefile():
    cookie_dir = "cookies"
    if not os.path.isdir(cookie_dir):
        return None
    for name in os.listdir(cookie_dir):
        if name.endswith(".txt"):
            return os.path.join(cookie_dir, name)
    return None


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def _ydl_opts(self) -> Dict[str, Any]:
        opts = {"quiet": True, "skip_download": True}
        cookie_path = cookiefile()
        if cookie_path:
            opts["cookiefile"] = cookie_path
        return opts

    async def _ydl_info(self, query: str, limit: int = 1) -> Dict[str, Any]:
        is_url = bool(re.search(self.regex, query))
        target = query if is_url else f"ytsearch{limit}:{query}"

        def _extract():
            with YoutubeDL(self._ydl_opts()) as ydl:
                return ydl.extract_info(target, download=False)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _extract)

    def _normalize_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        duration = info.get("duration")
        duration_min = None
        if duration:
            duration_min = seconds_to_min(duration)
        return {
            "title": info.get("title") or "Unknown Title",
            "duration_min": duration_min,
            "thumbnail": info.get("thumbnail"),
            "vidid": info.get("id"),
            "link": info.get("webpage_url") or info.get("original_url"),
        }

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None if offset in (None,) else text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            result_list = (await results.next()).get("result") or []
            if not result_list:
                raise ValueError("No search results")
            result = result_list[0]
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
            return title, duration_min, duration_sec, thumbnail, vidid
        except Exception as exc:
            LOGGER(__name__).warning("VideosSearch failed in details: %s", exc)
            info = await self._ydl_info(link, limit=1)
            entry = (info.get("entries") or [info])[0]
            data = self._normalize_info(entry)
            duration_sec = (
                int(time_to_seconds(data["duration_min"]))
                if data["duration_min"]
                else 0
            )
            thumbnail = data["thumbnail"] or ""
            return (
                data["title"],
                data["duration_min"],
                duration_sec,
                thumbnail,
                data["vidid"],
            )

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            result_list = (await results.next()).get("result") or []
            if not result_list:
                raise ValueError("No search results")
            return result_list[0]["title"]
        except Exception as exc:
            LOGGER(__name__).warning("VideosSearch failed in title: %s", exc)
            info = await self._ydl_info(link, limit=1)
            entry = (info.get("entries") or [info])[0]
            return self._normalize_info(entry)["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            result_list = (await results.next()).get("result") or []
            if not result_list:
                raise ValueError("No search results")
            return result_list[0]["duration"]
        except Exception as exc:
            LOGGER(__name__).warning("VideosSearch failed in duration: %s", exc)
            info = await self._ydl_info(link, limit=1)
            entry = (info.get("entries") or [info])[0]
            return self._normalize_info(entry)["duration_min"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            result_list = (await results.next()).get("result") or []
            if not result_list:
                raise ValueError("No search results")
            return result_list[0]["thumbnails"][0]["url"].split("?")[0]
        except Exception as exc:
            LOGGER(__name__).warning("VideosSearch failed in thumbnail: %s", exc)
            info = await self._ydl_info(link, limit=1)
            entry = (info.get("entries") or [info])[0]
            return self._normalize_info(entry)["thumbnail"]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        cookie_path = cookiefile()
        cmd = ["yt-dlp"]
        if cookie_path:
            cmd += ["--cookies", cookie_path]
        cmd += [
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return (1, stdout.decode().split("\n")[0]) if stdout else (0, stderr.decode())

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        cmd = (
            f"yt-dlp -i --compat-options no-youtube-unavailable-videos "
            f"--get-id --flat-playlist --playlist-end {limit} --skip-download '{link}' "
            f"2>/dev/null"
        )
        playlist = await shell_cmd(cmd)
        try:
            result = [key for key in playlist.split("\n") if key]
        except Exception:
            result = []
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            result_list = (await results.next()).get("result") or []
            if not result_list:
                raise ValueError("No search results")
            result = result_list[0]
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        except Exception as exc:
            LOGGER(__name__).warning("VideosSearch failed in track: %s", exc)
            info = await self._ydl_info(link, limit=1)
            entry = (info.get("entries") or [info])[0]
            data = self._normalize_info(entry)
            title = data["title"]
            duration_min = data["duration_min"]
            vidid = data["vidid"]
            yturl = data["link"]
            thumbnail = data["thumbnail"] or ""
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
            "cookiefile": cookiefile(),
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True}
        cookie_path = cookiefile()
        if cookie_path:
            ytdl_opts["cookiefile"] = cookie_path
        ydl = YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except Exception:
                    continue
                if "dash" not in str(format["format"]).lower():
                    try:
                        format["format"]
                        format["filesize"]
                        format["format_id"]
                        format["ext"]
                        format["format_note"]
                    except Exception:
                        continue
                    formats_available.append(
                        {
                            "format": format["format"],
                            "filesize": format["filesize"],
                            "format_id": format["format_id"],
                            "ext": format["ext"],
                            "format_note": format["format_note"],
                            "yturl": link,
                            "cookiefile": cookiefile(),
                        }
                    )
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            a = VideosSearch(link, limit=10)
            result_list = (await a.next()).get("result") or []
            if len(result_list) <= query_type:
                raise ValueError("No search results")
            title = result_list[query_type]["title"]
            duration_min = result_list[query_type]["duration"]
            vidid = result_list[query_type]["id"]
            thumbnail = result_list[query_type]["thumbnails"][0]["url"].split("?")[0]
            return title, duration_min, thumbnail, vidid
        except Exception as exc:
            LOGGER(__name__).warning("VideosSearch failed in slider: %s", exc)
            info = await self._ydl_info(link, limit=10)
            entries = info.get("entries") or []
            if len(entries) <= query_type:
                raise
            entry = entries[query_type]
            data = self._normalize_info(entry)
            return data["title"], data["duration_min"], data["thumbnail"], data["vidid"]

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            cookie_path = cookiefile()
            if cookie_path:
                ydl_optssx["cookiefile"] = cookie_path
            x = YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(best[height<=?720][width<=?1280])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            cookie_path = cookiefile()
            if cookie_path:
                ydl_optssx["cookiefile"] = cookie_path
            x = YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_video_dl():
            formats = f"{format_id}+140"
            fpath = f"downloads/{title}"
            ydl_optssx = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
            }
            cookie_path = cookiefile()
            if cookie_path:
                ydl_optssx["cookiefile"] = cookie_path
            x = YoutubeDL(ydl_optssx)
            x.download([link])

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_optssx = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
            cookie_path = cookiefile()
            if cookie_path:
                ydl_optssx["cookiefile"] = cookie_path
            x = YoutubeDL(ydl_optssx)
            x.download([link])

        if songvideo:
            await loop.run_in_executor(None, song_video_dl)
            fpath = f"downloads/{title}.mp4"
            return fpath
        elif songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            fpath = f"downloads/{title}.mp3"
            return fpath
        elif video:
            if await is_on_off(1):
                direct = True
                downloaded_file = await loop.run_in_executor(None, video_dl)
            else:
                cookie_path = cookiefile()
                cmd = ["yt-dlp"]
                if cookie_path:
                    cmd += ["--cookies", cookie_path]
                cmd += [
                    "-g",
                    "-f",
                    "best[height<=?720][width<=?1280]",
                    f"{link}",
                ]
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = None
                else:
                    return
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, direct
