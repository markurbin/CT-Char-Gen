#!/usr/bin/env python
# Code samples: http://wiki.python.org/moin/SimplePrograms
# Traveller Book 4 & 5 character Generation using classes
# November 2012 - 2015 - Mark Urbin
# "The Traveller game in all forms is owned by Far 
# Future Enterprises. Copyright 1977 - 2015 Far Future 
# Enterprises."
#
# R3 - Adding read UPP, Branch & Arm from config file
# Adding Book 5 'High Guard' support and moving more functions
# out to modules
#

import sys
import character as char
import show.raw as raw

def main(genmode='single', genqty=10):
	# Start of main code execution
	if type(genqty)==str:
		try:
			genqty = int(genqty)
			if genqty<0: raise ValueError
		except ValueError:
			print '"%s" is not a valid quantity...' % str(genqty)
			show_usage()
			return
	if genmode=='single':
		single_Char()
	elif genmode=='summary':
		looper(genqty)
	elif genmode=='list':
		looper2(genqty, 'random_chars.csv', 'a')
	elif genmode=='help' or genmode=='--help':
		show_usage()
	else:
		print '"%s" is not a valid mode...' % genmode
		show_usage()

def show_usage():
    print """
      Usage: %s [single]
        Generates and displays a single character (default mode)
        
      Usage: %s {list|summary} [quantity]
        Generates a list of characters, either dumping a list to a CSV file or else printing a summary.
        The quantity to generate defaults to 10.
             
    """ % (__file__, __file__)

def looper(loop):
    alive = 0
    dead = 0
    officer = 0
    alive_Officer = 0

    charlist = char.generate_multi(loop)
    #count = 0
    for grunt in charlist:
        if grunt.alive:
           alive += 1
           if grunt.officer:
               alive_Officer += 1
        else:
            dead += 1
        if grunt.officer:
            officer += 1

    print 'alive = ', alive
    print 'dead = ', dead
    print 'officer = ', officer
    print 'Alive Officer = ', alive_Officer
#end of looper

def looper2(loop, filename, fmode):
    
    outfile = open(filename, fmode)
    charlist = char.generate_multi(loop)
    #count = 0
    for grunt in charlist:
        if grunt.alive:
           s = 'Alive, '
        else:
            s = 'Dead, '
        s = s + ('%d, ' % grunt.age)
        if grunt.officer:
            s = s + 'Officer, ' +  grunt.military_rank()
        else:
            s = s + 'Enlisted, ' + grunt.military_rank()
        s = s + (', %d ' % grunt.term)
        #print s
        sprint.sprint(False, s,outfile)
    outfile.close()
#end of looper2


def single_Char():
    print '********************'
    grunt = char.generate('uppba.txt')
    
    print 'starting upp: '
    raw.print_init_upp(grunt)
        
    raw.print_history(grunt)
    print '+++++'
    raw.print_Char_Data(grunt)
#end of single_char


A = sys.argv[1:]
main(*A)
