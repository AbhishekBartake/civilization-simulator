
from strategy import Strategy
from trait import EngineeringTrait
from civilisation_model import Civilisation
from dataloader import DataLoader

strategy = Strategy(EngineeringTrait())
civ = Civilisation("123456734", EngineeringTrait())
stages = DataLoader().load_stages()

rules = {
    "food_per_person": 1.0,
    "capacity_per_infrastructure": 3000,
    "infrastructure_investment_cost": 1200,
    "technology_investment_cost": 1200
}

civ.stage = 1
civ.population = 1400
civ.food = 100
civ.treasury = 100
civ.infrastructure = 3
civ.technology = 1

event = {
    "name": "Flood",
    "effects": {
        "Food": {"amount": -20, "is_percentage": True},
        "Infrastructure": {"amount": -1, "is_percentage": False}
    }
}

print(
    "Food score:",
    strategy.get_priority_score("Food", civ, rules, stages, event)
)
print(
    "Infrastructure score:",
    strategy.get_priority_score(
        "Infrastructure", civ, rules, stages, event
    )
)
