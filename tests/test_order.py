import unittest

from models.customer import Customer
from models.item import Item
from models.loyalty_tier import LoyaltyTier
from models.order import Order, OrderLine
from models.order_status import OrderStatus
from models.store import Store


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.silver_customer = Customer(
            customer_id="C001",
            first_name="Jane",
            last_name="Doe",
            tier=LoyaltyTier.SILVER,
        )
        self.gold_customer = Customer(
            customer_id="C002",
            first_name="John",
            last_name="Smith",
            tier=LoyaltyTier.GOLD,
        )
        self.store = Store(
            store_id=1,
            store_name="StoreA",
            zone="A",
            items=["Milk", "Bread"],
        )
        self.item_1 = Item(
            product_id="P001",
            name="Milk",
            description="Fresh milk",
            unit_price=10.0,
        )

    def test_complete_order_adds_loyalty_points(self):
        order = Order(
            order_id="O001",
            customer=self.silver_customer,
            store=self.store,
            lines=[OrderLine(item=self.item_1, quantity=2)],
            total_price=20.0,
        )

        order.complete()

        self.assertEqual(order.status, OrderStatus.COMPLETED)
        self.assertEqual(self.silver_customer.loyaltyPoints, 60)

    def test_loyalty_points_depend_on_customer_tier(self):
        order = Order(
            order_id="O002",
            customer=self.gold_customer,
            store=self.store,
            lines=[OrderLine(item=self.item_1, quantity=2)],
            total_price=20.0,
        )

        order.complete()

        self.assertEqual(self.gold_customer.loyaltyPoints, 100)

    def test_complete_order_only_adds_points_once(self):
        order = Order(
            order_id="O003",
            customer=self.silver_customer,
            store=self.store,
            lines=[OrderLine(item=self.item_1, quantity=2)],
            total_price=20.0,
        )

        order.complete()

        with self.assertRaises(ValueError):
            order.complete()

        self.assertEqual(self.silver_customer.loyaltyPoints, 60)

    def test_cancelled_order_does_not_add_loyalty_points(self):
        order = Order(
            order_id="O004",
            customer=self.silver_customer,
            lines=[OrderLine(item=self.item_1, quantity=1)],
        )

        order.cancel()

        self.assertEqual(self.silver_customer.loyaltyPoints, 0)
