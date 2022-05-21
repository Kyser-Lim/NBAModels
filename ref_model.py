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
    return (as_crew_chief+as_crew2+as_crew3)/3.0



print("\nHello world \n \n This is the start of the NBA Referee Stat Tracker \n \n")

ref_db_hm = {} #this is the hashmap

#This has successfully created the database
with open('NBA_Referee.csv','r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    counter = 0
    for x in csv_reader:
        if x['Crew Chief'] in ref_db_hm:
            ref_db_hm[x['Crew Chief']].append(ind_game(x['Crew Chief'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], True))
#print(x['Crew Chief']+ " was a crew chief on " +ref_db_hm[x['Crew Chief']][1].get_date())
        else:
#print("Making a new crew chief:" + x["Crew Chief"])
            ref_db_hm[x['Crew Chief']] = []
            ref_db_hm[x['Crew Chief']].append(ind_game(x['Crew Chief'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], True))

        if x['Referee'] in ref_db_hm:
            ref_db_hm[x['Referee']].append(ind_game(x['Referee'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'],False))
        else:
#print("Making a new ref:" + x["Referee"])
            ref_db_hm[x['Referee']] = []
            ref_db_hm[x['Referee']].append(ind_game(x['Referee'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], False))

        if x['Umpire'] in ref_db_hm:
            ref_db_hm[x['Umpire']].append(ind_game(x['Umpire'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'],False))
        else:
#print("Making a new umpire:" + x["Umpire"])
            ref_db_hm[x['Umpire']] = []
            ref_db_hm[x['Umpire']].append(ind_game(x['Umpire'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Real Ref Diff'], False))
        
#print(x['Crew Chief']+ " was a crew chief on " +ref_db_hm[x['Crew Chief']][len(ref_db_hm[x['Crew Chief']])-1].get_date())
#ref_name = raw_input("Please type the name of the referee: ")
#last_games = raw_input("Please type the amount of games most recent: ")
#a, b = calculate_foul_avg(ref_name, ref_db_hm[ref_name], int(last_games))

result = input("Would you like the stats of an individual referee (type 1) or average of a referee rotation (type 2)? ")

if result == 1:
    ref_name = raw_input("Please type the name of the referee: ")
    last_games = input("Please type the amount of games most recent: ")
    crew_chief, not_crew_chief = calculate_foul_avg(ref_name, ref_db_hm[ref_name], last_games)
    if crew_chief != 0:
        print("As Crew Chief, "+ref_name + " has averaged " + str(crew_chief) + " over the last " + str(last_games) + " games.")
    if not_crew_chief != 0:
        print("As Crew, "+ ref_name + " has averaged " + str(not_crew_chief) + " over the last " + str(last_games) + " games.")

if result == 2:
    crew_chief_input = raw_input("Please type the name of the crew chief: ")
    umpire = raw_input("Please type the name of the second crew: ")
    referee = raw_input("Please type the name of the third crew: ")
    last_games = input("Please type the amount of games most recent: ")
    print("They average "+ str(ref_rotation_foul_avg(ref_db_hm, crew_chief_input, umpire, referee, last_games)) + " fouls over the last " + str(last_games) + " games.")
