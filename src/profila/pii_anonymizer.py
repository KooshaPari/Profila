"""PII Anonymizer for Profila.

Provides utilities for anonymizing sensitive information in reports.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# Common PII patterns
PII_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
}


@dataclass
class AnonymizerConfig:
    """Configuration for anonymization."""
    hash_paths: bool = True
    hash_authors: bool = True
    redact_pii: bool = True
    custom_replacements: dict[str, str] = None


class PIIAnonymizer:
    """Anonymizes PII in profiler reports."""
    
    def __init__(self, config: Optional[AnonymizerConfig] = None):
        self.config = config or AnonymizerConfig()
    
    def hash_string(self, value: str, salt: str = "") -> str:
        """Create a deterministic hash of a string."""
        combined = f"{salt}:{value}"
        return hashlib.sha256(combined.encode()).hexdigest()[:12]
    
    def anonymize_path(self, path: str) -> str:
        """Anonymize a file path."""
        if not self.config.hash_paths:
            return path
        
        # Replace home directory paths
        home = str(Path.home())
        if path.startswith(home):
            path = path.replace(home, "/user")
        
        return path
    
    def anonymize_author(self, name: str, email: str) -> dict:
        """Anonymize git author information."""
        if not self.config.hash_authors:
            return {"name": name, "email": email}
        
        return {
            "name": f"Author-{self.hash_string(name, 'author')}",
            "email": f"{self.hash_string(email, 'email')}@anonymous.local"
        }
    
    def redact_pii_in_text(self, text: str) -> str:
        """Redact PII patterns from text."""
        if not self.config.redact_pii:
            return text
        
        result = text
        
        for pii_type, pattern in PII_PATTERNS.items():
            result = re.sub(pattern, f"[{pii_type}_redacted]", result)
        
        return result
    
    def anonymize_report(self, report: dict) -> dict:
        """Anonymize a complete report."""
        result = report.copy()
        
        # Anonymize paths
        if "paths" in result:
            result["paths"] = [self.anonymize_path(p) for p in result["paths"]]
        
        # Anonymize author info
        if "authors" in result:
            result["authors"] = [self.anonymize_author(**a) for a in result["authors"]]
        
        # Redact PII in text fields
        for key, value in result.items():
            if isinstance(value, str):
                result[key] = self.redact_pii_in_text(value)
        
        return result


def anonymize_report(report: dict, level: str = "standard") -> dict:
    """Convenience function to anonymize a report.
    
    Args:
        report: The report to anonymize
        level: Anonymization level ("minimal", "standard", "strict")
    
    Returns:
        Anonymized report
    """
    configs = {
        "minimal": AnonymizerConfig(hash_paths=False, hash_authors=False, redact_pii=False),
        "standard": AnonymizerConfig(),
        "strict": AnonymizerConfig(hash_paths=True, hash_authors=True, redact_pii=True),
    }
    
    config = configs.get(level, configs["standard"])
    anonymizer = PIIAnonymizer(config)
    return anonymizer.anonymize_report(report)
