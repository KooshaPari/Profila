"""Pytest configuration and shared fixtures for Profila tests."""

import os
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add bin/ to path for importing profila modules
sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def sample_python_file(temp_dir):
    """Create a sample Python file for complexity analysis."""
    file_path = temp_dir / "sample.py"
    file_path.write_text("""
def simple_function():
    return 1

def complex_function(n):
    if n > 0:
        for i in range(n):
            if i % 2 == 0:
                print(i)
    return n

class SampleClass:
    def method(self):
        return True
""")
    return file_path


@pytest.fixture
def mock_psutil():
    """Mock psutil for system metrics testing."""
    with patch("system_metrics.psutil") as mock:
        mock.cpu_percent.return_value = 25.5
        mock.cpu_times.return_value._asdict.return_value = {
            "user": 100.0,
            "system": 50.0,
            "idle": 850.0,
        }
        mock.cpu_count.return_value = 8
        
        # Mock memory
        mem_mock = MagicMock()
        mem_mock.total = 16 * 1024 * 1024 * 1024
        mem_mock.available = 8 * 1024 * 1024 * 1024
        mem_mock.percent = 50.0
        mem_mock.used = 8 * 1024 * 1024 * 1024
        mem_mock.free = 8 * 1024 * 1024 * 1024
        mock.virtual_memory.return_value = mem_mock
        
        # Mock swap
        swap_mock = MagicMock()
        swap_mock.total = 4 * 1024 * 1024 * 1024
        swap_mock.used = 1 * 1024 * 1024 * 1024
        swap_mock.free = 3 * 1024 * 1024 * 1024
        swap_mock.percent = 25.0
        mock.swap_memory.return_value = swap_mock
        
        yield mock


@pytest.fixture
def output_dir(temp_dir):
    """Provide an output directory for test artifacts."""
    out = temp_dir / "output"
    out.mkdir()
    return out
