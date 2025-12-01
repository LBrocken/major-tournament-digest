import os
import sys
from dotenv import load_dotenv
import api_client
import analysis

def main():
    load_dotenv()
    
    # 1. Ask for Tournament Slug
    print("\n--- Major Tournament Digest ---")
    default_slug = os.getenv('TOURNAMENT_SLUG', 'genesis-x')
    slug_input = input(f"Enter Tournament Slug (default: '{default_slug}'): ").strip()
    
    if not slug_input:
        slug_input = default_slug

    # 2. Fetch Available Events
    print(f"Looking up tournament: {slug_input}...")
    tournament = api_client.fetch_tournament_events(slug_input)
    
    if not tournament:
        print("Tournament not found. Check spelling.")
        return

    print(f"\nFound Tournament: {tournament['name']}")
    events = tournament.get('events', [])
    
    if not events:
        print("No events found for this tournament.")
        return

    # 3. Interactive Event Selection
    print("\nAvailable Events:")
    for i, event in enumerate(events):
        game_name = event.get('videogame', {}).get('name', 'Unknown Game')
        print(f"[{i+1}] {event['name']} ({game_name})")

    try:
        selection = input("\nEnter the number of the event to analyze: ")
        index = int(selection) - 1
        if index < 0 or index >= len(events):
            print("Invalid selection.")
            return
        selected_event = events[index]
    except ValueError:
        print("Please enter a valid number.")
        return

    # 4. Fetch Data for selected event
    event_id = selected_event['id']
    standings_nodes, event_name = api_client.fetch_event_standings(event_id)
    
    if not standings_nodes:
        print("\nNo standings data found.")
        return

    print(f"\n\nAnalyzed {len(standings_nodes)} entrants for {event_name}")

    # 5. Run Analysis
    df = analysis.process_tournament_data(standings_nodes)
    
    # Analyze (SPR >= 3)
    high_performers = analysis.get_high_spr_runs(df, min_spr=3)
    
    print(f"\n--- 🚨 DEEP RUN REPORT (SPR +3 or higher) 🚨 ---")
    
    if high_performers.empty:
        print("No +3 SPR runs found.")
    else:
        for index, row in high_performers.iterrows():
            print(f"• {row['player_name']} (Seed {row['seed']})") 
            print(f"  Placed {row['placement']} | SPR: +{row['spr']}")
            print("  --------------------------------")
    
    print("Report Generation Complete.")

if __name__ == "__main__":
    main()