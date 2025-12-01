import requests
import os
import sys
import time

def get_headers():
    api_token = os.getenv('STARTGG_KEY')
    if not api_token:
        print("Error: STARTGG_KEY not found in environment variables.")
        sys.exit(1)
    return {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

def fetch_tournament_events(slug):
    """
    Step 1: Get the list of all events for a tournament slug.
    """
    url = 'https://api.start.gg/gql/alpha'
    
    query = """
    query GetEvents($slug: String!) {
      tournament(slug: $slug) {
        name
        events {
          id
          name
          videogame {
            name
          }
        }
      }
    }
    """
    
    response = requests.post(
        url, 
        json={'query': query, 'variables': {'slug': slug}}, 
        headers=get_headers()
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print(f"API Error: {data['errors'][0]['message']}")
            return None
        return data.get('data', {}).get('tournament')
    else:
        print(f"Network Error: {response.status_code}")
        return None

def fetch_event_standings(event_id):
    """
    Step 2: Get all players from a specific Event ID (Pagination).
    """
    url = 'https://api.start.gg/gql/alpha'
    
    # Query specific to an Event ID
    query = """
    query GetEventStandings($eventId: ID!, $page: Int!) {
      event(id: $eventId) {
        name
        standings(query: {perPage: 100, page: $page}) {
          pageInfo {
            totalPages
          }
          nodes {
            placement
            entrant {
              name
              initialSeedNum
            }
          }
        }
      }
    }
    """

    all_nodes = []
    page = 1
    more_pages = True
    event_name = "Unknown Event"

    print(f"Fetching data for Event ID {event_id}...", end=" ", flush=True)

    while more_pages:
        response = requests.post(
            url, 
            json={'query': query, 'variables': {'eventId': event_id, 'page': page}}, 
            headers=get_headers()
        )

        if response.status_code == 200:
            data = response.json()
            # Handle potential API errors gracefully
            if 'errors' in data:
                print(f"Error on page {page}: {data['errors'][0]['message']}")
                break
                
            event_data = data.get('data', {}).get('event')
            if not event_data:
                break
            
            event_name = event_data['name']
            standings = event_data.get('standings', {})
            nodes = standings.get('nodes', [])
            
            if not nodes:
                more_pages = False
            else:
                all_nodes.extend(nodes)
                print(f"{page}..", end=" ", flush=True)
                
                page_info = standings.get('pageInfo', {})
                if page >= page_info.get('totalPages', 1):
                    more_pages = False
                else:
                    page += 1
                    time.sleep(0.4) # Rate limit safety
        else:
            print(f"Network Error: {response.status_code}")
            break
            
    return all_nodes, event_name