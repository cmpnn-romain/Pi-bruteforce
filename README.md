<a name="readme-top"></a>

<br />
<div align="center">
  <h3 align="center">Pi Bruteforce | Number Finder</h3>
</div>

## Table of Contents

- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Output Format](#output-format)

## About The Project

**Pi Bruteforce** is a high-performance, multi-threaded tool for finding number sequences within the digits of Pi. According to the **Pi Search** theory, any finite sequence of digits should eventually appear in Pi including phone numbers, birthdays, SSNs, and more.

### Key Features
- 📊 **Chudnovsky algorithm** - Used for Pi computation
- 🚀 **Multi-threaded** - Auto-detects CPU cores for maximum performance
- 💾 **Binary compressed cache** - Faster loading with smaller file size
- 🔍 **Advanced pattern matching** - Regex, ranges, and multiple patterns
- ♾️ **Unlimited results** - Finds every unique match in Pi
- 📊 **JSON output** - Auto-generated filenames with comprehensive metadata

### Built With

* [![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)

## Getting Started

### Prerequisites

Python 3.12 or newer.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/cmpnn-romain/Pi-bruteforce.git
   ```
2. Make script executable
   ```bash
   chmod +x pi_brutforce.sh
   ```
3. Setup Dependencies
   ```bash
   ./pi_brutforce.sh --setup
   ```
4. Compute Pi Cache (First Time)
   ```bash
   ./pi_brutforce.sh --compute
   ```
   This creates a binary compressed cache (`pi_cache.pkl.gz`) for fast searches.

## Usage

View all options:
```bash
./pi_brutforce.sh --help
```

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

## Output Format
All results are saved to auto-generated JSON files with comprehensive metadata:
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
    }
  ]
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
