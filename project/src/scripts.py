from copy import copy

def setup_labels(z, num_teams):
    '''
    create dict of team pair - z value eg. { "12" : z_1, "13" : z_2 ...}

    z - iterable: 
    num_teams - int: 
    '''
    
    combos = []

    for i in range(0, num_teams - 1 ):
        for j in range(i, num_teams):
            if i != j:
                combos.append( str(i) + str(j) )
    return dict( zip(combos, z ) )



def ha_assign(timetable, z):

    assert isinstance(timetable,np.ndarray), "Timetable must be of type np.ndarray"

    ha_assignment = (np.ones_like(timetable) * -1)   # -1 for debug
    num_teams = timetable.shape[0]
    num_games = 2 * (num_teams-1)
    
    assert num_teams * (num_teams  - 1)/2 == len(z), "z vector not compatible with number of teams"
    z_labeled = setup_labels(z, num_teams)      
    
    for t_row in range( num_teams ):
        for slot in range( num_games ):
            team_1 = copy(t_row)
            team_2 = timetable[t_row, slot]

            #print(team_1, team_2)
            if team_1 > team_2:
                team_1, team_2 = team_2, team_1     # slot is in the second half of the tournament team1 is greater than team2, switch them
                label = str(team_1) + str(team_2)   # create label for lookup
                #print(label + "if")
                if slot >= (num_teams - 1):       # slot is in the second half of the tournament
                    a = z_labeled[ label ]      # 'a' is the 1 or 0 home assignment value,      y_t',s' = z
                
                else:                           # slot is in the first half of the tournament
                    a = 1 - z_labeled[ label ]                                                # y_t',s  = 1-z
                

            else:                                   # the order of teams matches the label
                label = str(team_1) + str(team_2)
                #print(label + "else")
                
                if slot >= (num_teams - 1):       # slot is in the second half of the tournament
                    a =  1 - z_labeled[ label ]                                                # y_t,s' = 1-z
                
                else:                           # slot in the first half of the tournament
                    a = z_labeled[ label ]                                                    # y_t,s  = z
                
            
            ha_assignment[t_row, slot] = a 

    return ha_assignment


def count_breaks(timetable, z):
    ha = ha_assign(timetable, z)

    breaks = 0
    for t_row in range(ha.shape[0]):
        for slot in range(ha.shape[1]-1):
            breaks += ha[t_row, slot] * ha[t_row, slot + 1] + (1 - ha[t_row,slot]) * ( 1 - ha[t_row, slot + 1])

    return breaks