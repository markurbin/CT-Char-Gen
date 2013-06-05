# Code samples: http://wiki.python.org/moin/SimplePrograms
# Traveller Book 4 & 5 character Generation using classes
# November 2012 - Mark Urbin
# "The Traveller game in all forms is owned by Far 
# Future Enterprises. Copyright 1977 - 2013 Far Future 
# Enterprises."
#
# R3 - Adding read UPP, Branch & Arm from config file
# Adding Book 5 'High Guard' support and moving more functions
# out to modules
#

import character as char
import show.raw as raw


def looper(loop):
    alive = 0
    dead = 0
    officer = 0
    alive_Officer = 0

    charlist = char.generate_multi(loop)
    count = 0
    for b4g in charlist:
        if b4g.alive:
           alive += 1
           if b4g.officer:
               alive_Officer += 1
        else:
            dead += 1
        if b4g.officer:
            officer += 1

    print 'alive = ', alive
    print 'dead = ', dead
    print 'officer = ', officer
    print 'Alive Officer = ', alive_Officer
#end of looper

def looper2(loop):
    
    outfile = open('random_chars.csv', 'a')
    charlist = char.generate_multi(loop)
    count = 0
    for b4g in charlist:
        if b4g.alive:
           s = 'Alive, '
        else:
            s = 'Dead, '
        s = s + ('%d, ' % b4g.age)
        if b4g.officer:
            s = s + 'Officer, ' +  b4g.military_rank()
        else:
            s = s + 'Enlisted, ' + b4g.military_rank()
        s = s + (', %d ' % b4g.term)
        #print s
        sprint.sprint(False, s,outfile)
    outfile.close()
#end of looper2


def single_Char():
    print '********************'
    b4g = char.generate('uppba.txt')
    
    print 'starting upp: '
    raw.print_init_upp(b4g)

    #Sb4g.arm = 'Commando'   #debug - set arm to Commando
        
    raw.print_history(b4g)
    print '+++++'
    raw.print_Char_Data(b4g)
#end of single_char

# Start of main code execution   

single_Char()

#looper(1000)

#looper2(20)


# Then the final character data, including the final UPP, any noble title, schools, etc.

