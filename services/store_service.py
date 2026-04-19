from staticData.staticData import DISTANCE_MAP, STORES


class StoreService:
    def normalize_zone(self, zone: str) -> str:
        if zone.startswith("Zone"):
            return zone

        return f"Zone{zone}"

    def find_stores_for_item(self, item_name: str):
        stores = [store for store in STORES if store.has_item(item_name)]
        if not stores:
            raise ValueError(f"No store found for item: {item_name}")
        return stores

    def get_distance(self, customer_zone: str, store_zone: str) -> int:
        normalized_customer_zone = self.normalize_zone(customer_zone)
        normalized_store_zone = self.normalize_zone(store_zone)

        for mapping in DISTANCE_MAP:
            zones = {mapping.zone_from, mapping.zone_to}
            if {normalized_customer_zone, normalized_store_zone} == zones:
                return mapping.distance

        raise ValueError(
            f"Distance not found for zones: {customer_zone} and {store_zone}"
        )

    def select_store(self, order, customer_zone: str):
        if not order.lines:
            raise ValueError("Cannot select a store for an empty order")

        candidate_stores = None

        for line in order.lines:
            item_stores = self.find_stores_for_item(line.item.name)
            if candidate_stores is None:
                candidate_stores = item_stores
            else:
                candidate_ids = {store.store_id for store in candidate_stores}
                candidate_stores = [
                    store for store in item_stores if store.store_id in candidate_ids
                ]

        if not candidate_stores:
            raise ValueError("No single store can fulfill the entire order")

        return min(
            candidate_stores,
            key=lambda store: self.get_distance(customer_zone, store.zone),
        )

    def assign_store(self, order, customer_zone: str):
        store = self.select_store(order, customer_zone)
        order.store = store
        order.delivery_distance = self.get_distance(customer_zone, store.zone)
        return order
