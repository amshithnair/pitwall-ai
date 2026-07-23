from typing import List, Dict

class TrafficModel:
    """Determines traffic impact and rejoin positions."""
    
    @staticmethod
    def calculate_rejoin_position(driver_id: str, pit_loss_ms: int, driver_gaps_to_leader: Dict[str, int]) -> int:
        if driver_id not in driver_gaps_to_leader:
            return 1
            
        current_gap = driver_gaps_to_leader[driver_id]
        projected_gap = current_gap + pit_loss_ms
        
        # Count how many drivers have a smaller gap than the projected gap
        position = 1
        for d, gap in driver_gaps_to_leader.items():
            if d != driver_id and gap < projected_gap:
                position += 1
                
        return position
