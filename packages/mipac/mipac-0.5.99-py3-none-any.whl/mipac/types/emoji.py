from typing import Optional, TypedDict

__all__ = ("EmojiPayload", "ICustomEmojiLite", "ICustomEmoji")


class ICustomEmojiLiteRequired(TypedDict):
    name: str


class ICustomEmojiLite(ICustomEmojiLiteRequired, total=False):
    url: str


class ICustomEmoji(ICustomEmojiLite):
    id: str
    category: str
    aliases: list[str]
    host: str | None
    license: str | None  # v13 only


class EmojiPayload(TypedDict):
    id: str | None
    aliases: Optional[list[str]]
    name: str | None
    category: str | None
    host: str | None
    url: str | None
    license: str | None  # v13 only
