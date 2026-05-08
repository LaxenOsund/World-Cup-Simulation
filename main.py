from tournament_logic import create_empty_standings, world_cup_groups_2026, create_all_matches
from elo_engine import get_all_elos
from team_stats_engine import calculate_team_strength
from match_simulator import simulate_games


def main():
    
    team_elos = get_all_elos("results.csv")

    team_stats, global_team_avg = calculate_team_strength("results.csv")

    tournament_standings = create_empty_standings(world_cup_groups_2026)
    #print(tournament_standings["Sweden"])
    tournament_matches = create_all_matches(world_cup_groups_2026)
    #print(tournament_matches)
    results = simulate_games(tournament_matches, team_stats, team_elos, global_team_avg)

    for match in results:
        group_name = match[0]
        team_a = match[1]
        team_b = match[2]
        goals_a = match[3]
        goals_b = match[4]
        
        print(f"[{group_name}] {team_a} {goals_a} - {goals_b} {team_b}")


if __name__ == "__main__":
    main()