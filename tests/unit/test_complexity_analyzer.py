"""Unit tests for complexity analyzer.

Traces to: FR-PROF-001 - Space/Time Complexity Analysis
"""

import pytest
from pathlib import Path

# Import after conftest.py modifies sys.path
from complexity_analyzer import ComplexityAnalyzer, Function


class TestComplexityAnalyzer:
    """Test suite for ComplexityAnalyzer class."""

    def test_init(self, temp_dir):
        """Test analyzer initialization."""
        analyzer = ComplexityAnalyzer(str(temp_dir))
        assert analyzer.root == temp_dir
        assert analyzer.functions == []
        assert analyzer.total_lines == 0
        assert analyzer.total_functions == 0

    def test_analyze_file_finds_functions(self, temp_dir, sample_python_file):
        """Test that analyze_file finds all functions in a file."""
        analyzer = ComplexityAnalyzer(str(temp_dir))
        analyzer.analyze_file(sample_python_file)
        
        # Should find: simple_function, complex_function, method
        assert len(analyzer.functions) == 3
        function_names = {f.name for f in analyzer.functions}
        assert "simple_function" in function_names
        assert "complex_function" in function_names
        assert "method" in function_names

    def test_simple_function_complexity(self, temp_dir, sample_python_file):
        """Test complexity calculation for simple function."""
        analyzer = ComplexityAnalyzer(str(temp_dir))
        analyzer.analyze_file(sample_python_file)
        
        simple = next(f for f in analyzer.functions if f.name == "simple_function")
        assert simple.complexity == 1  # Base complexity
        assert simple.cyclomatic == 1
        assert simple.loops == 0
        assert simple.conditionals == 0

    def test_complex_function_detection(self, temp_dir, sample_python_file):
        """Test detection of loops and conditionals."""
        analyzer = ComplexityAnalyzer(str(temp_dir))
        analyzer.analyze_file(sample_python_file)
        
        complex_func = next(f for f in analyzer.functions if f.name == "complex_function")
        assert complex_func.loops == 1  # One for loop
        assert complex_func.conditionals == 2  # Two if statements
        assert complex_func.complexity > 1

    def test_line_counting(self, temp_dir, sample_python_file):
        """Test that total lines are counted correctly."""
        analyzer = ComplexityAnalyzer(str(temp_dir))
        analyzer.analyze_file(sample_python_file)
        
        # Sample file has ~15 lines
        assert analyzer.total_lines > 0
        assert analyzer.total_lines >= 10

    def test_ignores_venv(self, temp_dir):
        """Test that venv directories are ignored."""
        # Create a venv directory with a Python file
        venv_dir = temp_dir / ".venv"
        venv_dir.mkdir()
        venv_file = venv_dir / "test.py"
        venv_file.write_text("def venv_func(): pass")
        
        # Create a regular Python file
        regular_file = temp_dir / "regular.py"
        regular_file.write_text("def regular_func(): pass")
        
        analyzer = ComplexityAnalyzer(str(temp_dir))
        analyzer.analyze()
        
        # Should only find the regular function
        function_names = {f.name for f in analyzer.functions}
        assert "regular_func" in function_names
        assert "venv_func" not in function_names

    def test_analyze_returns_self(self, temp_dir):
        """Test that analyze() returns self for chaining."""
        analyzer = ComplexityAnalyzer(str(temp_dir))
        result = analyzer.analyze()
        assert result is analyzer


class TestFunctionDataclass:
    """Test Function dataclass behavior."""

    def test_default_values(self):
        """Test Function default values."""
        func = Function(name="test", line=1)
        assert func.name == "test"
        assert func.line == 1
        assert func.complexity == 1
        assert func.cyclomatic == 1
        assert func.params == 0
        assert func.recurses is False
        assert func.loops == 0
        assert func.conditionals == 0

    def test_custom_values(self):
        """Test Function with custom values."""
        func = Function(
            name="complex",
            line=10,
            complexity=5,
            cyclomatic=4,
            params=3,
            recurses=True,
            loops=2,
            conditionals=3
        )
        assert func.complexity == 5
        assert func.cyclomatic == 4
        assert func.params == 3
        assert func.recurses is True
