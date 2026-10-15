
from civilisation_model import Civilisation
from trait import MilitaristicTrait, EngineeringTrait

student_id = "560856332"

militaristic = Civilisation(student_id, MilitaristicTrait())
militaristic.food = 1000

event = {
    "name": "Food Shortage",
    "effects": {
        "Food": {
            "amount": -100,
            "is_percentage": False
        }
    }
}

militaristic.apply_event(event)
print("Militaristic food:", militaristic.food)

engineering = Civilisation(student_id, EngineeringTrait())
engineering.food = 1000
engineering.apply_event(event)
print("Engineering food:", engineering.food)
