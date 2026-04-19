import unittest

from models.customer import Customer
from models.deliveryPartner import Delivery, DeliveryPartner
from models.item import Item
from models.loyalty_tier import LoyaltyTier
from models.order import Order, OrderLine
from models.store import Store
from services.delivery_partner_service import DeliveryPartnerService


class TestDeliveryPartnerService(unittest.TestCase):
    def setUp(self):
        self.service = DeliveryPartnerService()
        self.customer = Customer(
            customer_id="C001",
            first_name="Jane",
            last_name="Doe",
            tier=LoyaltyTier.SILVER,
        )
        self.store = Store(
            store_id=1,
            store_name="StoreA",
            zone="A",
            items=["Milk"],
        )
        self.item = Item(
            product_id="P001",
            name="Milk",
            description="Fresh milk",
            unit_price=10.0,
        )
        self.order = Order(
            order_id="O001",
            customer=self.customer,
            store=self.store,
            lines=[OrderLine(item=self.item, quantity=1)],
            delivery_distance=3,
            total_price=60.0,
        )

    def test_assign_partner_selects_least_busy_partner(self):
        partner_1 = DeliveryPartner(
            id=1,
            name="Alex",
            deliveries=[Delivery(time=30, distance=5.0)],
        )
        partner_2 = DeliveryPartner(
            id=2,
            name="Sam",
            deliveries=[],
        )

        assigned_partner = self.service.assign_partner(
            self.order, [partner_1, partner_2]
        )

        self.assertEqual(assigned_partner.name, "Sam")
        self.assertEqual(self.order.delivery_partner.name, "Sam")

    def test_assign_partner_adds_delivery_to_partner(self):
        partner = DeliveryPartner(
            id=1,
            name="Alex",
            deliveries=[],
        )

        self.service.assign_partner(self.order, [partner])

        self.assertEqual(partner.total_deliveries(), 1)
        self.assertEqual(partner.deliveries[0].distance, 3)

    def test_assign_partner_raises_error_when_no_partners_available(self):
        with self.assertRaises(ValueError):
            self.service.assign_partner(self.order, [])

    def test_assign_partner_requires_store_before_assignment(self):
        order = Order(
            order_id="O002",
            customer=self.customer,
            lines=[OrderLine(item=self.item, quantity=1)],
            total_price=60.0,
        )

        partner = DeliveryPartner(
            id=1,
            name="Alex",
            deliveries=[],
        )

        with self.assertRaises(ValueError):
            self.service.assign_partner(order, [partner])
