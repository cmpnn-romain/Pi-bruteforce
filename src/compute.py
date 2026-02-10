"""
Pi Computation Module

High-performance implementation of the Chudnovsky algorithm using Binary Splitting.
Supports parallel execution and optional gmpy2 optimization.
"""

import sys
import math
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from colorama import Fore, Style

# Try to import gmpy2 for maximum performance
try:
    import gmpy2
    from gmpy2 import mpz
    
    # Configure gmpy2
    gmpy2.get_context().precision = 100  # Initial low precision, scaled dynamically
    HAS_GMPY2 = True
except ImportError:
    HAS_GMPY2 = False
    # Fallback to Python's built-in int (which is arbitrary precision)
    mpz = int


class PiComputer:
    """Computes Pi to arbitrary precision using optimized Chudnovsky algorithm."""
    
    @staticmethod
    def compute(digits):
        """
        Compute Pi to the specified number of digits.
        
        Args:
            digits: Number of decimal places of Pi to compute
            
        Returns:
            str: Pi digits as a string (without decimal point)
        """
        print(f"{Fore.YELLOW}[*] Computing Pi to {digits:,} digits...{Style.RESET_ALL}")
        
        if HAS_GMPY2:
            print(f"{Fore.CYAN}[*] Using gmpy2 for maximum speed 🚀{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}[*] Using optimized Python integers (install gmpy2 for 10x speedup){Style.RESET_ALL}")
            # Increase integer string conversion limit for large Pi digits
            try:
                sys.set_int_max_str_digits(digits + 10000)
            except AttributeError:
                pass  # Older Python versions don't have this limit
        
        try:
            # Calculate number of terms required
            # Each term adds ~14.18 digits
            terms = int(digits / 14.1816474627254776555) + 1
            
            print(f"{Fore.CYAN}[*] Algorithm: Chudnovsky ({terms:,} terms){Style.RESET_ALL}")
            
            # Determine parallelism
            cpu_count = multiprocessing.cpu_count()
            
            # Binary splitting
            if cpu_count > 1 and terms > 1000:
                print(f"{Fore.CYAN}[*] Using parallel binary splitting on {cpu_count} cores{Style.RESET_ALL}")
                P, Q, T = PiComputer._parallel_binary_split(0, terms, cpu_count)
            else:
                P, Q, T = PiComputer._binary_split(0, terms)
            
            # Final calculation: pi = Q * 426880 * sqrt(10005) / T
            print(f"{Fore.YELLOW}[*] Performing final division and conversion...{Style.RESET_ALL}")
            
            # Constants
            C = 426880
            D = 10005
            
            if HAS_GMPY2:
                # Use gmpy2 for high-precision division and sqrt
                ctx = gmpy2.get_context()
                # Set precision to required bits (approx 3.32 bits per digit) with buffer
                ctx.precision = int(digits * 3.32192809488736234787) + 100
                
                # Sqrt(10005)
                sqrt_D = gmpy2.sqrt(D)
                
                # Final calculation
                pi = (Q * C * sqrt_D) / T
                
                # Convert to string
                # gmpy2 formats efficiently
                pi_str = "{:.{}f}".format(pi, digits)
                pi_str = pi_str.replace('.', '')[:digits]
                
            else:
                # Optimized pure Python integer arithmetic
                # Calculate required precision for fixed-point arithmetic
                # We need `digits` decimal places, so multiply by 10^digits
                
                # Integer square root of D * 10^(2*digits)
                # sqrt(D) * 10^digits ~= isqrt(D * 10^(2*digits))
                shift = digits + 10  # extra precision
                sqrt_D_shifted = math.isqrt(D * (10**(2*shift)))
                
                # Final calculation in fixed point
                # Pi ~= (Q * C * sqrt_D) / T
                # We want result * 10^digits
                # (Q * C * (sqrt_D * 10^shift)) // T
                
                numerator = Q * C * sqrt_D_shifted
                pi_val = numerator // T
                
                # Convert to string
                pi_str = str(pi_val)
                # Truncate extra precision digits
                pi_str = pi_str[:digits]
            
            print(f"{Fore.GREEN}[✓] Pi computed successfully! ({len(pi_str):,} digits){Style.RESET_ALL}")
            return pi_str
            
        except Exception as e:
            print(f"{Fore.RED}[✗] Computation failed: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Fallback to mpmath (slower)...{Style.RESET_ALL}")
            return PiComputer._fallback_mpmath(digits)

    @staticmethod
    def _binary_split(a, b):
        """
        Compute terms for range [a, b) using binary splitting.
        
        Args:
            a: Start index (inclusive)
            b: End index (exclusive)
            
        Returns:
            P, Q, T tuple
        """
        if b - a == 1:
            # Base case: calculate single term
            # P(a, a+1) = -(6a - 1)(2a - 1)(6a - 5)
            # Q(a, a+1) = 10939058860032000 * a^3
            # T(a, a+1) = P(a, a+1) * (545140134a + 13591409)
            
            if a == 0:
                P = mpz(1)
                Q = mpz(1)
            else:
                P = mpz((6*a - 1) * (2*a - 1) * (6*a - 5))
                # The series alternates signs, handling that here
                if HAS_GMPY2:
                    P = -P
                else:
                    P = -int(P) # Ensure Python int behaves correctly with signs
                    
                Q = mpz(10939058860032000 * a**3)
                
            T = P * (545140134*a + 13591409)
            
            return P, Q, T
        
        else:
            # Recursive step
            m = (a + b) // 2
            
            P_am, Q_am, T_am = PiComputer._binary_split(a, m)
            P_mb, Q_mb, T_mb = PiComputer._binary_split(m, b)
            
            # Merge results
            # P(a, b) = P(a, m) * P(m, b)
            # Q(a, b) = Q(a, m) * Q(m, b)
            # T(a, b) = Q(m, b) * T(a, m) + P(a, m) * T(m, b)
            
            P = P_am * P_mb
            Q = Q_am * Q_mb
            T = Q_mb * T_am + P_am * T_mb
            
            return P, Q, T

    @staticmethod
    def _parallel_binary_split(a, b, threads=4):
        """
        Perform binary splitting in chunks using parallelism at the top level.
        """
        chunk_size = (b - a) // threads
        ranges = []
        
        for i in range(threads):
            start = a + i * chunk_size
            end = a + (i + 1) * chunk_size if i < threads - 1 else b
            ranges.append((start, end))
        
        with ProcessPoolExecutor(max_workers=threads) as executor:
            if HAS_GMPY2:
                # ProcessPoolExecutor with gmpy2 objects might need care with pickling
                # Ideally, we pass simple ints arguments and return simple types if possible
                # But mpz objects effectively pickle fine in modern versions.
                # If issues arise, we can convert back/forth to str/int at boundary.
                pass
            
            # Map the helper stub that unpacks arguments
            results = list(executor.map(PiComputer._binary_split_wrapper, ranges))
        
        # Combine results sequentially
        # This is fast because we're combining ~threads large numbers
        
        # Start with first chunk
        P_total, Q_total, T_total = results[0]
        
        for i in range(1, len(results)):
            P_next, Q_next, T_next = results[i]
            
            # Merge logic same as recursive step
            T_total = Q_next * T_total + P_total * T_next
            P_total = P_total * P_next
            Q_total = Q_total * Q_next
            
        return P_total, Q_total, T_total

    @staticmethod
    def _binary_split_wrapper(args):
        """Wrapper for ProcessPoolExecutor"""
        return PiComputer._binary_split(*args)

    @staticmethod
    def _fallback_mpmath(digits):
        """Fallback to mpmath if optimization fails."""
        from mpmath import mp
        mp.dps = digits + 10
        pi_val = mp.pi
        return str(pi_val).replace('.', '')
