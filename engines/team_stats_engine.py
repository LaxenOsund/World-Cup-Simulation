import pandas as pd

def calculate_team_strength(file_path):

    """
    GF = Goals For
    GA = Goals Against
    GP = Games Played
    AS = Attacking Strength
    DS = Defensive Strength
    
    """
    df = pd.read_csv(file_path)
    
    # Calculates global average
    total_goals = df["home_score"].sum() + df["away_score"].sum()
    total_matches = len(df)
    global_team_avg = total_goals / (total_matches * 2)

    team_stats = {}

    # Creates a unique list with all teams
    all_teams = pd.concat([df["home_team"], df["away_team"]]).unique()

    # Calculates stats
    for team in all_teams:
        # Filters games for the team
        home_games = df[df["home_team"] == team]
        away_games = df[df["away_team"] == team]
        
        # Calculates matches
        games_played = len(home_games) + len(away_games)
        
        if games_played == 0:
            continue
            
        # Calculates GF
        goals_for = home_games["home_score"].sum() + away_games["away_score"].sum()
        
        # Calculats GA
        goals_against = home_games["away_score"].sum() + away_games["home_score"].sum()
        
        # Calculates averages
        team_stats[team] = {
            "GP": games_played,
            "AS": (goals_for / games_played) / global_team_avg,
            "DS": (goals_against / games_played) / global_team_avg
        }

    return team_stats, global_team_avg


if __name__ == "__main__":
    print("Testing for Sweden")
    stats = calculate_team_strength("results.csv")
    
    print("\n--- TEST: Sweden ---")
    print(f"Matches: {stats['Sweden']['GP']}")
    print(f"Attack (AS): {stats['Sweden']['AS']:.2f}")
    print(f"Defense (DS): {stats['Sweden']['DS']:.2f}")