"""
Output Formatting Module

Handles JSON output formatting and file generation.
"""

import json
import re
from datetime import datetime


def save_results_json(matches, length, output_file, search_params):
    """
    Save bruteforce results to JSON file.
    
    Args:
        matches: List of (position, number) tuples
        length: Length of the numbers
        output_file: Path to output JSON file
        search_params: Dictionary of search parameters used
    """
    # Build results structure
    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "pi_precision": search_params.get("precision", 0) + 10,
            "search_parameters": search_params,
            "total_matches": len(matches)
        },
        "matches": []
    }
    
    # Add each match
    for i, (pos, number) in enumerate(matches):
        results["matches"].append({
            "match_number": i + 1,
            "number": number,
            "position": pos,
            "position_formatted": f"{pos:,}"
        })
    
    # Write to file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    from colorama import Fore, Style
    print(f"\n{Fore.GREEN}[✓] Results saved to: {output_file}{Style.RESET_ALL}")


def generate_filename(mode, **kwargs):
    """
    Generate output filename based on search parameters.
    
    Args:
        mode: Search mode (bruteforce, regex, range, etc.)
        **kwargs: Additional parameters specific to the mode
        
    Returns:
        str: Generated filename
    """
    if mode == "bruteforce":
        filename_parts = [f"results_len{kwargs['length']}"]
        if kwargs.get('starts_with'):
            filename_parts.append(f"start{kwargs['starts_with']}")
        if kwargs.get('ends_with'):
            filename_parts.append(f"end{kwargs['ends_with']}")
        if kwargs.get('contains'):
            filename_parts.append(f"contains{kwargs['contains']}")
        return "_".join(filename_parts) + ".json"
    
    elif mode == "regex":
        safe_regex = re.sub(r'[^\w\-]', '_', kwargs['pattern'])[:30]
        return f"results_regex_{safe_regex}.json"
    
    elif mode == "range":
        return f"results_range_{kwargs['min']}_{kwargs['max']}.json"
    
    elif mode == "multiple_patterns":
        return f"results_len{kwargs['length']}_multipattern.json"
    
    elif mode == "direct_search":
        return f"results_search_{kwargs['target']}.json"
    
    else:
        return "results.json"
