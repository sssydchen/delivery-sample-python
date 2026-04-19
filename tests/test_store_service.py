import unittest

from models.customer import Customer
from models.item import Item
from models.loyalty_tier import LoyaltyTier
from models.order import Order, OrderLine
from services.store_service import StoreService


class TestStoreService(unittest.TestCase):
    def setUp(self):
        self.store_service = StoreService()
        self.customer = Customer(
            customer_id="C001",
            first_name="Jane",
            last_name="Doe",
            tier=LoyaltyTier.SILVER,
        )
        self.milk = Item(
            product_id="P001",
            name="Milk",
            description="Fresh milk",
            unit_price=10.0,
        )
        self.eggs = Item(
            product_id="P002",
            name="Eggs",
            description="Eggs",
            unit_price=12.0,
        )
        self.juice = Item(
            product_id="P003",
            name="Juice",
            description="Orange juice",
            unit_price=8.0,
        )

    def test_find_stores_for_item_returns_matching_stores(self):
        stores = self.store_service.find_stores_for_item("Milk")
        self.assertEqual(len(stores), 2)

    def test_find_stores_for_item_raises_error_when_not_found(self):
        with self.assertRaises(ValueError):
            self.store_service.find_stores_for_item("Monitor")

    def test_get_distance_returns_expected_distance(self):
        distance = self.store_service.get_distance("ZoneA", "ZoneB")
        self.assertEqual(distance, 3)

    def test_select_store_picks_nearest_store(self):
        order = Order(
            order_id="O001",
            customer=self.customer,
            store=None,
            lines=[OrderLine(item=self.milk, quantity=1)],
        )

        store = self.store_service.select_store(order, customer_zone="ZoneA")
        self.assertEqual(store.store_name, "StoreA")

    def test_assign_store_updates_order_store_and_distance(self):
        order = Order(
            order_id="O002",
            customer=self.customer,
            store=None,
            lines=[OrderLine(item=self.juice, quantity=1)],
        )

        self.store_service.assign_store(order, customer_zone="ZoneA")

        self.assertEqual(order.store.store_name, "StoreC")
        self.assertEqual(order.delivery_distance, 6)
