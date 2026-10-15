
from dataloader import DataLoader
from civilisation_model import Civilisation
from trait import EngineeringTrait

loader = DataLoader()
rules = loader.load_rules()

civilisation = Civilisation("560856334", EngineeringTrait())

resource = "Infrastructure"

# Simulate investing in Infrastructure
civilisation.start_cooldown(resource, rules)

print("After investment:", civilisation.investment_cooldowns)

# Simulate the next three turns
for turn in range(1, 4):
    civilisation.decrease_cooldowns()

    print(
        f"After turn {turn}:",
        civilisation.investment_cooldowns
    )