# parsing.pyi
from typing import Any, Callable, Tuple
from azure.functions import HttpRequest
from .models import ParsedWebhook

ParseFn = Callable[[HttpRequest], Tuple[bytes, dict[str, Any]]]

def create_parsed_webhook(req: HttpRequest, strategy: ParseFn) -> ParsedWebhook: ...
def parse_verification_params(
    req: Any, strategy: ParseFn
) -> Tuple[bytes, str, str]: ...
def azure_strategy(req: HttpRequest) -> Tuple[bytes, dict[str, Any]]: ...
