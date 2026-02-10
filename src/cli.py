"""
CLI Module

Handles command-line interface, argument parsing, and main application logic.
"""

import argparse
import sys
from colorama import init, Fore, Style

from .cache import PiCache
from .compute import PiComputer
from .search import PiSearcher
from .output import save_results_json, generate_filename

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Bruteforce number sequences within the digits of Pi using pattern matching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic bruteforce
  %(prog)s --length 9 --starts-with 123
  %(prog)s --length 6 --ends-with 999
  %(prog)s --length 10 --contains 666
  %(prog)s --length 8 --starts-with 42 --ends-with 24
  
  # Advanced features
  %(prog)s --regex "12[0-9]{3}45"                    # Regex pattern
  %(prog)s --min 123000000 --max 123999999           # Range search
  %(prog)s --length 9 --starts-with 123,456,789      # Multiple patterns
  
  # Cache management
  %(prog)s --compute                                 # Compute and cache Pi
  %(prog)s --compute --precision 100000000           # Cache 100M digits
  
  # Legacy mode
  %(prog)s 123456                                    # Direct search
        """
    )
    
    parser.add_argument(
        'target',
        type=str,
        nargs='?',
        help='Specific number sequence to search for (legacy mode)'
    )
    
    parser.add_argument(
        '-l', '--length',
        type=int,
        help='Length of numbers to bruteforce'
    )
    
    parser.add_argument(
        '--starts-with',
        type=str,
        help='Pattern(s) the number must start with (comma-separated for multiple)'
    )
    
    parser.add_argument(
        '--ends-with',
        type=str,
        help='Pattern(s) the number must end with'
    )
    
    parser.add_argument(
        '--contains',
        type=str,
        help='Pattern(s) the number must contain'
    )
    
    parser.add_argument(
        '--regex',
        type=str,
        help='Regex pattern to match (e.g., "12[0-9]{3}45")'
    )
    
    parser.add_argument(
        '--min',
        type=int,
        help='Minimum value for range search'
    )
    
    parser.add_argument(
        '--max',
        type=int,
        help='Maximum value for range search'
    )
    
    parser.add_argument(
        '-p', '--precision',
        type=int,
        default=10000000,
        help='Number of Pi digits to search (default: 10,000,000)'
    )
    
    parser.add_argument(
        '--compute',
        action='store_true',
        help='Compute and cache Pi digits only (no search)'
    )
    
    return parser.parse_args()


def handle_compute_mode(args):
    """Handle compute-only mode."""
    pi_digits = PiComputer.compute(args.precision)
    PiCache.save(pi_digits)


def handle_direct_search(args, pi_digits):
    """Handle legacy direct search mode."""
    target_str = args.target
    print(f"\n{Fore.CYAN}[*] Searching for: {target_str}{Style.RESET_ALL}")
    
    positions = PiSearcher.direct_search(pi_digits, target_str)
    
    # Generate output filename
    output_file = generate_filename("direct_search", target=target_str)
    
    # Build search params
    search_params = {
        "mode": "direct_search",
        "target": target_str,
        "precision": args.precision,
        "limit": None
    }
    
    save_results_json(positions, len(target_str), output_file, search_params)


def handle_regex_mode(args, pi_digits):
    """Handle regex search mode."""
    matches = PiSearcher.regex_search(pi_digits, args.regex, limit=None, threads=None)
    
    # Generate output filename
    output_file = generate_filename("regex", pattern=args.regex)
    
    search_params = {
        "mode": "regex",
        "regex": args.regex,
        "precision": args.precision,
        "limit": None,
        "threads": "auto"
    }
    
    # Determine length from first match
    length = len(matches[0][1]) if matches else 0
    save_results_json(matches, length, output_file, search_params)


def handle_range_mode(args, pi_digits):
    """Handle range search mode."""
    if args.min is None or args.max is None:
        print(f"{Fore.RED}[✗] Error: Both --min and --max are required for range search{Style.RESET_ALL}")
        sys.exit(1)
    
    if args.min > args.max:
        print(f"{Fore.RED}[✗] Error: --min must be less than or equal to --max{Style.RESET_ALL}")
        sys.exit(1)
    
    # Auto-detect length from range
    length = len(str(args.max))
    if len(str(args.min)) != length:
        print(f"{Fore.RED}[✗] Error: --min and --max must have the same number of digits{Style.RESET_ALL}")
        sys.exit(1)
    
    # Find all numbers in range
    matches = PiSearcher.bruteforce(
        pi_digits,
        length=length,
        limit=None,
        threads=None
    )
    
    # Filter by range
    filtered_matches = [(pos, num) for pos, num in matches if args.min <= int(num) <= args.max]
    
    # Generate output filename
    output_file = generate_filename("range", min=args.min, max=args.max)
    
    search_params = {
        "mode": "range",
        "min": args.min,
        "max": args.max,
        "length": length,
        "precision": args.precision,
        "limit": None,
        "threads": "auto"
    }
    
    save_results_json(filtered_matches, length, output_file, search_params)


def handle_multipattern_mode(args, pi_digits):
    """Handle multiple patterns mode."""
    patterns = [p.strip() for p in args.starts_with.split(',')]
    print(f"\n{Fore.CYAN}[*] Searching for {len(patterns)} patterns: {', '.join(patterns)}{Style.RESET_ALL}")
    
    all_matches = []
    seen_numbers = set()
    
    for pattern in patterns:
        matches = PiSearcher.bruteforce(
            pi_digits,
            length=args.length,
            starts_with=pattern,
            ends_with=args.ends_with,
            contains=args.contains,
            limit=None,
            threads=None
        )
        
        for pos, num in matches:
            if num not in seen_numbers:
                all_matches.append((pos, num))
                seen_numbers.add(num)
    
    # Sort by position
    all_matches.sort(key=lambda x: x[0])
    
    # Generate output filename
    output_file = generate_filename("multiple_patterns", length=args.length)
    
    search_params = {
        "mode": "multiple_patterns",
        "length": args.length,
        "patterns": patterns,
        "ends_with": args.ends_with,
        "contains": args.contains,
        "precision": args.precision,
        "limit": None,
        "threads": "auto"
    }
    
    save_results_json(all_matches, args.length, output_file, search_params)


def handle_bruteforce_mode(args, pi_digits):
    """Handle standard bruteforce mode."""
    if not args.length:
        print(f"{Fore.RED}[✗] Error: --length is required for bruteforce mode{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Use --help for usage information{Style.RESET_ALL}")
        sys.exit(1)
    
    # Validate patterns
    if args.starts_with and len(args.starts_with) >= args.length:
        print(f"{Fore.RED}[✗] Error: --starts-with pattern must be shorter than --length{Style.RESET_ALL}")
        sys.exit(1)
    
    if args.ends_with and len(args.ends_with) >= args.length:
        print(f"{Fore.RED}[✗] Error: --ends-with pattern must be shorter than --length{Style.RESET_ALL}")
        sys.exit(1)
    
    # Run bruteforce
    matches = PiSearcher.bruteforce(
        pi_digits,
        length=args.length,
        starts_with=args.starts_with,
        ends_with=args.ends_with,
        contains=args.contains,
        limit=None,
        threads=None
    )
    
    # Generate output filename
    output_file = generate_filename(
        "bruteforce",
        length=args.length,
        starts_with=args.starts_with,
        ends_with=args.ends_with,
        contains=args.contains
    )
    
    # Build search params
    search_params = {
        "mode": "bruteforce",
        "length": args.length,
        "starts_with": args.starts_with,
        "ends_with": args.ends_with,
        "contains": args.contains,
        "precision": args.precision,
        "limit": None,
        "threads": "auto"
    }
    
    save_results_json(matches, args.length, output_file, search_params)


def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # Compute-only mode
    if args.compute:
        handle_compute_mode(args)
        return
    
    # Initialize and load Pi cache
    print(f"{Fore.CYAN}[*] Initializing Pi Bruteforce with {args.precision:,} digits...{Style.RESET_ALL}")
    
    pi_digits, precision = PiCache.load()
    
    # Auto-compute if cache doesn't exist
    if pi_digits is None:
        print(f"{Fore.YELLOW}[!] No cache found. Computing Pi digits...{Style.RESET_ALL}")
        pi_digits = PiComputer.compute(args.precision)
        PiCache.save(pi_digits)
    
    # Legacy mode: direct search
    if args.target and not args.length:
        handle_direct_search(args, pi_digits)
        return
    
    # Regex mode
    if args.regex:
        handle_regex_mode(args, pi_digits)
        return
    
    # Range search mode
    if args.min is not None or args.max is not None:
        handle_range_mode(args, pi_digits)
        return
    
    # Multiple patterns mode
    if args.starts_with and ',' in args.starts_with:
        handle_multipattern_mode(args, pi_digits)
        return
    
    # Standard bruteforce mode
    handle_bruteforce_mode(args, pi_digits)


if __name__ == "__main__":
    main()
