
from strategy import Strategy


class MockTrait:
    def priority_bonus(self, resource):
        return 0


class MockCivilisation:
    RESOURCE_NAMES = [
        "Population",
        "Food",
        "Treasury",
        "Infrastructure",
        "Technology"
    ]

    def __init__(self):
        self.population = 100
        self.food = 0
        self.treasury = 10000
        self.infrastructure = 1
        self.technology = 1
        self.stage = 1
        self.investment_cooldowns = {}


def test_emergency_food_override():
    strategy = Strategy(MockTrait())
    civilisation = MockCivilisation()

    rules = {
        "food_base_production": 0.75,
        "food_production_per_technology": 0.05,
        "food_per_person": 1.0,
        "population_investment_cost": 0.20,
        "food_investment_cost": 0.10,
        "treasury_investment_cost": 0,
        "infrastructure_investment_cost": 1200,
        "technology_investment_cost": 1200
    }

    stages = [
        {
            "number": 1,
            "min_population": 0,
            "min_infrastructure": 0,
            "min_technology": 0
        },
        {
            "number": 2,
            "min_population": 1500,
            "min_infrastructure": 4,
            "min_technology": 2
        }
    ]

    event = {"name": "No Major Event", "effects": {}}

    # Food is critically low, so Food should be selected.
    result = strategy.choose_investment(
        civilisation, rules, stages, event
    )
    assert result == "Food", f"Expected Food, got {result}"
    print("PASS: Emergency override selects Food")

    # Food is unaffordable only if its cost exceeds Treasury.
    # Make Food unavailable through cooldown instead.
    civilisation.investment_cooldowns["Food"] = 2

    result = strategy.choose_investment(
        civilisation, rules, stages, event
    )
    assert result == "Infrastructure", (
        f"Expected Infrastructure fallback, got {result}"
    )
    print("PASS: Falls back to Infrastructure when Food is on cooldown")

    # If both Food and Infrastructure are unavailable, normal scoring
    # should choose another eligible resource.
    civilisation.investment_cooldowns["Infrastructure"] = 2

    result = strategy.choose_investment(
        civilisation, rules, stages, event
    )
    assert result not in ("Food", "Infrastructure"), (
        f"Expected another eligible resource, got {result}"
    )
    print("PASS: Uses normal scoring when both emergency options are unavailable")


def test_tie_breaking():
    strategy = Strategy(MockTrait())
    civilisation = MockCivilisation()

    # Ensure the emergency Food override does not activate.
    civilisation.food = 10000

    rules = {
        "food_base_production": 0.75,
        "food_production_per_technology": 0.05,
        "food_per_person": 1.0,
        "population_investment_cost": 0.20,
        "food_investment_cost": 0.10,
        "treasury_investment_cost": 0,
        "infrastructure_investment_cost": 1200,
        "technology_investment_cost": 1200
    }

    stages = [
        {
            "number": 1,
            "min_population": 0,
            "min_infrastructure": 0,
            "min_technology": 0
        }
    ]

    event = {"name": "No Major Event", "effects": {}}

    # Make every resource eligible.
    strategy.can_invest = lambda resource, civilisation, rules: True

    # Give Population and Food equal highest scores.
    def mock_score(resource, civilisation, rules, stages, event):
        if resource in ("Population", "Food"):
            return 50
        return 10

    strategy.get_priority_score = mock_score

    result = strategy.choose_investment(
        civilisation, rules, stages, event
    )

    assert result == "Population", (
        f"Expected Population to win the tie, got {result}"
    )

    print("PASS: Tie-breaking selects Population before Food")


if __name__ == "__main__":
    test_emergency_food_override()
    test_tie_breaking()

# if __name__ == "__main__":
#     test_emergency_food_override()
