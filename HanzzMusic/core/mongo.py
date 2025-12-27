# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
SQLite-backed storage wrapper to replace MongoDB usage.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

import aiosqlite

import config
from ..logging import LOGGER

_DB_LOCK = asyncio.Lock()
_DB_CONN: Optional[aiosqlite.Connection] = None


def _ensure_parent_dir(path: str) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


async def _get_conn() -> aiosqlite.Connection:
    global _DB_CONN
    if _DB_CONN is None:
        async with _DB_LOCK:
            if _DB_CONN is None:
                db_path = config.SQLITE_DB_PATH
                _ensure_parent_dir(db_path)
                _DB_CONN = await aiosqlite.connect(db_path)
                await _DB_CONN.execute("PRAGMA journal_mode=WAL;")
                await _DB_CONN.execute("PRAGMA synchronous=NORMAL;")
                await _DB_CONN.execute("PRAGMA foreign_keys=ON;")
                await _DB_CONN.commit()
                LOGGER(__name__).info("SQLite database initialized at %s", db_path)
    return _DB_CONN


def _matches(doc: Dict[str, Any], query: Optional[Dict[str, Any]]) -> bool:
    if not query:
        return True
    for key, expected in query.items():
        if isinstance(expected, dict):
            actual = doc.get(key)
            for op, value in expected.items():
                try:
                    if op == "$gt":
                        if actual is None or actual <= value:
                            return False
                    elif op == "$lt":
                        if actual is None or actual >= value:
                            return False
                    elif op == "$gte":
                        if actual is None or actual < value:
                            return False
                    elif op == "$lte":
                        if actual is None or actual > value:
                            return False
                    else:
                        return False
                except TypeError:
                    return False
        else:
            if doc.get(key) != expected:
                return False
    return True


def _apply_update(doc: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    if "$set" in update:
        doc.update(update["$set"])
        return doc
    doc.update(update)
    return doc


class SQLiteCursor:
    def __init__(self, collection: "SQLiteCollection", query: Dict[str, Any]):
        self._collection = collection
        self._query = query
        self._docs: Optional[List[Dict[str, Any]]] = None
        self._index = 0

    async def _load(self) -> None:
        if self._docs is None:
            self._docs = await self._collection._find_docs(self._query)

    async def to_list(self, length: Optional[int] = None) -> List[Dict[str, Any]]:
        await self._load()
        docs = self._docs or []
        if length is None:
            return list(docs)
        return list(docs)[:length]

    def __aiter__(self):
        return self

    async def __anext__(self) -> Dict[str, Any]:
        await self._load()
        if not self._docs or self._index >= len(self._docs):
            raise StopAsyncIteration
        doc = self._docs[self._index]
        self._index += 1
        return doc


class SQLiteCollection:
    def __init__(self, name: str):
        self._name = name

    async def _ensure_table(self, conn: aiosqlite.Connection) -> None:
        await conn.execute(
            f'CREATE TABLE IF NOT EXISTS "{self._name}" '
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, doc TEXT NOT NULL)"
        )
        await conn.commit()

    async def _fetch_rows(self, conn: aiosqlite.Connection) -> List[Dict[str, Any]]:
        await self._ensure_table(conn)
        async with conn.execute(f'SELECT id, doc FROM "{self._name}"') as cursor:
            rows = await cursor.fetchall()
        results = []
        for row_id, doc_text in rows:
            try:
                doc = json.loads(doc_text)
            except Exception:
                continue
            results.append({"_row_id": row_id, "doc": doc})
        return results

    async def _find_docs(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        conn = await _get_conn()
        rows = await self._fetch_rows(conn)
        matched = []
        for row in rows:
            doc = row["doc"]
            if _matches(doc, query):
                matched.append(doc)
        return matched

    def find(self, query: Dict[str, Any]) -> SQLiteCursor:
        return SQLiteCursor(self, query)

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        conn = await _get_conn()
        rows = await self._fetch_rows(conn)
        for row in rows:
            doc = row["doc"]
            if _matches(doc, query):
                return doc
        return None

    async def insert_one(self, document: Dict[str, Any]) -> bool:
        conn = await _get_conn()
        await self._ensure_table(conn)
        await conn.execute(
            f'INSERT INTO "{self._name}" (doc) VALUES (?)',
            (json.dumps(document),),
        )
        await conn.commit()
        return True

    async def delete_one(self, query: Dict[str, Any]) -> bool:
        conn = await _get_conn()
        rows = await self._fetch_rows(conn)
        for row in rows:
            doc = row["doc"]
            if _matches(doc, query):
                await conn.execute(
                    f'DELETE FROM "{self._name}" WHERE id = ?',
                    (row["_row_id"],),
                )
                await conn.commit()
                return True
        return False

    async def update_one(
        self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False
    ) -> bool:
        conn = await _get_conn()
        rows = await self._fetch_rows(conn)
        for row in rows:
            doc = row["doc"]
            if _matches(doc, query):
                doc = _apply_update(doc, update)
                await conn.execute(
                    f'UPDATE "{self._name}" SET doc = ? WHERE id = ?',
                    (json.dumps(doc), row["_row_id"]),
                )
                await conn.commit()
                return True
        if upsert:
            new_doc: Dict[str, Any] = {}
            for key, value in query.items():
                if isinstance(value, dict):
                    continue
                new_doc[key] = value
            new_doc = _apply_update(new_doc, update)
            await self.insert_one(new_doc)
            return True
        return False


class SQLiteDatabase:
    def __init__(self, path: str):
        self._path = path
        self._collections: Dict[str, SQLiteCollection] = {}

    def __getattr__(self, name: str) -> SQLiteCollection:
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._collections:
            self._collections[name] = SQLiteCollection(name)
        return self._collections[name]

    async def command(self, command_name: str) -> Dict[str, Any]:
        if command_name != "dbstats":
            return {}
        conn = await _get_conn()
        async with conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'"
        ) as cursor:
            tables = [row[0] for row in await cursor.fetchall()]
        objects = 0
        data_size = 0
        for table in tables:
            async with conn.execute(f'SELECT doc FROM "{table}"') as cursor:
                rows = await cursor.fetchall()
            objects += len(rows)
            for row in rows:
                if row and row[0]:
                    data_size += len(row[0].encode("utf-8"))
        storage_size = 0
        try:
            storage_size = os.path.getsize(self._path)
        except OSError:
            storage_size = 0
        return {
            "dataSize": data_size,
            "storageSize": storage_size,
            "objects": objects,
            "collections": len(tables),
        }


mongodb = SQLiteDatabase(config.SQLITE_DB_PATH)
