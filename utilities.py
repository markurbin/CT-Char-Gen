# utilities.py
# Shared helper functions for Traveller character generators

import csv
import os
import json

def print_character(grunt, filename=None):
    """Print character to console and append to the correct file"""
    output = "=" * 70 + "\n"
    
    # Death notification (classic Traveller style)
    if not grunt.alive:
        output += "!!! Character died during creation !!!\n\n"

    # UPP in hex
    upp_values = [grunt.upp.str, grunt.upp.dex, grunt.upp.end, grunt.upp.int, grunt.upp.edu, grunt.upp.soc]
    upp_hex = ''.join(f"{v:X}" for v in upp_values)
    output += f"UPP: {upp_hex}\n"
    
    output += f"Service: {grunt.branch} / {grunt.arm}\n"
    output += f"Rank: {grunt.military_rank()}\n"
    output += f"Age: {grunt.age}   Terms Served: {grunt.term}\n"

    # === Muster Out Benefits (reliable display) ===
    muster_items = []
    
    # Primary source: unified muster_loot (preferred)
    if hasattr(grunt, 'muster_loot') and grunt.muster_loot:
        muster_items = [str(item) for item in grunt.muster_loot if item]
    
    # Fallback: scan history for any missed benefits
    if not muster_items:
        for line in grunt.history:
            if "Muster Benefit:" in line:
                benefit = line.split("Muster Benefit:", 1)[1].strip()
                if benefit and benefit not in muster_items:
                    muster_items.append(benefit)

    if muster_items:
        output += f"Muster Out: {', '.join(muster_items)}\n"

    output += f"Cash: Cr{grunt.cash:,}\n"

    if grunt.skills:
        skill_list = [f"{k}-{v}" for k, v in sorted(grunt.skills.items())]
        output += "Skills: " + ", ".join(skill_list[:15]) + "\n"
        if len(grunt.skills) > 15:
            output += f"     ... and {len(grunt.skills)-15} more\n"

    # Combat Ribbons (Book 4) - show between Skills and Decorations
    if hasattr(grunt, 'ribbons') and grunt.ribbons:
        ribbon_list = ", ".join(grunt.ribbons)
        output += f"Combat Ribbons: {ribbon_list}\n"

    if grunt.decorations:
        output += "Decorations: " + ", ".join(grunt.decorations) + "\n"

    output += "\n--- Career History ---\n"
    for line in grunt.history:
        output += "  " + line + "\n"
    output += "=" * 70 + "\n\n"

    print(output)

    # Determine correct filename
    if filename is None:
        if 'Army' in grunt.branch:
            filename = "B4_army.txt"
        else:
            filename = "B4_marines.txt"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(output)

def export_to_csv(grunt, csv_filename=None, rich_book4=False):
    """
    Export character data to CSV.
    
    - If rich_book4=True  → writes rich structured data to book4_characters.csv (for analyze_merc.py)
    - Otherwise           → keeps original Book 5 / legacy behavior (separate files per branch)
    """
    if rich_book4:
        return export_to_rich_book4_csv(grunt)

    # === ORIGINAL LEGACY BEHAVIOR (Book 5 / Navy) ===
    if csv_filename is None:
        if 'Army' in grunt.branch:
            csv_filename = "B4_army.csv"
        elif 'Marine' in grunt.branch:
            csv_filename = "B4_marines.csv"
        else:
            csv_filename = "B5_navy.csv"

    upp_hex = ''.join(f"{v:X}" for v in [
        grunt.upp.str, grunt.upp.dex, grunt.upp.end,
        grunt.upp.int, grunt.upp.edu, grunt.upp.soc
    ])

    skill_str = ", ".join(f"{k}-{v}" for k, v in sorted(grunt.skills.items()))
    dec_str = ", ".join(grunt.decorations) if getattr(grunt, 'decorations', None) else ""

    is_officer = "Officer" if getattr(grunt, 'officer', False) else "Enlisted"
    rank_num = getattr(grunt, 'rank', 0)
    display_rank = rank_num + 1                     # 1-based for CSV
    rank_code = f"O{display_rank}" if is_officer == "Officer" else f"E{display_rank}"

    row = {
        'UPP': upp_hex,
        'Branch': grunt.branch,
        'Arm': getattr(grunt, 'arm', ''),
        'Rank': grunt.military_rank(),
        'Rank_Code': rank_code,
        'Officer_Enlisted': is_officer,
        'Age': grunt.age,
        'Terms': grunt.term,
        'Cash': grunt.cash,
        'Alive': grunt.alive,

        # Education paths (existing flags)
        'Applied_Naval_Academy': getattr(grunt, 'academy_fail', False) or getattr(grunt, 'academy', False),
        'Graduated_Naval_Academy': getattr(grunt, 'academy', False),
        'Graduated_Flight_School': 'Flight' in getattr(grunt, 'schools', []),
        'Graduated_Medical_School': getattr(grunt, 'medschool', False),
        'Graduated_College': getattr(grunt, 'college', False),
        'Navy_Officer_Training_Corps': getattr(grunt, 'notc', False),

        'Skills': skill_str,
        'Decorations': dec_str,
        'Died_During_Creation': not grunt.alive and len(grunt.history) < 10
    }

    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def export_to_rich_book4_csv(grunt, csv_filename="book4_characters.csv"):
    """Rich CSV specifically for Book 4 analysis"""
    upp_hex = ''.join(f"{v:X}" for v in [
        grunt.upp.str, grunt.upp.dex, grunt.upp.end,
        grunt.upp.int, grunt.upp.edu, grunt.upp.soc
    ])

    skills_json = json.dumps(dict(grunt.skills), ensure_ascii=False)
    dec_str = "|".join(getattr(grunt, 'decorations', []))
    ribbon_str = "|".join(getattr(grunt, 'ribbons', []))

    row = {
        'alive': grunt.alive,
        'age': grunt.age,
        'term': grunt.term,
        'branch': grunt.branch,
        'arm': getattr(grunt, 'arm', 'Unknown'),
        'officer': getattr(grunt, 'officer', False),
        'rank': grunt.rank + 1,                     # 1-based
        'rank_name': grunt.military_rank(),
        'upp_hex': upp_hex,
        'str': grunt.upp.str,
        'dex': grunt.upp.dex,
        'end': grunt.upp.end,
        'int': grunt.upp.int,
        'edu': grunt.upp.edu,
        'soc': grunt.upp.soc,
        'cash': grunt.cash,
        'r_pay': getattr(grunt, 'r_pay', 0),
        'skills_json': skills_json,
        'skills_text': ", ".join(f"{k}-{v}" for k, v in sorted(grunt.skills.items())),
        'decorations': dec_str,
        'ribbons': ribbon_str,
        'history_count': len(grunt.history)
    }

    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row) 



   
