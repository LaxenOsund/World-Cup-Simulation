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
def create_empty_standings(groups_dict):
    """
    Takes a dictionary with groups of teams and creates an empty standings dictionary
    """
    stat_dict = {}
    for group in world_cup_groups_2026.values():
        for team in group:
                stat_dict[team] = {"Pts": 0, "GF": 0, "GA": 0, "GD": 0}
    return stat_dict




def create_all_matches(groups_dict):
    matches = []
    for group_name, teams in world_cup_groups_2026.items():
        group_matches = list(combinations(teams, 2))
        for match in group_matches:
            team_a = match[0]
            team_b = match[1]
            matches.append((group_name,team_a, team_b))
    return matches

#print(create_all_matches(world_cup_groups_2026))

