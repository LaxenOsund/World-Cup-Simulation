import matplotlib.pyplot as plt

def plot_probabilities(champions, simulations):
    print("\nCreating graph")
    
    # Pick top 15 winners
    sorted_champions = sorted(champions.items(), key=lambda x: x[1], reverse=True)[:15]
    
    # Get teamnames and win chances
    teams = [item[0] for item in sorted_champions]
    probabilities = [(item[1] / simulations) * 100 for item in sorted_champions]

    plt.figure(figsize=(10, 6))
    
    # Create bars
    bars = plt.barh(teams, probabilities, color='#1f77b4', edgecolor='black')
    
    plt.xlabel('Winchance (%)', fontsize=12)

    
    # Inverts y axis so most common winner gets placed highest
    plt.gca().invert_yaxis() 

    # Loops through every bar and prints win % on side
    for bar in bars:
        bredd = bar.get_width()
        plt.text(bredd + 0.5, bar.get_y() + bar.get_height()/2, 
                 f'{bredd:.1f}%', 
                 va='center', ha='left', fontsize=10, fontweight='bold')

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tight_layout()
    
    # Saves image
    plt.savefig('vm_result.png', dpi=300)

    plt.show()