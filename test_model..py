
from civilisation_model import Civilisation
from trait import EngineeringTrait

trait = EngineeringTrait()
civilisation = Civilisation("500123456", trait)

print("Initial resources:")
civilisation.display_resources()

print("\nTesting event lookup:")
event = Civilisation.find_event(0.10, [
    {
        "name": "Drought",
        "lower": 0.00,
        "upper": 0.14,
        "effects": {
            "Food": {
                "amount": -30,
                "is_percentage": True
            }
        }
    }
])
print("Event found:", event["name"])

print("\nTesting event application:")
old_food = civilisation.food
civilisation.apply_event(event)
expected_food = max(0, old_food + int(old_food * -30 / 100))
print("Food before:", old_food)
print("Food after:", civilisation.food)
print("Expected food:", expected_food)
assert civilisation.food == expected_food

print("\nTesting investment:")
rules = {
    "infrastructure_investment_cost": 1200,
    "infrastructure_investment_gain": 2,
    "cooldown_turns": 2
}

civilisation.treasury = 10000
old_infrastructure = civilisation.infrastructure
old_treasury = civilisation.treasury
cost = old_infrastructure * 1200

civilisation.apply_investment("Infrastructure", rules)

assert civilisation.infrastructure == old_infrastructure + 3
assert civilisation.treasury == old_treasury - cost
assert civilisation.investment_cooldowns["Infrastructure"] == 2

print("Infrastructure investment passed!")
print("Treasury:", civilisation.treasury)
print("Infrastructure:", civilisation.infrastructure)
print("Cooldowns:", civilisation.investment_cooldowns)

print("\nAll model checks passed!")


print("\nTesting resource update:")

rules = {
    "food_base_production": 0.75,
    "food_production_per_technology": 0.05,
    "food_per_person": 1.0,
    "food_storage_turns": 5,
    "capacity_per_infrastructure": 3000,
    "famine_loss": 0.20,
    "overcrowding_loss": 0.10,
    "growth_rate": 0.08,
    "tax_per_person": 0.15,
    "upkeep_per_infrastructure": 40
}

civilisation = Civilisation("123456789", trait)

civilisation.update_resources(rules)

print("Population:", civilisation.population)
print("Food:", civilisation.food)
print("Treasury:", civilisation.treasury)

assert civilisation.population == 1125
assert civilisation.food == 3158
assert civilisation.treasury == 2706

print("Resource update checks passed!")
print("Resource update checks passed!")
