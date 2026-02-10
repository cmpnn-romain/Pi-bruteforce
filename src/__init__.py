"""
Pi Bruteforce Tool - Modular Package

A high-performance, multi-threaded tool for finding number sequences within the digits of Pi.
"""

__version__ = "2.0.0"
__author__ = "Pi Bruteforce Team"

from .cache import PiCache
from .compute import PiComputer
from .search import PiSearcher
from .output import save_results_json, generate_filename

__all__ = [
    "PiCache",
    "PiComputer", 
    "PiSearcher",
    "save_results_json",
    "generate_filename"
]
