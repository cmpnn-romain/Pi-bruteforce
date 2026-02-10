"""
Cache Management Module

Handles loading and saving Pi digit cache files in compressed binary format.
Supports both new msgpack+gzip format and legacy JSON format.
"""

import os
import json
import gzip
import msgpack
from datetime import datetime
from colorama import Fore, Style


class PiCache:
    """Manages Pi digit cache operations."""
    
    @staticmethod
    def load(cache_file="pi_cache.pkl.gz"):
        """
        Load Pi digits from compressed binary cache file.
        
        Args:
            cache_file: Path to cache file
            
        Returns:
            tuple: (pi_digits string, precision int) or (None, None) if failed
        """
        if not os.path.exists(cache_file):
            # Try legacy JSON format for backward compatibility
            json_cache = "pi_cache.json"
            if os.path.exists(json_cache):
                print(f"{Fore.YELLOW}[*] Found legacy JSON cache, loading...{Style.RESET_ALL}")
                return PiCache._load_json(json_cache)
            return None, None
        
        print(f"{Fore.YELLOW}[*] Loading Pi cache from {cache_file}...{Style.RESET_ALL}")
        
        try:
            # Decompress and deserialize
            with gzip.open(cache_file, 'rb') as f:
                packed_data = f.read()
            cache_data = msgpack.unpackb(packed_data, raw=False)
            
            pi_digits = cache_data["pi_digits"]
            precision = cache_data["metadata"]["precision"]
            
            print(f"{Fore.GREEN}[✓] Pi cache loaded successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Precision: {len(pi_digits):,} digits{Style.RESET_ALL}")
            return pi_digits, precision
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to load cache: {e}{Style.RESET_ALL}")
            return None, None
    
    @staticmethod
    def save(pi_digits, cache_file="pi_cache.pkl.gz"):
        """
        Save Pi digits to compressed binary cache file.
        
        Args:
            pi_digits: String of Pi digits
            cache_file: Path to cache file
        """
        cache_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "precision": len(pi_digits),
                "version": "2.0"
            },
            "pi_digits": pi_digits
        }
        
        print(f"{Fore.YELLOW}[*] Saving Pi cache to {cache_file}...{Style.RESET_ALL}")
        
        # Serialize with msgpack and compress with gzip
        packed_data = msgpack.packb(cache_data, use_bin_type=True)
        with gzip.open(cache_file, 'wb', compresslevel=6) as f:
            f.write(packed_data)
        
        # Calculate file size
        file_size_mb = os.path.getsize(cache_file) / (1024 * 1024)
        
        print(f"{Fore.GREEN}[✓] Pi cache saved successfully!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Cache file: {cache_file} ({file_size_mb:.2f} MB){Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Precision: {len(pi_digits):,} digits{Style.RESET_ALL}")
    
    @staticmethod
    def _load_json(cache_file="pi_cache.json"):
        """
        Load Pi digits from legacy JSON cache (backward compatibility).
        
        Args:
            cache_file: Path to JSON cache file
            
        Returns:
            tuple: (pi_digits string, precision int) or (None, None) if failed
        """
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            pi_digits = cache_data["pi_digits"]
            precision = cache_data["metadata"]["precision"]
            
            print(f"{Fore.GREEN}[✓] Legacy cache loaded successfully!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Consider regenerating cache with --compute for better performance{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Precision: {len(pi_digits):,} digits{Style.RESET_ALL}")
            return pi_digits, precision
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to load legacy cache: {e}{Style.RESET_ALL}")
            return None, None
