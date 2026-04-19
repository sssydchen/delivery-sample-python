from models.order import Order

class PricingService:
    BASE_COST = 50.0
    BASE_DISTANCE = 5
    EXTRA_COST_PER_UNIT = 10.0

    def calculate_delivery_fee(self, distance: float) -> float:
        if distance <= 0:
            raise ValueError("Distance must be greater than 0")

        if distance <= self.BASE_DISTANCE:
            return self.BASE_COST

        extra_distance = distance - self.BASE_DISTANCE
        return self.BASE_COST + (extra_distance * self.EXTRA_COST_PER_UNIT)

    def price_order(self, order: Order, distance: float) -> float:
        order.delivery_fee = self.calculate_delivery_fee(distance)
        order.calculate_subtotal()
        order.total_price = order.subtotal + order.delivery_fee
        return order.total_price
