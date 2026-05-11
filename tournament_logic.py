from itertools import combinations
world_cup_groups_2026 = {
    "Group A": ["Mexico", "Czech Republic", "South Korea", "South Africa"],
    "Group B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "Group C": ["Brazil", "Haiti", "Morocco", "Scotland"],
    "Group D": ["United States", "Australia", "Paraguay", "Turkey"],
    "Group E": ["Ivory Coast", "Curaçao", "Ecuador", "Germany"],
    "Group F": ["Japan", "Netherlands", "Sweden", "Tunisia"],
    "Group G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "Group H": ["Cape Verde", "Saudi Arabia", "Spain", "Uruguay"],
    "Group I": ["France", "Iraq", "Norway", "Senegal"],
    "Group J": ["Algeria", "Argentina", "Austria", "Jordan"],
    "Group K": ["Colombia", "DR Congo", "Portugal", "Uzbekistan"],
    "Group L": ["Croatia", "England", "Ghana", "Panama"]
}

Round_of_32 = [
    ("2A","2B",73),("1C","2F",76),("1F","2C",75),("2E","2I",78),
    ("1H","2J",84),("2K","2L",83),("2D","2G",88),("1J","2H",86),
    
    ("1E",["A","B","C","D","F"],74),
    ("1I",["C","D","F","G","H"],77),
    ("1A",["C","E","F","H","I"],79),
    ("1L",["E","H","I","J","K"],80),
    ("1G",["A","E","H","I","J"],82),
    ("1D",["B","E","F","I","J"],81),
    ("1B",["E","F","G","I","J"],85),
    ("1K",["D","E","I","J","L"],87)
]

Round_of_16 = [
    (73,75,90),(74,77,89),(76,78,91),(79,80,92),
    (83,84,93),(81,82,94),(86,88,95),(85,87,96)
]

Round_of_8 = [
    (89,90,97),(93,94,98),(91,92,99),(95,96,100)
]

Round_of_4 = [
    (97,98,101),(99,100,102)
]

final = [
    (101,102,104)
]
def create_empty_standings(groups_dict):
    """
    Takes a dictionary with groups of teams and creates an empty standings dictionary
    """
    stat_dict = {}
    for group in groups_dict.values():
        for team in group:
                stat_dict[team] = {"Pts": 0, "GF": 0, "GA": 0, "GD": 0}
    return stat_dict

def create_all_matches(groups_dict):
    """
    Takes a dictionary with groups of teams and creates every match combination
    """
    matches = []
    for group_name, teams in groups_dict.items():
        group_matches = list(combinations(teams, 2))
        for match in group_matches:
            team_a = match[0]
            team_b = match[1]
            matches.append((group_name,team_a, team_b))
    return matches

def update_standings(result_list, standings_dict):
    """
    Takes list with all completed matches and standings dictionary and calculates group standings 
    result_list[0] = Group Name
    result_list[1] = Team A
    result_list[2] = Team B
    result_list[3] = Score A
    result_list[4] = Score B
    """
    for match in result_list:
        group, team_a, team_b, score_a, score_b = match

        standings_dict[team_a]["GF"] += score_a
        standings_dict[team_a]["GA"] += score_b
        standings_dict[team_a]["GD"] += score_a - score_b

        standings_dict[team_b]["GF"] += score_b
        standings_dict[team_b]["GA"] += score_a
        standings_dict[team_b]["GD"] += score_b - score_a
        
        if score_a > score_b:
            standings_dict[team_a]["Pts"] += 3
        elif score_b > score_a:
            standings_dict[team_b]["Pts"] += 3
        else:
            standings_dict[team_a]["Pts"] += 1
            standings_dict[team_b]["Pts"] += 1

    return standings_dict

def sort_groups(standings_dict, group_dict):
    """
    Takes dictionary with unsorted standings and dictionary with the groups and sorts groups based on 1. Pts, 2. GD and 3. GF
    returns sorted groups
    """
    fin_groups = {}
    for group, team_list in group_dict.items():
        group_data = []
        for team in team_list:
            group_data.append((team, standings_dict[team]))
        sorted_group = sorted(group_data, key=lambda x :(
            x[1]["Pts"],
            x[1]["GD"],
            x[1]["GF"]
        ),reverse=True)
        fin_groups[group] = sorted_group
    return fin_groups

def advancing_teams(group_standings_dict):
    """
    Takes a dictionary of all groups and their standings and calculates the 32 teams that goes trhough to r32
    returns the 32 teams
    """
    advancing_teams = []
    third_teams = []
    for group, team_list in group_standings_dict.items():
        for placement in range(3):
            if placement != 2:
                advancing_teams.append([str(placement + 1) + group[6:],team_list[placement]])
            else:
                third_teams.append([str(placement + 1) + group[6:],team_list[placement]])
    
    sorted_thirds = sorted(third_teams,key=lambda x :(
        x[1][1]["Pts"],
        x[1][1]["GD"],
        x[1][1]["GF"]
    ),reverse=True)

    best_threes = sorted_thirds[:8]
    advancing_teams.extend(best_threes)
    return advancing_teams

def r32_generator(advanced_teams,round_template = Round_of_32):
    """
    Takes advancing teams aswell as round template and creates a list with tuples of all the matches in r32
    """
    team_dict = {}
    threes_list = []

    for team_info in advanced_teams:
        team_id = team_info[0]
        team_name = team_info[1][0]

        if "3" in team_id:
            threes_list.append(team_info)
        else:
            team_dict[team_id] = team_name
    r32_matches = []
    for match in round_template:
        id_a = match[0]
        team_a_name = team_dict[id_a]
        match_id = match[2]

        id_b = match[1]
        if isinstance(id_b, list):
            allowed_groups = id_b
            for three in threes_list:
                three_id = three[0]
                three_group = three_id[1]
                #Checks if allowed matchup
                if three_group in allowed_groups:
                    #Allowed matchup found! 
                    team_b_name = three[1][0]
                    #Remove "booked" team from list and stop searching for another team
                    threes_list.remove(three)
                    break
        else:
            team_b_name = team_dict[id_b]
        r32_matches.append((match_id,team_a_name,team_b_name))
    return r32_matches
        
def knockout_advancing_teams(match_list):
    """
    Takes list containging (match_id,team_a,team_b,score_a,score_b)
    and returns the winner together with the match_id to easily put into next round

    """
    advancing_teams={}
    for match in match_list:
        match_id ,team_a,team_b,team_a_score, team_b_score = match
        if team_a_score > team_b_score:
            advancing_teams[match_id] = team_a
        else:
            advancing_teams[match_id] = team_b
    return advancing_teams

def knockout_generator(advanced_teams,round_template):
    """
    Takes advanced teams and round templates for the r16 QF SF and Final and returns list of matches to be simulated
    """
    new_matches = []
    for match in round_template:
        match_id_a = match[0]
        match_id_b = match[1]
        new_match_id = match[2]

        team_a = advanced_teams[match_id_a]
        team_b = advanced_teams[match_id_b]

        new_matches.append((new_match_id,team_a,team_b))
    return new_matches