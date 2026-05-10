import tournament_logic
from engines.elo_engine import get_all_elos
from engines.team_stats_engine import calculate_team_strength
from match_simulator import simulate_matches, simulate_knockout_matches

def main():

    team_elos = get_all_elos("results.csv")
    team_stats, global_team_avg = calculate_team_strength("results.csv")

    champions = {}
    SIMULATIONS = 1_000_0

    print(f"Starting Monte Carlo simulation ({SIMULATIONS} tournaments)...")

    for i in range(SIMULATIONS):
        
        tournament_standings = tournament_logic.create_empty_standings(tournament_logic.world_cup_groups_2026)
        tournament_matches = tournament_logic.create_all_matches(tournament_logic.world_cup_groups_2026)
        
        # Group Stage
        results = simulate_matches(tournament_matches, team_stats, team_elos, global_team_avg)
        updated_table = tournament_logic.update_standings(results, tournament_standings)
        sorted_groups = tournament_logic.sort_groups(updated_table, tournament_logic.world_cup_groups_2026)
        advancing_teams = tournament_logic.advancing_teams(sorted_groups)

        # Knockout Stages
        r32_matches = tournament_logic.r32_generator(advancing_teams)
        r32_results = simulate_knockout_matches(r32_matches, team_stats, team_elos, global_team_avg)
        r32_advancing_teams = tournament_logic.knockout_advancing_teams(r32_results)

        r16_matches = tournament_logic.knockout_generator(r32_advancing_teams, tournament_logic.Round_of_16)
        r16_results = simulate_knockout_matches(r16_matches, team_stats, team_elos, global_team_avg)
        r16_advancing_teams = tournament_logic.knockout_advancing_teams(r16_results)

        r8_matches = tournament_logic.knockout_generator(r16_advancing_teams, tournament_logic.Round_of_8)
        r8_results = simulate_knockout_matches(r8_matches, team_stats, team_elos, global_team_avg)
        r8_advancing_teams = tournament_logic.knockout_advancing_teams(r8_results)
        
        r4_matches = tournament_logic.knockout_generator(r8_advancing_teams, tournament_logic.Round_of_4)
        r4_results = simulate_knockout_matches(r4_matches, team_stats, team_elos, global_team_avg)
        r4_advancing_teams = tournament_logic.knockout_advancing_teams(r4_results)
        
        r2_matches = tournament_logic.knockout_generator(r4_advancing_teams, tournament_logic.final)
        r2_results = simulate_knockout_matches(r2_matches, team_stats, team_elos, global_team_avg)
        
        # Extract the winning team from the final match dictionary
        winner_dict = tournament_logic.knockout_advancing_teams(r2_results)
        champion = list(winner_dict.values())[0]

        # Record tournament win
        if champion in champions:
            champions[champion] += 1
        else:
            champions[champion] = 1

        # Printing every 10000 simulations
        if (i + 1) % 10000 == 0:
            print(f"Simulated {i + 1} tournaments...")

    # display probabilities
    print("\n WINNER PROBABILITIES ")
    sorted_champions = sorted(champions.items(), key=lambda x: x[1], reverse=True)
    
    for team, wins in sorted_champions:
        probability = (wins / SIMULATIONS) * 100
        print(f"{team}: {probability:.1f}% ({wins} wins)")
    #print(results)
    #print(sorted_groups)
#    print(team_elos)

if __name__ == "__main__":
    main()