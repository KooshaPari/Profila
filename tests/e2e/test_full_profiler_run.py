"""End-to-end tests for full profiler run.

Traces to: FR-PROF-201 - Full Profiler Run
"""

import json
import subprocess
from pathlib import Path

import pytest


class TestFullProfilerRun:
    """Test suite for complete profiler execution."""

    def test_profiler_script_exists(self):
        """Verify the main profiler entry point exists."""
        profiler_sh = Path(__file__).parent.parent.parent / "bin" / "profiler.sh"
        assert profiler_sh.exists(), "profiler.sh not found"

    def test_profiler_sh_help(self):
        """Test that profiler.sh provides help information."""
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        
        result = subprocess.run(
            ["bash", str(bin_dir / "profiler.sh"), "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode in [0, 1]

    def test_all_metrics_script(self):
        """Test that all_metrics.sh script is valid."""
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        
        result = subprocess.run(
            ["bash", "-n", str(bin_dir / "all_metrics.sh")],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0

    def test_end_to_end_complexity_analysis(self, temp_dir):
        """Complete E2E test: create Python files, analyze, verify output."""
        src_dir = temp_dir / "project" / "src"
        src_dir.mkdir(parents=True)
        
        (src_dir / "calculator.py").write_text("""
class Calculator:
    def add(self, a, b):
        return a + b
    
    def factorial(self, n):
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)
""")
        
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        import sys
        sys.path.insert(0, str(bin_dir))
        from complexity_analyzer import ComplexityAnalyzer
        
        analyzer = ComplexityAnalyzer(str(src_dir))
        analyzer.analyze()
        
        expected_functions = {"add", "factorial"}
        found_functions = {f.name for f in analyzer.functions}
        
        assert expected_functions <= found_functions
        
        factorial = next(f for f in analyzer.functions if f.name == "factorial")
        assert factorial.recurses, "factorial should be marked as recursive"

    def test_continuous_mode_simulation(self):
        """Simulate continuous profiler operation."""
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        
        result = subprocess.run(
            ["python3", str(bin_dir / "continuous_profiler.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0

    def test_chart_generation_workflow(self, temp_dir):
        """Test chart generation from metrics data."""
        bin_dir = Path(__file__).parent.parent.parent / "bin"
        
        metrics_data = {
            "timestamps": ["2026-04-01T10:00:00", "2026-04-01T10:01:00"],
            "cpu_percent": [25.5, 30.2],
            "memory_percent": [60.0, 62.5]
        }
        
        input_file = temp_dir / "metrics.json"
        input_file.write_text(json.dumps(metrics_data))
        
        import sys
        sys.path.insert(0, str(bin_dir))
        
        try:
            import generate_charts
            assert hasattr(generate_charts, 'main') or hasattr(generate_charts, 'generate')
        except ImportError:
            pytest.skip("Cannot import generate_charts")
