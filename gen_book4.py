#!/usr/bin/env python
# gen_book4.py
# Generates random Book 4 characters (Army or Marines)
# Usage: python gen_book4.py [number] [a|m]

import sys
import random
from character import B4Char
from utilities import print_character
from utilities import export_to_csv

def sanitize_count(arg):
    try:
        n = int(arg)
        if 1 <= n <= 5000:
            return n
    except:
        pass
    return 1


def sanitize_branch(arg):
    if not arg:
        return None
    arg = arg.lower().strip()
    if arg == 'a': return 'Imperial Army'
    if arg == 'm': return 'Imperial Marines'
    return None


def generate_book4_character(branch=None, noKill=True):
    grunt = B4Char()
    grunt.noKill = noKill
    if branch:
        grunt.branch = branch
    grunt.career()
    grunt.muster_out()
    return grunt


if __name__ == "__main__":
    args = sys.argv[1:]
    count = sanitize_count(args[0] if args else None)
    branch_choice = sanitize_branch(args[1] if len(args) > 1 else None)

    print(f"Generating {count} Book 4 character{'s' if count > 1 else ''}...")

    for i in range(count):
        char = generate_book4_character(branch=branch_choice, noKill=True)
        
        print(f"\n--- Character {i+1}/{count} ---")
        print_character(char)
        
        # ← This is the key line for rich Book 4 CSV
        export_to_csv(char, rich_book4=True)
        
        print(f"   → Added to book4_characters.csv")

    print(f"\n✅ Done! Generated {count} characters.")
    print("   Analysis command: python analyze_merc.py book4_characters.csv")


