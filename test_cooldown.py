
from civilisation_model import Civilisation
from trait import EngineeringTrait

rules = {"cooldown_turns": 2}

civilisation = Civilisation("123456789", EngineeringTrait())

# Start a cooldown after investing in Infrastructure
civilisation.start_cooldown("Infrastructure", rules)

assert civilisation.investment_cooldowns["Infrastructure"] == 2

# First turn passes
civilisation.decrease_cooldowns()
assert civilisation.investment_cooldowns["Infrastructure"] == 1

# Second turn passes
civilisation.decrease_cooldowns()
assert "Infrastructure" not in civilisation.investment_cooldowns

print("All cooldown method tests passed!")
