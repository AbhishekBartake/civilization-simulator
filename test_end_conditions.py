
from civilisation_model import Civilisation
from simulation import Simulation
from trait import (
    AgriculturalTrait,
    CommercialTrait,
    ScientificTrait,
    MilitaristicTrait,
    EngineeringTrait
)

# Create a civilisation using your existing setup
student_id = "560856334"
simulation = Simulation(student_id)
civilisation = simulation.civilisation

# Test 1: Population below minimum
civilisation.population = 249
print(
    "Population 249:",
    civilisation.check_end_condition(simulation.rules, 0)
)

# Test 2: Population exactly at minimum
civilisation.population = 250
print(
    "Population 250:",
    civilisation.check_end_condition(simulation.rules, 0)
)

# Test 3: Food reaches zero for two consecutive turns
civilisation.population = 1000
civilisation.food = 0
civilisation.stage = 1
civilisation.year = 100

print(
    "Food zero for 1 turn:",
    civilisation.check_end_condition(simulation.rules, 1)
)

print(
    "Food zero for 2 turns:",
    civilisation.check_end_condition(simulation.rules, 2)
)


# Test 4: Space Colony reached
civilisation.population = 150000
civilisation.food = 100000
civilisation.stage = 10
civilisation.year = 1000

print(
    "Space Colony:",
    civilisation.check_end_condition(simulation.rules, 0)
)

# Test 5: Year 3000 reached
civilisation.stage = 9
civilisation.year = 3000
civilisation.population = 1000
civilisation.food = 1000

print(
    "Year 3000:",
    civilisation.check_end_condition(simulation.rules, 0)
)


# Test 6: Verify all five trait assignments
for remainder in range(5):
    student_id = "1234567" + str(10+remainder)
    trait = Simulation.get_trait(student_id)
    print(remainder, trait.NAME)


# Test 7: Verify trait rule adjustments
rules = simulation.rules

for trait_class in (
    AgriculturalTrait,
    CommercialTrait,
    MilitaristicTrait,
    ScientificTrait,
    EngineeringTrait,
):
    trait = trait_class()
    adjusted = trait.adjust_rules(rules)

    print(
        trait.NAME,
        "growth_rate =", adjusted["growth_rate"],
        "tax_per_person =", adjusted["tax_per_person"],
        "upkeep_per_infrastructure =",
        adjusted["upkeep_per_infrastructure"],
    )

# Test Engineering's infrastructure priority bonus
engineering = EngineeringTrait()
print(
    "Engineering infrastructure bonus:",
    engineering.priority_bonus("Infrastructure"),
)
