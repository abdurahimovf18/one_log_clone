import uuid
from datetime import datetime, timedelta
from typing import TypedDict


class MessageData(TypedDict):
    id: uuid.UUID
    owner_id: uuid.UUID
    text_id: uuid.UUID | None
    interval: timedelta
    duration: timedelta
    started_at: datetime | None
    created_at: datetime


class SettingsPageItem(TypedDict):
    is_selected: bool
    callback: str
    label: str


class SettingsPage(TypedDict):
    items: list[SettingsPageItem]


class SettingsStateData(TypedDict):
    page: SettingsPage
