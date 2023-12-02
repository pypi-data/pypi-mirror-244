# models.pyi
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class ParsedWebhook:
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    source_url: Optional[str]
    onlinestore_name: Optional[str]
    topic: Optional[str]

    def __post_init__(self) -> None: ...
