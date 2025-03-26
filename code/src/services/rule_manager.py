import re
import os
import json
from typing import Dict, List

class RuleManager:
    """Manages email classification rules and performs email categorization."""
    def __init__(self):
        self.rules = {}
        try:
            # Look for rules.json in the same directory as this file
            current_dir = os.path.dirname(__file__)
            rules_path = os.path.join(current_dir, 'rules.json')
            
            if os.path.exists(rules_path):
                with open(rules_path, 'r') as f:
                    data = json.load(f)
                    # Extract rules from the classification_rules array
                    for rule in data.get('classification_rules', []):
                        # Use request_type as key and keywords as values
                        self.rules[rule['request_type']] = rule['keywords']
        except Exception as e:
            print(f"Error loading initial rules: {e}")

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