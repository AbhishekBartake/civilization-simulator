
from simulation import Simulation

simulation = Simulation("560856334")
civilisation = simulation.civilisation

civilisation.infrastructure = 1
civilisation.treasury = 10000

civilisation.apply_investment("Infrastructure", simulation.rules)

print("Infrastructure:", civilisation.infrastructure)
