"""Unit tests for system metrics collector.

Traces to: FR-PROF-003 - System Metrics Collection
"""

import json
import pytest
from unittest.mock import MagicMock, patch

from system_metrics import collect


class TestSystemMetrics:
    """Test suite for system metrics collection."""

    def test_collect_returns_dict(self, mock_psutil):
        """Test that collect() returns a dictionary."""
        result = collect()
        assert isinstance(result, dict)

    def test_collect_has_cpu_metrics(self, mock_psutil):
        """Test that result includes CPU metrics."""
        result = collect()
        
        assert "cpu" in result
        assert "percent" in result["cpu"]
        assert "times" in result["cpu"]
        assert "count" in result["cpu"]
        assert result["cpu"]["percent"] == 25.5
        assert result["cpu"]["count"] == 8

    def test_collect_has_memory_metrics(self, mock_psutil):
        """Test that result includes memory metrics."""
        result = collect()
        
        assert "memory" in result
        assert "total_bytes" in result["memory"]
        assert "available_bytes" in result["memory"]
        assert "percent" in result["memory"]
        assert result["memory"]["total_bytes"] == 16 * 1024 * 1024 * 1024

    def test_collect_has_swap_metrics(self, mock_psutil):
        """Test that result includes swap metrics."""
        result = collect()
        
        assert "swap" in result
        assert "total_bytes" in result["swap"]
        assert "used_bytes" in result["swap"]
        assert "percent" in result["swap"]

    def test_collect_has_disk_metrics(self, mock_psutil):
        """Test that result includes disk metrics."""
        result = collect()
        
        assert "disk" in result
        assert isinstance(result["disk"], dict)

    def test_collect_has_timestamp(self, mock_psutil):
        """Test that result includes timestamp."""
        result = collect()
        
        assert "timestamp" in result
        assert isinstance(result["timestamp"], (int, float))

    def test_json_serializable(self, mock_psutil):
        """Test that result can be serialized to JSON."""
        result = collect()
        
        json_str = json.dumps(result)
        assert isinstance(json_str, str)
        
        parsed = json.loads(json_str)
        assert parsed["cpu"]["percent"] == 25.5
