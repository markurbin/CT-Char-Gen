#!/usr/bin/env python
# gen_book5.py
# Generates random Imperial Navy (Book 5 High Guard) characters

import sys
from character import B4Char
from utilities import print_character   # Shared printing + file output
from utilities import export_to_csv

def sanitize_count(arg):
    try:
        n = int(arg)
        if 1 <= n <= 5000:
            return n
    except (ValueError, TypeError):
        pass
    return 1


def generate_book5_character(noKill=True):
    grunt = B4Char()
    grunt.noKill = noKill
    grunt.branch = 'Imperial Navy'
    grunt.arm = 'Line'  # added 4 June 2026
    #grunt.apply_skill("Default")       # Was used in debugging
    grunt.career()
    grunt.muster_out()
    return grunt


if __name__ == "__main__":
    args = sys.argv[1:]
    count = sanitize_count(args[0] if args else None)

    print(f"Generating {count} Imperial Navy character{'s' if count > 1 else ''}...\n")

    for i in range(count):
        char = generate_book5_character(noKill=True)
        print(f"Character {i+1}/{count}")
        print_character(char, filename="book5_chars.txt")
        export_to_csv(char)