"""
Search Algorithms Module

Implements multi-threaded search algorithms for finding patterns in Pi digits.
"""

import re
import multiprocessing
from colorama import Fore, Style


class PiSearcher:
    """Handles all search operations on Pi digits."""
    
    @staticmethod
    def bruteforce(pi_digits, length, starts_with=None, ends_with=None, contains=None, limit=None, threads=None):
        """
        Bruteforce numbers in Pi matching the given pattern using multi-threading.
        
        Args:
            pi_digits: String of Pi digits to search
            length: Length of numbers to find
            starts_with: Pattern the number must start with
            ends_with: Pattern the number must end with
            contains: Pattern the number must contain
            limit: Maximum number of results to return (None = unlimited)
            threads: Number of threads to use (None = auto-detect CPU count)
            
        Returns:
            List of (position, number) tuples matching the pattern
        """
        print(f"\n{Fore.CYAN}[*] Bruteforcing {length}-digit numbers in Pi...{Style.RESET_ALL}")
        
        # Build pattern description
        pattern_desc = []
        if starts_with:
            pattern_desc.append(f"starts with '{starts_with}'")
        if ends_with:
            pattern_desc.append(f"ends with '{ends_with}'")
        if contains:
            pattern_desc.append(f"contains '{contains}'")
        
        if pattern_desc:
            print(f"{Fore.CYAN}[*] Pattern: {', '.join(pattern_desc)}{Style.RESET_ALL}")
        
        # Determine number of threads
        if threads is None:
            threads = multiprocessing.cpu_count()
        
        print(f"{Fore.CYAN}[*] Using {threads} thread(s) for parallel search{Style.RESET_ALL}")
        
        # Split work into chunks for parallel processing
        chunk_size = len(pi_digits) // threads
        chunks = []
        for i in range(threads):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < threads - 1 else len(pi_digits)
            chunks.append((start_idx, end_idx, pi_digits, length, starts_with, ends_with, contains))
        
        # Run parallel search
        if threads > 1:
            with multiprocessing.Pool(threads) as pool:
                chunk_results = pool.map(_search_chunk, chunks)
        else:
            # Single-threaded fallback
            chunk_results = [_search_chunk(chunks[0])]
        
        # Merge results from all threads
        matches = []
        seen_numbers = set()
        
        for chunk_matches in chunk_results:
            for pos, number in chunk_matches:
                if number not in seen_numbers:
                    matches.append((pos, number))
                    seen_numbers.add(number)
                    
                    # Only break if limit is set
                    if limit is not None and len(matches) >= limit:
                        break
            
            if limit is not None and len(matches) >= limit:
                break
        
        # Sort by position
        matches.sort(key=lambda x: x[0])
        
        return matches
    
    @staticmethod
    def regex_search(pi_digits, pattern, limit=None, threads=None):
        """
        Search for numbers matching a regex pattern.
        
        Args:
            pi_digits: String of Pi digits to search
            pattern: Regex pattern to match
            limit: Maximum number of results to return (None = unlimited)
            threads: Number of threads to use (None = auto-detect CPU count)
            
        Returns:
            List of (position, number) tuples matching the pattern
        """
        print(f"\n{Fore.CYAN}[*] Searching with regex pattern: {pattern}{Style.RESET_ALL}")
        
        # Compile regex
        try:
            regex = re.compile(pattern)
        except re.error as e:
            print(f"{Fore.RED}[✗] Invalid regex pattern: {e}{Style.RESET_ALL}")
            return []
        
        # Determine number of threads
        if threads is None:
            threads = multiprocessing.cpu_count()
        
        print(f"{Fore.CYAN}[*] Using {threads} thread(s) for parallel search{Style.RESET_ALL}")
        
        # Split work into chunks
        chunk_size = len(pi_digits) // threads
        chunks = []
        for i in range(threads):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < threads - 1 else len(pi_digits)
            chunks.append((start_idx, end_idx, pi_digits, pattern))
        
        # Run parallel search
        if threads > 1:
            with multiprocessing.Pool(threads) as pool:
                chunk_results = pool.map(_search_chunk_regex, chunks)
        else:
            chunk_results = [_search_chunk_regex(chunks[0])]
        
        # Merge results
        matches = []
        seen_numbers = set()
        
        for chunk_matches in chunk_results:
            for pos, number in chunk_matches:
                if number not in seen_numbers:
                    matches.append((pos, number))
                    seen_numbers.add(number)
                    
                    if limit is not None and len(matches) >= limit:
                        break
            
            if limit is not None and len(matches) >= limit:
                break
        
        # Sort by position
        matches.sort(key=lambda x: x[0])
        
        return matches
    
    @staticmethod
    def direct_search(pi_digits, target):
        """
        Search for all occurrences of a specific number sequence.
        
        Args:
            pi_digits: String of Pi digits to search
            target: Target number sequence to find
            
        Returns:
            List of (position, number) tuples
        """
        positions = []
        start = 0
        
        while True:
            pos = pi_digits.find(target, start)
            if pos == -1:
                break
            positions.append((pos, target))
            start = pos + 1
        
        return positions


def _search_chunk(args):
    """
    Worker function for bruteforce search chunk.
    
    Args:
        args: Tuple of (start_idx, end_idx, pi_digits, length, starts_with, ends_with, contains)
        
    Returns:
        List of (position, number) tuples found in this chunk
    """
    start_idx, end_idx, pi_digits, length, starts_with, ends_with, contains = args
    local_matches = []
    local_seen = set()
    
    for i in range(start_idx, min(end_idx, len(pi_digits) - length + 1)):
        candidate = pi_digits[i:i + length]
        
        # Check if candidate matches all criteria
        if len(candidate) != length:
            continue
            
        if starts_with and not candidate.startswith(starts_with):
            continue
            
        if ends_with and not candidate.endswith(ends_with):
            continue
            
        if contains and contains not in candidate:
            continue
        
        # Only add unique numbers
        if candidate not in local_seen:
            local_matches.append((i, candidate))
            local_seen.add(candidate)
    
    return local_matches


def _search_chunk_regex(args):
    """
    Worker function for regex search chunk.
    
    Args:
        args: Tuple of (start_idx, end_idx, pi_digits, pattern)
        
    Returns:
        List of (position, number) tuples found in this chunk
    """
    start_idx, end_idx, pi_digits, pattern = args
    local_matches = []
    local_seen = set()
    
    # Compile regex
    regex = re.compile(pattern)
    
    # Search in this chunk
    chunk_text = pi_digits[start_idx:end_idx]
    for match in regex.finditer(chunk_text):
        number = match.group()
        pos = start_idx + match.start()
        
        if number not in local_seen:
            local_matches.append((pos, number))
            local_seen.add(number)
    
    return local_matches
