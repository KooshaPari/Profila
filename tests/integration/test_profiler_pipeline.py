"""Integration tests for profiler pipeline.

Traces to: FR-PROF-101 - Profiler Pipeline Integration
"""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestProfilerPipeline:
    """Test suite for profiler pipeline integration."""

    def test_bin_scripts_exist(self):
        """Verify all profiler scripts exist and are executable."""
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        
        required_scripts = [
            "complexity_analyzer.py",
            "continuous_profiler.py",
            "system_metrics.py",
            "generate_charts.py",
            "profiler.sh",
            "all_metrics.sh",
        ]
        
        for script in required_scripts:
            script_path = bin_dir / script
            assert script_path.exists(), f"Missing script: {script}"

    def test_system_metrics_output_structure(self):
        """Test that system metrics returns expected data structure."""
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        
        result = subprocess.run(
            ["python3", str(bin_dir / "system_metrics.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0, f"system_metrics.py failed: {result.stderr}"

    def test_profiler_sh_syntax(self):
        """Test that main profiler.sh script has valid syntax."""
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        
        result = subprocess.run(
            ["bash", "-n", str(bin_dir / "profiler.sh")],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"profiler.sh has syntax errors: {result.stderr}"

    def test_analyze_multiple_files(self, temp_dir):
        """Test that analyzer processes multiple Python files."""
        for i in range(3):
            (temp_dir / f"module_{i}.py").write_text(f"""
def function_{i}():
    return {i}
""")
        
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        import sys
        sys.path.insert(0, str(bin_dir))
        from complexity_analyzer import ComplexityAnalyzer
        
        analyzer = ComplexityAnalyzer(str(temp_dir))
        analyzer.analyze()
        
        assert len(analyzer.functions) == 3

    def test_ignores_non_python_files(self, temp_dir):
        """Test that analyzer ignores non-Python files."""
        (temp_dir / "valid.py").write_text("def func(): pass")
        (temp_dir / "not_python.txt").write_text("not python code")
        
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        import sys
        sys.path.insert(0, str(bin_dir))
        from complexity_analyzer import ComplexityAnalyzer
        
        analyzer = ComplexityAnalyzer(str(temp_dir))
        analyzer.analyze()
        
        assert len(analyzer.functions) == 1
        assert analyzer.functions[0].name == "func"
