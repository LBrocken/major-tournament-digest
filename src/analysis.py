import pandas as pd

def get_placement_tiers(max_seed=10000):
    """
    Generates placement tiers. 
    """
    tiers = [1, 2, 3, 4]
    current = 5
    step = 2
    
    while current < max_seed:
        tiers.append(current)
        tiers.append(current + step)
        current = current + step + step
        step *= 2
    return tiers

def calculate_spr(seed, placement, tiers):
    projected_tier_index = 0
    for i, tier in enumerate(tiers):
        if tier <= seed:
            projected_tier_index = i
        else:
            break
            
    actual_tier_index = 0
import pandas as pd

def get_placement_tiers(max_seed=10000):
    """
    Generates placement tiers. 
    """
    tiers = [1, 2, 3, 4]
    current = 5
    step = 2
    
    while current < max_seed:
        tiers.append(current)
        tiers.append(current + step)
        current = current + step + step
        step *= 2
    return tiers

def calculate_spr(seed, placement, tiers):
    projected_tier_index = 0
    for i, tier in enumerate(tiers):
        if tier <= seed:
            projected_tier_index = i
        else:
            break
            
    actual_tier_index = 0
    for i, tier in enumerate(tiers):
        if placement >= tier:
            actual_tier_index = i
        else:
            break
            
    return projected_tier_index - actual_tier_index

def process_tournament_data(standings_nodes):
    tiers = get_placement_tiers()
    clean_data = []
    
    for node in standings_nodes:
        entrant = node.get('entrant', {})
        if not entrant: continue
        
        seed = entrant.get('initialSeedNum', 9999)
        placement = node.get('placement', 9999)
        name = entrant.get('name', 'Unknown')
        
        spr = calculate_spr(seed, placement, tiers)
        
        record = {
            'player_name': name,
            'seed': seed,
            'placement': placement,
            'spr': spr
        }
        clean_data.append(record)

    df = pd.DataFrame(clean_data)
    return df

def get_high_spr_runs(df, min_spr=3):
    """
    Returns ALL players with an SPR of min_spr or higher.
    Sorting Order:
    1. SPR (Descending) -> Biggest upset factor first
    2. Placement (Ascending) -> Better placing (1st) first
    3. Seed (Ascending) -> Higher seed/Better Rank (#1) first
    """
    # Filter for SPR >= 3
    high_spr = df[df['spr'] >= min_spr].copy()

    # Multi-column sort
    # SPR: Desc (False), Placement: Asc (True), Seed: Asc (True)
    return high_spr.sort_values(
        by=['spr', 'placement', 'seed'], 
        ascending=[False, True, True]
    )