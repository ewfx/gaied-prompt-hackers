import re
from typing import Dict, List

class RuleManager:
    """Manages email classification rules and performs email categorization."""
    def __init__(self):
        self.rules = {}

    def add_rules(self, new_rules: Dict[str, List[str]]) -> bool:
        """
        Add new classification rules to the manager.
        If a category already exists, its keywords will be updated.
        """
        for category, keywords in new_rules.items():
            if category in self.rules:
                # Append new keywords to the existing category
                self.rules[category].extend(keywords)
                # Remove duplicates
                self.rules[category] = list(set(self.rules[category]))
            else:
                # Add new category with keywords
                self.rules[category] = keywords
        return True

    def get_rules(self) -> Dict[str, List[str]]:
        """
        Retrieve the current classification rules.
        """
        return self.rules

# Single instance to be used across the application
rule_manager = RuleManager()