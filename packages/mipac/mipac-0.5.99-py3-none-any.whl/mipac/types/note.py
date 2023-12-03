from __future__ import annotations

from typing import Any, Generic, Literal, NotRequired, Optional, TypedDict, TypeVar

from mipac.types.drive import IFile
from mipac.types.emoji import ICustomEmojiLite
from mipac.types.poll import IPoll
from mipac.types.reaction import IReactionAcceptance
from mipac.types.user import IPartialUser

T = TypeVar("T")

INoteVisibility = Literal["public", "home", "followers", "specified"]


class INoteState(TypedDict):
    is_favorited: bool
    is_muted_thread: bool


class INoteUpdated(TypedDict, Generic[T]):
    type: Literal["noteUpdated"]
    body: T


class INoteUpdatedDeleteBody(TypedDict):
    deleted_at: str


class INoteUpdatedDelete(TypedDict):
    id: str
    type: Literal["deleted"]
    body: INoteUpdatedDeleteBody


class INoteUpdatedReactionBody(TypedDict):
    reaction: str
    emoji: ICustomEmojiLite
    user_id: str


class INoteUpdatedReaction(TypedDict):
    id: str
    type: Literal["reacted", "unreacted"]
    body: INoteUpdatedReactionBody


class GeoPayload(TypedDict):
    """
    衛星情報
    """

    coordinates: Optional[list[Any]]
    altitude: int | None
    accuracy: int | None
    altitude_accuracy: int | None
    heading: int | None
    speed: int | None


class INoteChannel(TypedDict):
    """ノート内にあるチャンネルの情報

    ログインしていてもis_following等は存在しない
    """

    id: str
    name: str
    color: str
    is_sensitive: bool
    allow_renote_to_external: bool


class INote(TypedDict):
    """Misskey Raw Model: Note"""

    id: str
    created_at: str
    deleted_at: NotRequired[str]
    text: str | None
    cw: str | None
    user_id: str
    user: IPartialUser
    reply_id: str | None
    renote_id: str | None
    reply: NotRequired["INote"]
    renote: NotRequired["INote"]
    is_hidden: NotRequired[bool]
    visibility: INoteVisibility
    mentions: NotRequired[list[str]]
    visible_user_ids: NotRequired[list[str]]
    file_ids: list[str]
    files: list[IFile]
    tags: NotRequired[list[str]]
    poll: NotRequired[IPoll]
    channel_id: NotRequired[str | None]
    channel: NotRequired[INoteChannel | None]
    local_only: bool
    reaction_acceptance: IReactionAcceptance
    reactions: dict[str, int]  # リアクションの種類と数
    renote_count: int
    replies_count: int
    uri: NotRequired[str]
    url: NotRequired[str]
    reaction_and_user_pair_cache: NotRequired[
        dict[str, list[IPartialUser]]
    ]  # リアクションとユーザーのペアのキャッシュ
    clipped_count: NotRequired[int]  # Misskeyの内部的にたまに存在しないだけで普通は存在しそう...?
    my_reaction: NotRequired[str | None]  # ログイン時のみ存在


class ICreatedNote(TypedDict):
    """
    created note
    """

    created_note: INote


class INoteReaction(TypedDict):
    id: str
    created_at: str
    user: IPartialUser
    type: str


class INoteTranslateResult(TypedDict):
    sourceLang: str
    text: str
