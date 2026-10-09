
import random

from dataloader import DataLoader
from civilisation_model import Civilisation

student_id = "560856334"

loader = DataLoader()
data = loader.load_all()

if data is not None:
    rules, events, stages = data

    civilisation = Civilisation(student_id)

    random.seed(int(student_id))

    random_number = random.randint(0, 99)
    event_number = random_number / 100

    event = Civilisation.find_event(event_number, events)

    print("Random integer:", random_number)
    print("Event number:", event_number)
    print("Selected event:", event["name"])

    civilisation.update_resources(rules)

    civilisation.apply_event(event)

    print("\nAFTER RESOURCE UPDATE AND EVENT")
    civilisation.year = 10
    civilisation.display_resources()
