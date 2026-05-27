#!/usr/bin/env python3
"""
Convert BibTeX file to JSON format for PS-Wiki API

Usage:
    python database/pyscripts/bib2json.py --input assets/bibliography/papers.bib --output database/build/bib.json --validate --pretty
"""

import json
import argparse
from typing import Dict, List, Any
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

_EXCLUDED_FIELDS = {"abstract", "bibtex_show", "abbr"}
_BIBTEX_RESERVED = {"ENTRYTYPE", "ID"}


def parse_bibtex_file(filepath: str) -> Dict[str, Dict[str, Any]]:
    """
    Parse a BibTeX file and convert to structured JSON format.

    Args:
        filepath: Path to the .bib file

    Returns:
        Dictionary mapping citation keys to entry data
    """
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False

    with open(filepath, "r", encoding="utf-8") as f:
        bib_database = bibtexparser.load(f, parser=parser)

    entries = {}
    for entry in bib_database.entries:
        key = entry["ID"]
        entry_type = entry["ENTRYTYPE"].lower()

        fields = {
            k: v
            for k, v in entry.items()
            if k not in _BIBTEX_RESERVED and k not in _EXCLUDED_FIELDS
        }

        bibtex_lines = [f"@{entry_type}{{{key},"]
        for field_name, field_value in fields.items():
            bibtex_lines.append(f"  {field_name} = {{{field_value}}},")
        if bibtex_lines[-1].endswith(","):
            bibtex_lines[-1] = bibtex_lines[-1].rstrip(",")
        bibtex_lines.append("}")

        entries[key] = {
            "key": key,
            "type": entry_type,
            "fields": fields,
            "bibtex": "\n".join(bibtex_lines),
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
    all_entries = list(set(e['type'] for e in entries.values()))
    sorted_entry_types = sorted(all_entries)
    output_data = {
        "metadata": {
            "total_entries": len(entries),
            "source_file": Path(args.input).name,
            "entry_types": sorted_entry_types
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
