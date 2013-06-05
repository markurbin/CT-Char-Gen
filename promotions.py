def award_medal(grunt, medal, ua):
    s = '%s awarded in %s' % (medal, ua)
    grunt.decorations.append(s)
    grunt.history.append(s)

def get_medal(grunt, roll, target, ua):
    if (roll - target) >= 6:
        award_medal(grunt, "SEH", ua)
    elif (3 <= (roll - target) < 6):
        award_medal(grunt, "MCG", ua)
    elif (roll - target) < 3:
        award_medal(grunt, "MCUF", ua)

def award_ribbon(grunt, ga, ua):
    ribbon_type = '%s Combat Ribbon'
    if grunt.officer and (ga=='Command'):
        ribbon_type = '%s Combat Command Ribbon'
    ribbon_name = ribbon_type % ua
    grunt.ribbons.append(ribbon_name)
    grunt.history.append(ribbon_name)

def promote(grunt):
    if grunt.officer:
        officer(grunt)
    else:
        enlisted(grunt)

def enlisted(grunt):
    if grunt.officer:
        officer(grunt)
        return False
    grunt.rank += 1
    if grunt.rank > 8:
        grunt.rank = 8
        s = 'No promotion avilable until after OCS' 
        grunt.history.append(s)
        return True
    else:
        s = 'Promoted to %s' % grunt.military_rank()
        grunt.history.append(s)
        return True
#end enlisted

def officer(grunt):
    if (False == grunt.officer):   #error condition, should never hit this
        enlisted(grunt)
        return False
    if grunt.rank == 9:
        grunt.rank = 9
        s = 'No further promotion availiable.' 
        grunt.history.append(s)
    else:
        grunt.rank += 1
        grunt.promote_this_term = True
        s = 'Promoted to %s' % grunt.military_rank()
        grunt.history.append(s)
    return True
#end of officer
