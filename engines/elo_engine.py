import pandas as pd
import math

MEAN_ELO = 1500
ELO_WIDTH = 400
K_FACTOR = 32
HOME_ADVANTAGE_POINTS = 100

 
def calculate_elo(home_elo, away_elo, match_outcome, home_advantage):
    """
    Calculates Elo based on match outcome with logarithmic MoV adjustment.
    https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    """
    effective_home_elo = home_elo + home_advantage
    expected_home = 1 / (1 + 10 ** ((away_elo - effective_home_elo) / ELO_WIDTH))
    expected_away = 1- expected_home

    away_result = 1.0 - match_outcome[0]

    #logarithmig MoV adjustment on K value to reward high scoring teams
    adj_k = K_FACTOR * (1 + math.log(max(1, match_outcome[1])))
    
    new_home_elo = home_elo + adj_k * (match_outcome[0] - expected_home)
    new_away_elo = away_elo + adj_k * (away_result - expected_away)

    return new_home_elo, new_away_elo

def calculate_match_outcome(home_score, away_score):
    """
    Calculates match outcome based on scores.
    Home win = 1
    Away win = 0
    Draw = 0.5
    """
    if home_score > away_score:
        match_outcome = 1
    elif home_score == away_score:
        match_outcome = 0.5
    else:
        match_outcome = 0
    goal_diff = abs(home_score - away_score)
    return match_outcome, goal_diff

def check_advantage(home_team,match_country):
    """
    Checks if there is home advantage at play
    if home advantage give extra elo points to home team
    """
    if (home_team == match_country):
        return HOME_ADVANTAGE_POINTS
    return 0
    
def get_all_elos(filepath):
    df = pd.read_csv(filepath) 
    df.drop(labels = ["city","tournament","neutral"], inplace=True,axis = 1) 

    team_elos = {} 

    for index, row in df.iterrows(): 
        #Retrives Team data 
        home_team = row["home_team"] 
        away_team = row["away_team"] 
        home_score = row["home_score"] 
        away_score = row["away_score"] 
        #Retrives match data 
        match_country = row["country"] 

        # Checks if team is missing from Elo ladder and adds them if they are
        if home_team not in team_elos:
            team_elos[home_team] = MEAN_ELO
        if away_team not in team_elos:
            team_elos[away_team] = MEAN_ELO
        
        match_outcome = calculate_match_outcome(home_score, away_score)
        current_advantage = check_advantage(home_team,match_country)

        current_home_elo = team_elos[home_team]
        current_away_elo = team_elos[away_team]

        new_home_elo, new_away_elo = calculate_elo(current_home_elo, current_away_elo, match_outcome, current_advantage)

        team_elos[home_team] = new_home_elo
        team_elos[away_team] = new_away_elo

    return team_elos

    # Prints top 25 teams 
    #top_teams = sorted(team_elos.items(), key=lambda x: x[1], reverse=True)
    #print("\n--- Top 25 Teams ---")
    #for i in range(25):
    #    print(f"{i+1}. {top_teams[i][0]}: {top_teams[i][1]:.0f} poäng")