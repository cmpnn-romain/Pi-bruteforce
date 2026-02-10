# Pi Bruteforce | Number Finder

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)

</div>

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Usage Examples](#usage-examples)
5. [Output Format](#output-format)

<br>

## 🎯 Overview

**Pi Bruteforce** is a high-performance, multi-threaded tool for finding number sequences within the digits of Pi. According to the **Pi Search** theory, any finite sequence of digits should eventually appear in Pi including phone numbers, birthdays, SSNs, and more.

### Key Features
- 📊 **Chudnovsky algorithm** - Used for Pi computation
- 🚀 **Multi-threaded** - Auto-detects CPU cores for maximum performance
- 💾 **Binary compressed cache** - Faster loading with smaller file size
- 🔍 **Advanced pattern matching** - Regex, ranges, and multiple patterns
- ♾️ **Unlimited results** - Finds every unique match in Pi
- 📊 **JSON output** - Auto-generated filenames with comprehensive metadata

<br>

## ✨ Features

The tool supports multiple search modes with the following options:

### Search Options
- `--length N` - Length of numbers to find
- `--starts-with P` - Pattern(s) to start with (comma-separated for multiple)
- `--ends-with P` - Pattern(s) to end with
- `--contains P` - Pattern(s) to contain
- `--regex PATTERN` - Regex pattern matching
- `--min N` / `--max N` - Range search (find all numbers between min and max)
- `--precision N` - Number of Pi digits to search (default: 10,000,000)

### Performance Features
- **Auto-threading** - Automatically uses all CPU cores
- **Binary cache** - Stores Pi digits in compressed `.pkl.gz` format
- **Auto-compute** - Automatically generates cache if missing
- **Smart filenames** - Auto-generated based on search parameters

<br>

## 🏃 Quick Start

### 1. Make Script Executable
```bash
chmod +x pi_brutforce.sh
```

### 2. Setup Dependencies
```bash
./pi_brutforce.sh --setup
```

### 3. Compute Pi Cache (First Time)
```bash
./pi_brutforce.sh --compute
```
This creates a binary compressed cache (`pi_cache.pkl.gz`) for fast searches.

### 4. View All Options
```bash
./pi_brutforce.sh --help
```

<br>

## 📖 Usage Examples

### Basic Pattern Matching
```bash
# Find 9-digit numbers starting with 123
./pi_brutforce.sh --length 9 --starts-with 123

# Find 6-digit numbers ending with 999
./pi_brutforce.sh --length 6 --ends-with 999

# Find 10-digit numbers containing 666
./pi_brutforce.sh --length 10 --contains 666

# Combine filters: 8-digit numbers starting with 42 and ending with 24
./pi_brutforce.sh --length 8 --starts-with 42 --ends-with 24
```

### Advanced Features
```bash
# Regex pattern matching
./pi_brutforce.sh --regex "12[0-9]{3}45"

# Range search (all 9-digit numbers from 123000000 to 123999999)
./pi_brutforce.sh --min 123000000 --max 123999999

# Multiple patterns (find numbers starting with 123, 456, or 789)
./pi_brutforce.sh --length 9 --starts-with 123,456,789
```

### Legacy Direct Search
```bash
# Search for a specific number sequence
./pi_brutforce.sh 123456
```

### Cache Management
```bash
# Compute cache with custom precision (100M digits)
./pi_brutforce.sh --compute --precision 100000000
```

<br>

## 📊 Output Format

All results are saved to auto-generated JSON files with comprehensive metadata:

### Example Output: `results_len9_start123.json`
```json
{
  "metadata": {
    "timestamp": "2026-02-10T15:42:00",
    "pi_precision": 10000010,
    "search_parameters": {
      "mode": "bruteforce",
      "length": 9,
      "starts_with": "123",
      "ends_with": null,
      "contains": null,
      "precision": 10000000,
      "limit": null,
      "threads": "auto"
    },
    "total_matches": 1247
  },
  "matches": [
    {
      "match_number": 1,
      "number": "123456789",
      "position": 523551,
      "position_formatted": "523,551"
    },
    {
      "match_number": 2,
      "number": "123789456",
      "position": 891234,
      "position_formatted": "891,234"
    }
  ]
}
```

### Output Filenames
Filenames are automatically generated based on search type:
- **Bruteforce**: `results_len9_start123.json`
- **Regex**: `results_regex_12_0_9__3_45.json`
- **Range**: `results_range_123000000_123999999.json`
- **Multiple patterns**: `results_len9_multipattern.json`
- **Direct search**: `results_search_123456.json`