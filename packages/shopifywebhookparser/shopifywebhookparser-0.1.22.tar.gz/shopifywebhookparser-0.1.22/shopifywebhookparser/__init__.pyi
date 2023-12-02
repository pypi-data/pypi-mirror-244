# __init__.pyi
from .models import ParsedWebhook
from .parsing import create_parsed_webhook, parse_verification_params, azure_strategy

# Assuming you have the type hints for these in their respective .pyi files, 
# you don't need to repeat them here. Just re-export them as below:

def create_parsed_webhook(...): ...
def parse_verification_params(...): ...
def azure_strategy(...): ...

# If ParsedWebhook is a class:
class ParsedWebhook:
    ...
