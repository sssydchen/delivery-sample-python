from dataclasses import dataclass, field
from models.category import Category
from typing import Optional

    
@dataclass   
class Item:
    product_id: str 
    name: str 
    description: str
    unit_price: float
    category: Optional[Category] = field(default_factory=lambda: Category.DEFAULT)
    
    def get_category_name(self) -> str:
        return self.category.value if self.category else Category.DEFAULT
    


