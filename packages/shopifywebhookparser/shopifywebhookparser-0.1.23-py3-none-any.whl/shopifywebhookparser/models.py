# models.py
from dataclasses import dataclass, field, InitVar
from typing import Any, Optional

@dataclass
class ParsedWebhook:
    """
    Represents a parsed Shopify webhook request.

    Attributes:
        payload (Dict[str, Any]): The main content of the webhook, typically parsed from JSON.
        attributes (Dict[str, str]): The headers from the webhook request.
        source_url (Optional[str]): The source URL of the webhook, extracted from the headers if not provided.
        onlinestore_name (Optional[str]): The name of the online store, derived from the source URL if not provided.
        topic (Optional[str]): The topic of the webhook, extracted from the headers if not provided.
    """
    payload: dict[str, Any]
    attributes: dict[str, str]
    source_url: Optional[str] = None
    onlinestore_name: Optional[str] = None
    topic: Optional[str] = None

    def __post_init__(self):
        # Set `source_url`, `onlinestore_name`, `topic` if not provided during initialization
        if not self.source_url:
            self.source_url = self.attributes.get("X-Shopify-Shop-Domain", "")
        if not self.onlinestore_name:
            self.onlinestore_name = self.source_url.split(".")[0] if self.source_url else ""
        if not self.topic:
            self.topic = self.attributes.get("X-Shopify-Topic", "")
