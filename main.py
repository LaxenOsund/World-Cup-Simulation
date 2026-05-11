import tournament_logic
from engines.elo_engine import get_all_elos
from engines.team_stats_engine import calculate_team_strength
from match_simulator import simulate_matches, simulate_matches
import visualize

def main():

    team_elos = get_all_elos("results.csv")
    team_stats, global_team_avg = calculate_team_strength("results.csv")

    champions = {}
    SIMULATIONS = 30_00

    print(f"Starting Monte Carlo simulation ({SIMULATIONS} tournaments)...")

    for i in range(SIMULATIONS):
        
        tournament_standings = tournament_logic.create_empty_standings(tournament_logic.world_cup_groups_2026)
        tournament_matches = tournament_logic.create_all_matches(tournament_logic.world_cup_groups_2026)
        
        # Group Stage
        results = simulate_matches(tournament_matches, team_stats, team_elos, global_team_avg,False)
        updated_table = tournament_logic.update_standings(results, tournament_standings)
        sorted_groups = tournament_logic.sort_groups(updated_table, tournament_logic.world_cup_groups_2026)
        advancing_teams = tournament_logic.advancing_teams(sorted_groups)

        # Knockout Stages

        knockout_rounds = [
            tournament_logic.Round_of_16,
            tournament_logic.Round_of_8,
            tournament_logic.Round_of_4,
            tournament_logic.final
        ]

        r32_matches = tournament_logic.r32_generator(advancing_teams)
        r32_results = simulate_matches(r32_matches, team_stats, team_elos, global_team_avg,True)
        current_advancing_teams = tournament_logic.knockout_advancing_teams(r32_results)

        for current_round in knockout_rounds:
            matches = tournament_logic.knockout_generator(current_advancing_teams, current_round)
            results = simulate_matches(matches, team_stats, team_elos, global_team_avg,True)
            current_advancing_teams = tournament_logic.knockout_advancing_teams(results)
        
        # Extract the winning team from the final match dictionary
        champion = list(current_advancing_teams.values())[0]

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
    visualize.plot_probabilities(champions, SIMULATIONS)
    #print(results)
    #print(sorted_groups)
#    print(team_elos)


if __name__ == "__main__":
    main()