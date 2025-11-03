#!/usr/bin/env python3
"""
Convert BibTeX file to JSON format for PS-Wiki API

Usage:
    python database/pyscripts/bib2json.py --input assets/bibliography/papers.bib --output database/build/bib.json --validate --pretty
"""

import json
import argparse
import re
from typing import Dict, List, Any
from pathlib import Path


def parse_bibtex_file(filepath: str) -> Dict[str, Dict[str, Any]]:
    """
    Parse a BibTeX file and convert to structured JSON format.
    
    Args:
        filepath: Path to the .bib file
        
    Returns:
        Dictionary mapping citation keys to entry data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = {}
    
    # Pattern to match BibTeX entries
    # Matches: @type{key, field = {value}, ...}
    entry_pattern = r'@(\w+)\{([^,]+),\s*(.*?)\n\}'
    
    # Fields to exclude from the JSON output
    excluded_fields = {'abstract', 'bibtex_show', 'abbr'}
    
    for match in re.finditer(entry_pattern, content, re.DOTALL):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        fields_str = match.group(3)
        
        # Parse fields
        fields = {}
        field_pattern = r'(\w+)\s*=\s*\{([^}]*)\}'
        
        for field_match in re.finditer(field_pattern, fields_str, re.DOTALL):
            field_name = field_match.group(1).strip()
            field_value = field_match.group(2).strip()
            
            # Skip excluded fields
            if field_name in excluded_fields:
                continue
            
            # Clean up multiline values
            field_value = re.sub(r'\s+', ' ', field_value)
            fields[field_name] = field_value
        
        # Reconstruct BibTeX entry for the 'bibtex' field (without excluded fields)
        bibtex_lines = [f"@{entry_type}{{{key},"]
        for field_name, field_value in fields.items():
            bibtex_lines.append(f"  {field_name} = {{{field_value}}},")
        if bibtex_lines[-1].endswith(','):
            bibtex_lines[-1] = bibtex_lines[-1].rstrip(',')  # Remove trailing comma
        bibtex_lines.append("}")
        
        entries[key] = {
            "key": key,
            "type": entry_type,
            "fields": fields,
            "bibtex": "\n".join(bibtex_lines)
        }
    
    return entries


def validate_entries(entries: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    Validate BibTeX entries and return list of warnings.
    
    Args:
        entries: Dictionary of parsed entries
        
    Returns:
        List of validation warnings
    """
    warnings = []
    
    required_fields = {
        'article': ['author', 'title', 'journal', 'year'],
        'book': ['author', 'title', 'publisher', 'year'],
        'online': ['title', 'url', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'techreport': ['author', 'title', 'institution', 'year']
    }
    
    for key, entry in entries.items():
        entry_type = entry['type']
        fields = entry['fields']
        
        # Check for required fields
        if entry_type in required_fields:
            for req_field in required_fields[entry_type]:
                if req_field not in fields:
                    warnings.append(
                        f"Entry '{key}' of type '{entry_type}' missing required field '{req_field}'"
                    )
        
        # Check for URL accessibility
        if 'url' in fields and not fields['url'].startswith(('http://', 'https://')):
            warnings.append(f"Entry '{key}' has invalid URL: {fields['url']}")
    
    return warnings


def main():
    parser = argparse.ArgumentParser(
        description='Convert BibTeX file to JSON for PS-Wiki API'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input BibTeX file path'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output JSON file path'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate entries and show warnings'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output'
    )
    
    args = parser.parse_args()
    
    # Parse BibTeX file
    print(f"Parsing {args.input}...")
    entries = parse_bibtex_file(args.input)
    print(f"Found {len(entries)} entries")
    
    # Validate if requested
    if args.validate:
        warnings = validate_entries(entries)
        if warnings:
            print("\nValidation warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        else:
            print("\nAll entries valid!")
    
    # Write JSON output
    output_data = {
        "metadata": {
            "total_entries": len(entries),
            "source_file": Path(args.input).name,
            "entry_types": list(set(e['type'] for e in entries.values()))
        },
        "entries": entries
    }
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        if args.pretty:
            # Custom JSON formatting with line breaks between entries
            f.write('{\n')
            f.write('  "metadata": ')
            json.dump(output_data["metadata"], f, indent=4, ensure_ascii=False)
            f.write(',\n  "entries": {')
            
            # Write each entry with a blank line separator
            entry_items = list(output_data["entries"].items())
            for i, (key, entry) in enumerate(entry_items):
                f.write(f'    "{key}": ')
                entry_json = json.dumps(entry, indent=6, ensure_ascii=False)
                # Adjust indentation for nested content
                entry_json = entry_json.replace('\n', '\n    ')
                f.write(entry_json.rstrip())
                
                # Add comma if not the last entry
                if i < len(entry_items) - 1:
                    f.write(',\n\n')  # Double newline for spacing between entries
                else:
                    f.write('\n')
            
            f.write('  }\n')
            f.write('}\n')
        else:
            json.dump(output_data, f, ensure_ascii=False)
    
    print(f"\nWritten to {args.output}")
    print(f"Entry types: {', '.join(output_data['metadata']['entry_types'])}")


if __name__ == '__main__':
    main()
