from models.deliveryPartner import Delivery


class DeliveryPartnerService:
    def assign_partner(self, order, partners):
        if not partners:
            raise ValueError("No delivery partners available")

        if order.store is None:
            raise ValueError("Cannot assign delivery partner without a store")

        selected_partner = min(partners, key=lambda partner: partner.total_deliveries())

        selected_partner.deliveries.append(
            Delivery(time=30, distance=order.delivery_distance)
        )
        order.delivery_partner = selected_partner

        return selected_partner
