"""Analytics module for Profila.

Provides anonymous usage analytics without collecting personally identifiable information.
"""

from __future__ import annotations

import hashlib
import json
import platform
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class AnalyticsEvent:
    """A single analytics event."""
    event_type: str
    timestamp: str
    anonymous_id: str
    properties: dict


class AnalyticsCollector:
    """Collects anonymous analytics for Profila."""
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path("./output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.anonymous_id = self._generate_anonymous_id()
    
    def _generate_anonymous_id(self) -> str:
        """Generate a unique but anonymous session ID."""
        # Use machine characteristics to create a stable ID
        characteristics = f"{platform.system()}-{platform.machine()}"
        return hashlib.sha256(characteristics.encode()).hexdigest()[:16]
    
    def track(self, event_type: str, properties: Optional[dict] = None) -> None:
        """Track an analytics event.
        
        Args:
            event_type: Type of event (e.g., "analyze", "export", "error")
            properties: Additional properties to track
        """
        event = AnalyticsEvent(
            event_type=event_type,
            timestamp=datetime.utcnow().isoformat(),
            anonymous_id=self.anonymous_id,
            properties=properties or {}
        )
        
        # Write to local file only
        output_file = self.output_dir / "analytics.jsonl"
        with open(output_file, "a") as f:
            f.write(json.dumps(asdict(event)) + "\n")
    
    def track_analyze(self, file_count: int, function_count: int, duration_ms: float) -> None:
        """Track an analysis run."""
        self.track("analyze", {
            "file_count": file_count,
            "function_count": function_count,
            "duration_ms": duration_ms
        })
    
    def track_error(self, error_type: str, message: str) -> None:
        """Track an error occurrence."""
        self.track("error", {
            "error_type": error_type,
            "message": message
        })
    
    def track_export(self, export_format: str, size_bytes: int) -> None:
        """Track an export operation."""
        self.track("export", {
            "format": export_format,
            "size_bytes": size_bytes
        })


# Global analytics collector
_analytics: Optional[AnalyticsCollector] = None


def get_analytics(output_dir: Optional[str] = None) -> AnalyticsCollector:
    """Get or create global analytics collector."""
    global _analytics
    
    if _analytics is None:
        _analytics = AnalyticsCollector(output_dir)
    
    return _analytics
