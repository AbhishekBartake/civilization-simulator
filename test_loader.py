
from dataloader import DataLoader

loader = DataLoader()
data = loader.load_all()

if data is not None:
    rules, events, stages = data

    print("Rules loaded:", len(rules))
    print("Events loaded:", len(events))
    print("Stages loaded:", len(stages))

    print("\nGrowth rate:", rules["growth_rate"])
    print("First event:", events[0]["name"])
    print("Second stage:", stages[1]["name"])
