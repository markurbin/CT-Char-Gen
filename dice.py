from random import randint

def dice(sides=6, qty=1):
	"Rolls the specified number of dice (default 1 six-sided die) and returns the total."
	total = 0
        for i in range(qty):
		total = total + randint(1, sides)
        return total

def coin_flip():
	"Flips a coin, returning True for heads and False for tails."
	return (1 == randint(0, 1))
