from models.store import Store
from models.distanceMap import DistanceMap
from models.item import Item, Category 

DISTANCE_MAP = {
    DistanceMap("ZoneA", "ZoneA", 0),
    DistanceMap("ZoneA", "ZoneB", 3),
    DistanceMap("ZoneA", "ZoneC", 6),
    DistanceMap("ZoneB", "ZoneB", 0),
    DistanceMap("ZoneC", "ZoneC", 0)
}

STORES = [
    Store(1, "StoreA", "A", ["Milk","Eggs"]),
    Store(2, "StoreB", "B", ["Bread", "Milk"]),
    Store(3, "StoreC", "C", ["Juice", "Bread"]),
]

ITEMS = [
    Item(product_id="P008", name="KeyBoard", description="Mechanical Keyboard", unit_price=50),
    Item(product_id="P009", name="Mouse", description="Wireless Mouse",  unit_price=25),
    Item(product_id="P010", name="Monitor", description="27 inch 4K Monitor",  unit_price=75),
    Item(product_id="P011", name="Notebook",description="A4 Size Notebook",  unit_price=15)
]
