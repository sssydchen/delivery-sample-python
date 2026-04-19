from dataclasses import dataclass
from models.loyalty_tier import LoyaltyTier
    
@dataclass
class Customer:
    customer_id: str
    first_name: str
    last_name: str
    tier: LoyaltyTier
    loyaltyPoints: int = 0 

    def add_loyalty_points(self, points: int) -> None:
        if points < 0:
            raise ValueError("Loyalty points cannot be negative")

        self.loyaltyPoints += points

    