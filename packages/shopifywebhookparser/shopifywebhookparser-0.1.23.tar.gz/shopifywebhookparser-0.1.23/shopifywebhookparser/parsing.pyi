# models.pyi
from typing import Any, Dict, Optional
from dataclasses import dataclass

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
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    source_url: Optional[str] = None
    onlinestore_name: Optional[str] = None
    topic: Optional[str] = None

    def __post_init__(self) -> None: ...
