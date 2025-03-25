import re
from typing import Dict, List

class RuleManager:
    """Manages email classification rules and performs email categorization."""
    def __init__(self):
        self.rules = {}

    async def store_rules(self, rules_content: str) -> bool:
        # TODO: Parse and store rules
        self.rules = {"rules": rules_content}
        return True

    async def get_rules(self) -> dict:
        return self.rules

# Single instance to be used across the application
rule_manager = RuleManager()
