# promotions.py
# Traveller Book 4 Promotions, Medals, and Ribbons

def award_medal(grunt, medal, ua):
    """Award a medal and record it."""
    s = f'{medal} awarded in {ua}'
    grunt.decorations.append(s)
    grunt.history.append(s)


def get_medal(grunt, roll, target, ua):
    """Award appropriate medal based on how well the decoration roll succeeded."""
    margin = roll - target
    if margin >= 6:
        award_medal(grunt, "SEH", ua)      # Star of Extreme Heroism
    elif margin >= 3:
        award_medal(grunt, "MCG", ua)      # Meritorious Conduct in Ground Combat
    else:
        award_medal(grunt, "MCUF", ua)     # Meritorious Conduct Under Fire


def award_ribbon(grunt, ga, ua):
    """Award combat ribbon (normal or command version)."""
    if grunt.officer and ga == 'Command':
        ribbon_name = f'{ua} Combat Command Ribbon'
    else:
        ribbon_name = f'{ua} Combat Ribbon'
    
    grunt.ribbons.append(ribbon_name)
    grunt.history.append(ribbon_name)


def promote(grunt):
    """Main promotion dispatcher."""
    if grunt.officer:
        officer(grunt)
    else:
        enlisted(grunt)

def enlisted(grunt):
    """Promote enlisted character."""
    if grunt.officer:
        officer(grunt)
        return False

    grunt.rank += 1
    if grunt.rank > 8:
        grunt.rank = 8
        grunt.history.append('No further promotion available (max rank reached)')
        return True
    else:
        s = f'Promoted to {grunt.military_rank()}'
        grunt.history.append(s)
        return True

def officer(grunt):
    """Promote officer character."""
    if not grunt.officer:
        enlisted(grunt)
        return False

    if grunt.rank >= 9:
        grunt.history.append('No further promotion available (already at General rank)')
        return True

    grunt.rank += 1
    grunt.promote_this_term = True
    s = f'Promoted to {grunt.military_rank()}'
    grunt.history.append(s)
    return True
