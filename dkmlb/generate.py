import csv
import requests
from bs4 import BeautifulSoup
from scipy import stats

abbrev_dict = {}
slate_dict = {}
proj_pitchers = {} #name, hand, whip, lavg, lxfip, ravg, rxfip
proj_lineups = {} #team, PA, ops, ld, last7ops, lwoba, rwoba, salary, position
vegastt_list = []
vegastt = {}

#translate all abbrevs to team names
with open('abbrevs.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    for line in csvreader:
        brevteam = line[0].split("|")
        # print(brevteam)
        abbrev_dict[brevteam[0]] = brevteam[1]

#get specified slate
team_count = 0
with open('slate.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    away_team = ""
    for row in csvreader:
        #even row
        if team_count % 2 == 0:
            # print(row[0])
            away_team = abbrev_dict[row[0]]
            vegastt[away_team] = float(row[1])
            vegastt_list.append(float(row[1]))
        #odd row
        elif team_count % 2 == 1:
            home_team = abbrev_dict[row[0]]
            vegastt[home_team] = float(row[1])
            vegastt_list.append(float(row[1]))
            slate_dict[away_team] = home_team
            slate_dict[home_team] = away_team
        team_count += 1

#get tonights opposing pitchers stats for batters
whip_list = []
xfip_list = []
relief_list = []
with open('projected_pitchers.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[2] in slate_dict.keys():
            pitcher_stats = [line[0], line[1], float(line[11]),float(line[20])]
            whip_list.append(float(line[11]))
            xfip_list.append(float(line[20]))
            # print (line[2], pitcher_stats)
            proj_pitchers[line[2]] = pitcher_stats

with open('relief.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[0] in slate_dict.keys():
            pitcher_stats = [float(line[16])]
            relief_list.append(float(line[16]))
            proj_pitchers[line[0]].extend(pitcher_stats)

# with open('vsleft_pitchers.csv','r') as csvfile:
#     csvreader = csv.reader(csvfile)
#     header = next(csvreader)
#     for line in csvreader:
#         if line[1] in proj_pitchers.keys():
#             pitcher_stats = [float(line[9]), float(line[14])]
#             proj_pitchers[line[1]].extend(pitcher_stats)

# with open('vsright_pitchers.csv','r') as csvfile:
#     csvreader = csv.reader(csvfile)
#     header = next(csvreader)
#     for line in csvreader:
#         if line[1] in proj_pitchers.keys():
#             pitcher_stats = [float(line[9]), float(line[14])]
#             proj_pitchers[line[1]].extend(pitcher_stats)

# for key,val in proj_pitchers.items():
#     print(key,val)

# scrape roto grinders for lineups and put in dict
lineup_url = "https://rotogrinders.com/lineups/mlb?site=draftkings"
doc = requests.get(lineup_url)
soup = BeautifulSoup(doc.text, 'html.parser')

#missed players (they're in starting lineups but either fangraphs or DK misspelled name)
# -2 means DKSalaries missed
# 0 means fangraphs batters.csv missed
# -1 means last7ops missed

# for players where fangraph spells differently than roto lineups
# changes the players name to fangraph spelling (value in dict) on in proj_lineups
special_name_dict = {}
special_name_dict['Albert Almora'] = "Albert Almora Jr."
special_name_dict['Tyler France'] = "Ty France"
special_name_dict['Yulieski Gurriel'] = "Yuli Gurriel"
special_name_dict['Lourdes Gurriel'] = "Lourdes Gurriel Jr."
special_name_dict['Stevie Wilkerson'] = "Steve Wilkerson"
special_name_dict['Pete Alonso'] = "Peter Alonso"
special_name_dict['Ronald Acuna'] = "Ronald Acuna Jr."
special_name_dict['Jackie Bradley'] = "Jackie Bradley Jr."
special_name_dict['Nick Castellanos'] = "Nicholas Castellanos"
special_name_dict['Vladimir Guerrero Jr'] = "Vladimir Guerrero Jr."
special_name_dict['Richard Martin'] = "Richie Martin"
special_name_dict['Jakob Bauers'] = "Jake Bauers"
special_name_dict['Matthew Beaty'] = "Matt Beaty"

# for players whose team is --- on fangraphs
special_team_dict = {}
special_team_dict['Tyler Austin'] = "Giants"
special_team_dict['Wilmer Font'] = "Mets"
special_team_dict['Gerardo Parra'] = "Nationals"
special_team_dict['Kendrys Morales'] = "Yankees"
special_team_dict['Blake Swihart'] = "Diamondbacks"
special_team_dict['Kevin Pillar'] = "Giants"
special_team_dict['Erik Kratz'] = "Rays"
special_team_dict['Travis d\'Arnaud'] = "Rays"
special_team_dict['Aaron Altherr'] = "Giants"
special_team_dict['Mike Wright Jr.'] = "Mariners"
special_team_dict['Shawn Armstrong'] = "Orioles"
special_team_dict['Chris Stratton'] = "Giants"
special_team_dict['Austin Adams'] = "Twins"

# for players where DK Salaries spells differently than roto/fangraph
# checks proj_lineups w second one as key
dk_name_dict = {}
dk_name_dict['Pete Alonso'] = "Peter Alonso"
dk_name_dict['Kike Hernandez'] = "Enrique Hernandez"
dk_name_dict['Stevie Wilkerson'] = "Steve Wilkerson"
dk_name_dict['Shin-soo Choo'] = "Shin-Soo Choo"

starters = soup.find_all('a', class_='player-popup')
lineup_count = -1
for elt in starters:
    name = elt.get_text()
    if name in special_name_dict.keys():
        name = special_name_dict[name]
    proj_lineups[name] = []

ops_list = []
ld_list = []
last7ops_list = []
left_woba_list = []
right_woba_list = []

with open('batters.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        #needs at least 20 PA's
        if int(line[2]) < 10:
            continue
        if line[0] in proj_lineups.keys():
            team_name = line[1]
            # if line[0] == "Kendrys Morales":
            #     print("HELLO")
            if line[0] in special_team_dict.keys():
                # print(line[0])
                team_name = special_team_dict[line[0]]
            batter_stats = [team_name, line[2], float(line[9])]
            ops_list.append(float(line[9]))
            proj_lineups[line[0]].extend(batter_stats)

with open('batters2.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[0] in proj_lineups.keys():
            batter_stats = [float(line[4].split(" ")[0])/100]
            ld_list.append(float(line[4].split(" ")[0])/100)
            proj_lineups[line[0]].extend(batter_stats)

with open('last7batters.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[0] in proj_lineups.keys():
            # needs at least 9 PA's this week or we use his season OPS
            if int(line[2]) < 4:
                if len(proj_lineups[line[0]]) >= 4:
                    proj_lineups[line[0]].append(proj_lineups[line[0]][2])
            else:
                batter_stats = [float(line[9])]
                last7ops_list.append(float(line[9]))
                proj_lineups[line[0]].extend(batter_stats)

with open('left_batters.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[0] in proj_lineups.keys():
            batter_stats = [float(line[15])]
            left_woba_list.append(float(line[15]))
            proj_lineups[line[0]].extend(batter_stats)

with open('right_batters.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[0] in proj_lineups.keys():
            batter_stats = [float(line[15])]
            right_woba_list.append(float(line[15]))
            proj_lineups[line[0]].extend(batter_stats)

with open('DKSalaries.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        name = line[2]
        if name in dk_name_dict.keys():
            name = dk_name_dict[name]
        if name in proj_lineups.keys():
            batter_stats = [float(line[5]), line[0]]
            proj_lineups[name].extend(batter_stats)

with open('hot_batters.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[0] in proj_lineups.keys():
            if len(proj_lineups[line[0]]) >= 3:
                bigger = max(proj_lineups[line[0]][2], float(line[17]))
                proj_lineups[line[0]][2] = str(bigger) + " HOT"
            
with open('cold_batters.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for line in csvreader:
        if line[0] in proj_lineups.keys():
            if len(proj_lineups[line[0]]) >= 3:
                smaller = proj_lineups[line[0]][2]
                #smaller = min(proj_lineups[line[0]][2], float(line[17]))
                proj_lineups[line[0]][2] = str(smaller) + " COLD" 
            
#missed players (they're in starting lineups but either fangraphs or DK misspelled name)
# -2 means DKSalaries missed
# 0 means fangraphs batters.csv missed
# -1 means last7ops missed
for key in proj_lineups.keys():
    if len(proj_lineups[key]) == 0:
        print(key, proj_lineups[key])
    elif proj_lineups[key][0] in slate_dict.keys() and len(proj_lineups[key]) < 9:
        print(key, len(proj_lineups[key]), proj_lineups[key])

gen_csv = True
if gen_csv:
    with open('batter_rank.csv','w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        header = ["Player", "Position", "Team", "PA", "OPS","OPS%", "LD", "LD%", "last7OPS", "last7OPS%", "Opp Pitcher", "Vegas TT", "Vegas Pts", "Opp WHIP", "WHIP Pts", "Opp xFIP", "xFIP Pts", "Opp Relief", "Rel Pts", "Opp Hand", "Hand wOBA", "Hand wOBA%", "wOBA Diff", "Salary", "Score", "Value"]
        wr.writerow(header)
        for player in proj_lineups.keys():
            # if player == "Kendrys Morales":
            #     print(player, len(proj_lineups[player]), proj_lineups[player])
            if len(proj_lineups[player]) < 9:
                continue
            if proj_lineups[player][0] in slate_dict.keys():
                player_stats = []
                position = proj_lineups[player][8]
                team = proj_lineups[player][0]
                pa = proj_lineups[player][1]
                ops = proj_lineups[player][2]
                real_ops = str(ops).split(" ")
                true_ops = float(real_ops[0])
                if len(real_ops) > 1 and real_ops[1] == "HOT":
                    true_ops = float(real_ops[0]) * 1.25
                ops_ = round(stats.percentileofscore(ops_list,true_ops),1)
                ld = proj_lineups[player][3]
                ld_ = round(stats.percentileofscore(ld_list,ld),1)
                last7ops = proj_lineups[player][4]
                last7_ = round(stats.percentileofscore(last7ops_list,last7ops),1)
                lwoba = proj_lineups[player][5]
                lwoba_ = round(stats.percentileofscore(left_woba_list,lwoba),1)
                rwoba = proj_lineups[player][6]
                rwoba_ = round(stats.percentileofscore(right_woba_list,rwoba),1)
                salary = proj_lineups[player][7]
                opposing_team = slate_dict[team]
                if opposing_team not in proj_pitchers.keys():
                    continue
                opp_pitcher = proj_pitchers[opposing_team][0].split(" ")[1]
                vegastotal = vegastt[team]
                avgvegas = sum(vegastt_list)/len(vegastt_list)
                vegas_ = round((vegastotal - avgvegas) * 20,1)
                oppwhip = proj_pitchers[opposing_team][2]
                avgwhip = sum(whip_list)/len(whip_list)
                oppwhip_ = round((oppwhip - avgwhip) * 30,1)
                opphand = proj_pitchers[opposing_team][1]
                oppxfip = proj_pitchers[opposing_team][3]
                avgxfip = sum(xfip_list)/len(xfip_list)
                oppxfip_ = round((oppxfip - avgxfip) * 30,1)
                opprelief = proj_pitchers[opposing_team][4]
                avgrelief = sum(relief_list)/len(relief_list)
                opprelief_ = round((opprelief - avgrelief) * 15,1)
                player_stats.append(player)
                player_stats.append(position)
                player_stats.append(team)
                player_stats.append(pa)
                player_stats.append(ops)
                player_stats.append(ops_)
                player_stats.append(ld)
                player_stats.append(ld_)
                player_stats.append(last7ops)
                player_stats.append(last7_)
                player_stats.append(opp_pitcher)
                player_stats.append(vegastotal)
                player_stats.append(vegas_)
                player_stats.append(oppwhip)
                player_stats.append(oppwhip_)
                player_stats.append(oppxfip)
                player_stats.append(oppxfip_)
                player_stats.append(opprelief)
                player_stats.append(opprelief_)
                player_stats.append(opphand)
                woba = 0
                woba_ = 0
                wobadiff = 0
                if opphand == "L":
                    woba = lwoba
                    woba_ = lwoba_
                    wobadiff = lwoba - rwoba
                elif opphand == "R":
                    woba = rwoba
                    woba_ = rwoba_
                    wobadiff = rwoba - lwoba
                player_stats.append(woba)
                player_stats.append(woba_)
                player_stats.append(wobadiff)
                player_stats.append(salary)
                score = ops_ + (0.25 * ld_) + last7_ + vegas_ + oppwhip_ + oppxfip_ + opprelief_ + (0.5 * woba_) + (75 * wobadiff)
                score = round(score, 0)
                player_stats.append(score)
                value = round(score*100/salary,2)
                player_stats.append(value)
                wr.writerow(player_stats)

    with open('pitcher_rank.csv', 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        header = ["Player", "Salary", "Team", "Opp", "Ceiling", "Floor", "Points", "Value"]
        wr.writerow(header)
        with open('mlb_pitchers.csv','r') as csvfile:
            csvreader = csv.reader(csvfile)
            for line in csvreader:
                team_name = abbrev_dict[line[2]]
                if team_name not in slate_dict.keys():
                    continue
                val = round(float(line[7])/float(line[1]) * 1000,2)
                new_csv_line = [line[0],line[1],team_name, line[4], line[5], line[6], line[7], val]
                wr.writerow(new_csv_line)


















