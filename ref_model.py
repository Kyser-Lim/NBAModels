import csv

class ind_game:
    def __init__(self, name, date, away, home, fouls, foul_diff, chief):
        self.name = name
        self.date = date
        self.away = away
        self.home = home
        self.fouls = float(fouls)
        self.foul_diff = float(foul_diff)
        self.chief = chief
        
    def print_name(self):
        print(self.name)

    def get_name(self):
        return self.name

    def print_date(self):
        print(self.date)

    def get_date(self):
        return self.date

    def get_fouls(self):
        return self.fouls
    
    def is_chief(self):
        return self.chief

    def get_diff(self):
        return self.foul_diff

#Calculate a referee's average fouls called in x of their last games
def calculate_foul_avg(name, games_array, last_x_games):
    fouls_as_chief = 0
    fouls_not_chief = 0
    games_as_chief = 0
    chief_avg = 0
    not_chief_avg = 0

    if last_x_games> len(games_array):
        last_x_games = len(games_array)

    for x in games_array[0:last_x_games]:        
        if x.is_chief():
#print("is chief")
            fouls_as_chief = fouls_as_chief + x.get_fouls()
            games_as_chief = games_as_chief+1
        else:
#print("is not chief")
            fouls_not_chief = fouls_not_chief + x.get_fouls()

    if games_as_chief > 0:
        chief_avg = fouls_as_chief/games_as_chief
        #print("As Crew Chief, "+name + " has averaged " + str(chief_avg) + " over the last " + str(last_x_games) + " games.")

    if games_as_chief != last_x_games:
        not_chief_avg = fouls_not_chief/(last_x_games-games_as_chief)
        #print("As Crew, "+name + " has averaged " + str(not_chief_avg) + " over the last " + str(last_x_games-games_as_chief) + " games.")

    return chief_avg, not_chief_avg

def ref_rotation_foul_avg(db, crew_chief, umpire, referee, last_x_games):
    as_crew_chief, as_crew = calculate_foul_avg(crew_chief, db[crew_chief], last_x_games) 
    as_crew_chief2, as_crew2 = calculate_foul_avg(umpire, db[umpire], last_x_games)
    as_crew_chief3, as_crew3 = calculate_foul_avg(referee, db[referee], last_x_games)

    if as_crew_chief == 0:
        if as_crew == 0:
            print("This referee has not reffed a game before!!!")
            use1 = 0
        else:
            use1 = as_crew
    else:
        use1 = as_crew_chief

    if as_crew2 == 0:
        if as_crew_chief2 == 0:
            print("This referee has not reffed a game before!!!")
            use2 = 0
        else:
            use2 = as_crew_chief2
    else:
        use2 = as_crew2

    if as_crew3 == 0:
        if as_crew_chief3 == 0:
            print("This referee has not reffed a game before!!!")
            use3 = 0
        else:
            use3 = as_crew_chief3
    else:
        use3 = as_crew3

    return (use1+use2+use3)/3.0

#Calculate a referee's average foul differential called in x of their last games
def calculate_foul_diff(name, games_array, last_x_games):
    diff_as_chief = 0
    diff_not_chief = 0
    games_as_chief = 0
    chief_avg = 0
    not_chief_avg = 0

    if last_x_games> len(games_array):
        last_x_games = len(games_array)

    for x in games_array[0:last_x_games]:        
        if x.is_chief():
            #print("is chief")
            diff_as_chief = diff_as_chief + x.get_diff()
            games_as_chief = games_as_chief+1
        else:
            #print("is not chief")
            diff_not_chief = diff_not_chief + x.get_diff()

    if games_as_chief > 0:
        chief_avg = diff_as_chief/games_as_chief
        #print("As Crew Chief, "+name + " has averaged " + str(chief_avg) + " over the last " + str(last_x_games) + " games.")

    if games_as_chief != last_x_games:
        not_chief_avg = diff_not_chief/(last_x_games-games_as_chief)
        #print("As Crew, "+name + " has averaged " + str(not_chief_avg) + " over the last " + str(last_x_games-games_as_chief) + " games.")

    return chief_avg, not_chief_avg

def ref_rotation_foul_diff_avg(db, crew_chief, umpire, referee, last_x_games):
    as_crew_chief, as_crew = calculate_foul_diff(crew_chief, db[crew_chief], last_x_games) 
    as_crew_chief2, as_crew2 = calculate_foul_diff(umpire, db[umpire], last_x_games)
    as_crew_chief3, as_crew3 = calculate_foul_diff(referee, db[referee], last_x_games)




    if as_crew_chief == 0:
        if as_crew == 0:
            if len(db[crew_chief]) == 0:
                print("Referee 1 has not reffed a game before!!!")
            use1 = 0
        else:
            use1 = as_crew
    else:
        use1 = as_crew_chief

    if as_crew2 == 0:
        if as_crew_chief2 == 0:
            if len(db[umpire]) == 0:
                print("Referee 2 has not reffed a game before!!!")
            use2 = 0
        else:
            use2 = as_crew_chief2
    else:
        use2 = as_crew2

    if as_crew3 == 0:
        if as_crew_chief3 == 0:
            if len(db[referee]) == 0:
                print("Referee 3 has not reffed a game before!!!")
            use3 = 0
        else:
            use3 = as_crew_chief3
    else:
        use3 = as_crew3
   # print(str(use1) + "    " + str(use2) + "     " + str(use3))
    return (use1+use2+use3)

print("\nHello world \n \n This is the start of the NBA Referee Stat Tracker \n \n")

ref_db_hm = {} #this is the hashmap

#This has successfully created the database
with open('NBA_Referee.csv','r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    counter = 0
    for x in csv_reader:
        if x['Crew Chief'] in ref_db_hm:
            ref_db_hm[x['Crew Chief']].append(ind_game(x['Crew Chief'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], True))
        else:
            ref_db_hm[x['Crew Chief']] = []
            ref_db_hm[x['Crew Chief']].append(ind_game(x['Crew Chief'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], True))

        if x['Referee'] in ref_db_hm:
            ref_db_hm[x['Referee']].append(ind_game(x['Referee'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'],False))
        else:
            ref_db_hm[x['Referee']] = []
            ref_db_hm[x['Referee']].append(ind_game(x['Referee'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], False))

        if x['Umpire'] in ref_db_hm:
            ref_db_hm[x['Umpire']].append(ind_game(x['Umpire'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'],False))
        else:
            ref_db_hm[x['Umpire']] = []
            ref_db_hm[x['Umpire']].append(ind_game(x['Umpire'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], False))
        
#print(x['Crew Chief']+ " was a crew chief on " +ref_db_hm[x['Crew Chief']][len(ref_db_hm[x['Crew Chief']])-1].get_date())
#ref_name = raw_input("Please type the name of the referee: ")
#last_games = raw_input("Please type the amount of games most recent: ")
#a, b = calculate_foul_avg(ref_name, ref_db_hm[ref_name], int(last_games))

result = input("Would you like: \n 1. Individual referee stats\n 2. Referee rotation stats\n")

if result == 1:
    ref_name = raw_input("Please type the name of the referee: ")
    last_games = input("Please type the amount of games most recent: ")
    if last_games > len(ref_db_hm[ref_name]):
        last_games = len(ref_db_hm[ref_name])
    crew_chief, not_crew_chief = calculate_foul_avg(ref_name, ref_db_hm[ref_name], last_games)
    if crew_chief != 0:
        print("As Crew Chief, "+ref_name + " has averaged " + str(crew_chief) + " fouls over the last " + str(last_games) + " games.")
    if not_crew_chief != 0:
        print("As Crew, "+ ref_name + " has averaged " + str(not_crew_chief) + " fouls over the last " + str(last_games) + " games.")

#    print(not_crew_chief)
    crew_chief, not_crew_chief = calculate_foul_diff(ref_name, ref_db_hm[ref_name], last_games)
#    print(not_crew_chief)
#    if len(ref_db_hm[ref_name]) != 0:
    print("As Crew Chief, "+ref_name + " has averaged " + str(crew_chief) + " foul differential over the last " + str(last_games) + " games.")
 #   if not_crew_chief != 0:
    print("As Crew, "+ ref_name + " has averaged " + str(not_crew_chief) + " foul differential over the last " + str(last_games) + " games.")

if result == 2:
    crew_chief_input = raw_input("Please type the name of the crew chief: ")
    umpire = raw_input("Please type the name of the second crew: ")
    referee = raw_input("Please type the name of the third crew: ")
    last_games = input("Please type the amount of games most recent: ")

    if len(ref_db_hm[crew_chief_input]) < last_games or len(ref_db_hm[umpire]) < last_games or len(ref_db_hm[referee]) < last_games:
        last_games = max(len(ref_db_hm[crew_chief_input]), len(ref_db_hm[umpire]), len(ref_db_hm[referee]))
    print("They average "+ str(ref_rotation_foul_avg(ref_db_hm, crew_chief_input, umpire, referee, last_games)) + " fouls over the last " + str(last_games) + " games.")
    print("They average "+ str(ref_rotation_foul_diff_avg(ref_db_hm, crew_chief_input, umpire, referee, last_games)) + " foul differential over the last " + str(last_games) + " games.")

 
#need to add logic that allows cross reference between ref foul history and a team or with home/away