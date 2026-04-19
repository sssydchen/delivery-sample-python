from dataclasses import dataclass, field
from typing import Optional

from models.customer import Customer
from models.item import Item
from models.deliveryPartner import DeliveryPartner
from models.order_status import OrderStatus
from models.store import Store


@dataclass
class OrderLine:
    item: Item
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

    def line_total(self) -> float:
        return self.item.unit_price * self.quantity


@dataclass
class Order:
    order_id: str
    customer: Customer
    lines: list[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    store: Optional[Store] = None
    delivery_partner: Optional[DeliveryPartner] = None
    delivery_distance: float = 0.0
    delivery_fee: float = 0.0
    subtotal: float = 0.0
    total_price: float = 0.0

    def calculate_subtotal(self) -> float:
        self.subtotal = sum(line.line_total() for line in self.lines)
        return self.subtotal

    def calculate_total(self) -> float:
        self.total_price = self.calculate_subtotal() + self.delivery_fee
        return self.total_price

    def calculate_loyalty_points(self) -> int:
        base_points = int(self.total_price)
        return base_points * self.customer.tier.value

    def complete(self) -> None:
        if self.status != OrderStatus.CREATED:
            raise ValueError("Only created orders can be completed")
        if not self.lines:
            raise ValueError("Cannot complete an order with no items")
        if self.store is None:
            raise ValueError("Cannot complete an order without a store")
        if self.total_price <= 0:
            raise ValueError("Cannot complete an order without a calculated total")

        self.status = OrderStatus.COMPLETED
        self.customer.add_loyalty_points(self.calculate_loyalty_points())

    def cancel(self) -> None:
        if self.status != OrderStatus.CREATED:
            raise ValueError("Only created orders can be cancelled")

        self.status = OrderStatus.CANCELLED

    def reject(self) -> None:
        if self.status != OrderStatus.CREATED:
            raise ValueError("Only created orders can be rejected")

        self.status = OrderStatus.REJECTED
