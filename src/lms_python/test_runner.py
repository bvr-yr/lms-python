"""Unittest discovery and execution script."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = PROJECT_ROOT / "tests"


def run_tests() -> None:
    """Discover and execute all test cases in the tests directory."""
    suite = unittest.defaultTestLoader.discover(str(TESTS_DIR))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
