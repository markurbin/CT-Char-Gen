from random import randint

def dice(qty=1, sides=6):
    """
    Traveller RPG dice roller - d6 by default.
    
    Usage:
        dice()      → 1d6   (returns 1-6)
        dice(2)     → 2d6   (returns 2-12)   ← most common
        dice(3)     → 3d6
        dice(1, 8)  → 1d8   (if you ever need non-d6)
        dice(6, 2)  → 2d6   (explicit form still works)
    """
    # If only one argument is passed and it's small, treat it as number of d6s
    # This makes dice(2) mean 2d6 - the Traveller standard
    if sides == 6 and qty <= 10:   # reasonable Traveller range
        # qty is actually the number of dice
        num_dice = qty
        die_sides = 6
    else:
        # Explicit call like dice(6, 2) or dice(1, 8)
        num_dice = qty
        die_sides = sides

    total = 0
    for _ in range(num_dice):
        total += randint(1, die_sides)
    return total


def dice2():
    """Quick 2d6 - very common in Traveller"""
    return dice(2)


def coin_flip():
    """Returns True for heads"""
    return randint(0, 1) == 1


def droplow(qty=2, sides=6):
    """Roll qty+1 dice, drop the lowest, return sum"""
    if qty < 1:
        return 0
    rolls = [randint(1, sides) for _ in range(qty + 1)]
    rolls.remove(min(rolls))
    return sum(rolls)

