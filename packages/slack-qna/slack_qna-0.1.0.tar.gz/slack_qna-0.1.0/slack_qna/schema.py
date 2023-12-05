from typing import Optional, Union, Callable
from dataclasses import dataclass

@dataclass
class IncomingMessage:
    message_id: str
    channel_id: str
    raw: str
    message: str
    thread_id: Optional[str] = None

@dataclass
class OutgoingMessage:
    channel_id: str
    data: Union[str, bytes]
    data_type: str  # 'text' or 'image' or 'file'
    thread_id: Optional[str] = None

@dataclass
class Reactions:
    loading: Optional[str] = None
    success: Optional[str] = None
    failed: Optional[str] = None

@dataclass
class CommandHook:
    is_sync: bool
    data_type: str  # 'text' or 'image' or 'file
    handler: Callable[[IncomingMessage], 'Awaitable[Union[str, bytes]]']

