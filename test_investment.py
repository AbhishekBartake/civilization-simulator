
from civilisation_model import Civilisation
from trait import EngineeringTrait

rules = {
    "population_investment_cost": 0.20,
    "population_investment_gain": 0.10,
    "food_investment_cost": 0.10,
    "food_investment_gain": 0.80,
    "treasury_investment_cost": 0,
    "treasury_investment_gain": 0.40,
    "infrastructure_investment_cost": 1200,
    "infrastructure_investment_gain": 2,
    "technology_investment_cost": 1200,
    "technology_investment_gain": 1,
}

trait = EngineeringTrait()
civilisation = Civilisation("123456789", trait)

# Test 1: Infrastructure investment
civilisation.population = 1000
civilisation.treasury = 10000
civilisation.infrastructure = 2

civilisation.apply_investment("Infrastructure", rules)

assert civilisation.infrastructure == 5
assert civilisation.treasury == 7600

print("PASS: Infrastructure investment")

# Test 2: Population investment
civilisation.population = 1000
civilisation.treasury = 10000

civilisation.apply_investment("Population", rules)

assert civilisation.population == 1100
assert civilisation.treasury == 9800

print("PASS: Population investment")

# Test 3: Food investment
civilisation.population = 1000
civilisation.food = 500
civilisation.treasury = 10000

civilisation.apply_investment("Food", rules)

assert civilisation.food == 1300
assert civilisation.treasury == 9900

print("PASS: Food investment")

# Test 4: Treasury investment
civilisation.population = 1000
civilisation.treasury = 10000

civilisation.apply_investment("Treasury", rules)

assert civilisation.treasury == 10400

print("PASS: Treasury investment")

# Test 5: Technology investment
civilisation.technology = 1
civilisation.treasury = 10000

civilisation.apply_investment("Technology", rules)

assert civilisation.technology == 2
assert civilisation.treasury == 8800

print("PASS: Technology investment")

print("All investment tests passed!")