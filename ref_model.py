import csv
from pickle import TRUE

class ind_game:
    def __init__(self, name, date, away, home, fouls, foul_diff, chief):
        self.name = name
        self.date = date
        self.away = away
        self.home = home
        self.fouls = fouls
        self.foul_diff = foul_diff
        self.chief = chief
        
    def print_name(self):
        print(self.name)

    def get_name(self):
        return self.name

    def print_date(self):
        print(self.date)

    def get_date(self):
        return self.date

print("\nHello world \n \n This is the start of the NBA Referee Stat Tracker \n \n \n \n")

ref_db_hm = {}
with open('NBA_Referee.csv','r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for x in csv_reader:
        if x['Crew Chief'] in ref_db_hm:
            print(ref_db_hm[x['Crew Chief']].get_name() + " was crew chief on " +ref_db_hm[x['Crew Chief']].get_date())
        else:
            ref_db_hm[x['Crew Chief']] = ind_game(x['Crew Chief'], x['Date'], x['AWAY'], x['HOME'], x['Total Fouls'], x['Ref Diff'], TRUE)
        #print(x['Crew Chief'] + "      " + x['Referee'] + "         " + x['Umpire'])

