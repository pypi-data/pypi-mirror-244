# models.py
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ParsedWebhook:
    """
    Represents a parsed Shopify webhook request.

    Attributes:
        payload (Dict[str, Any]): The main content of the webhook, typically parsed from JSON.
        attributes (Dict[str, str]): The headers from the webhook request.
        source_url (str): The source URL of the webhook, extracted from the headers.
        onlinestore_name (str): The name of the online store, derived from the source URL.
        topic (str): The topic of the webhook, extracted from the headers.

    The `source_url`, `onlinestore_name`, and `topic` attributes are set in the `__post_init__` method
    based on the provided `attributes`.
    """

    payload: dict[str, Any]
    attributes: dict[str, str]
    source_url: Optional[str] = field(default=None, init=False)
    onlinestore_name: Optional[str] = field(default=None, init=False)
    topic: Optional[str] = field(default=None, init=False)

    def __post_init__(self):
        if not self.source_url:
            self.source_url = self.attributes.get("X-Shopify-Shop-Domain", "")
        if not self.onlinestore_name:
            self.onlinestore_name = (
                self.source_url.split(".")[0] if self.source_url else ""
            )
        if not self.topic:
            self.topic = self.attributes.get("X-Shopify-Topic", "")
