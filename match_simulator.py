#lambda = average global goals * Team_A_AS * Team_B_DS
import numpy as np

def simulate_games(gamelist, team_stats,team_elos, AVERAGE_GOALS):
    ELO_WIDTH = 400
    results = []
    for game in gamelist:
        group = game[0]
        team_a = game[1]
        team_b = game[2]

        team_a_elo = team_elos.get(team_a, 1500)
        team_a_as = team_stats.get(team_a, {}).get("AS", 1.0)
        team_a_ds = team_stats.get(team_a, {}).get("DS", 1.0)

        team_b_elo = team_elos.get(team_b, 1500)
        team_b_as = team_stats.get(team_b, {}).get("AS", 1.0)
        team_b_ds = team_stats.get(team_b, {}).get("DS", 1.0)

        #To calculate for home advantage
        if team_a in ["Mexico", "Canada", "United States"]:
            team_a_elo += 100
        if team_b in ["Mexico", "Canada", "United States"]:
            team_b_elo += 100
        
        expected_a = 1 / (1 + 10 ** ((team_a_elo - team_b_elo) / ELO_WIDTH))
        expected_b = 1- expected_a

        TOTAL_MATCH_GOALS = AVERAGE_GOALS * 2
        lambda_a = (expected_a * TOTAL_MATCH_GOALS * team_a_as * team_b_ds)
        goals_a = np.random.poisson(lambda_a)

        lambda_b = (expected_b * TOTAL_MATCH_GOALS * team_b_as * team_a_ds)
        goals_b = np.random.poisson(lambda_b)

        results.append((group, team_a, team_b, goals_a, goals_b))
    return results