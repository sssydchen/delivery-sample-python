from services.pricing_service import PricingService


class SampleProblem:
    def __init__(self):
        self.pricing_service = PricingService()

    def calculate_cost(self, distance):
        return self.pricing_service.calculate_delivery_fee(distance)


def main():
    sample = SampleProblem()
    result = sample.calculate_cost(8)
    print(result)


if __name__ == "__main__":
    main()
