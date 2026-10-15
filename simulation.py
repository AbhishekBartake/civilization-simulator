
from dataloader import DataLoader
from civilisation_model import Civilisation
from strategy import Strategy
from trait import (
    AgriculturalTrait,
    CommercialTrait,
    MilitaristicTrait,
    ScientificTrait,
    EngineeringTrait
)
import random

class Simulation:
    
    @staticmethod
    def get_trait(student_id):
        trait_number = int(student_id[-2:]) % 5

        trait_classes = {
            0: AgriculturalTrait,
            1: CommercialTrait,
            2: MilitaristicTrait,
            3: ScientificTrait,
            4: EngineeringTrait
        }

        return trait_classes[trait_number]()

    def __init__(self, student_id):
        loader = DataLoader()
        self.student_id = student_id
        
        self.rules = loader.load_rules()
        self.events = loader.load_events()
        self.stages = loader.load_stages()

        self.trait = self.get_trait(student_id)
        self.civilisation = Civilisation(student_id, self.trait)
        self.strategy = Strategy(self.trait)
        self.history = []
    
    def process_event(self):
        event_number = random.randint(0, 99) / 100

        event = Civilisation.find_event(
            event_number,
            self.events
        )

        self.civilisation.apply_event(event)

        return event
    
    def choose_investment(self, event):
        resource = self.strategy.choose_investment(
            self.civilisation,
            self.rules,
            self.stages,
            event
        )

        return resource
    
    def apply_investment(self, resource):
        self.civilisation.apply_investment(
            resource,
            self.rules
        )
    

    def attempt_advancement(self, event):
        if not self.civilisation.can_advance_stage(
            self.stages
        ):
            return False

        civilisation = self.civilisation
        next_stage_number = civilisation.stage + 1

        next_stage = None

        for stage in self.stages:
            if stage["number"] == next_stage_number:
                next_stage = stage
                break

        chance = self.rules["base_advancement_chance"]

        consumption = int(
            civilisation.population
            * self.rules["food_per_person"]
        )

        comfortable_food = (
            self.rules["comfortable_food_turns"]
            * consumption
        )

        if civilisation.food >= comfortable_food:
            chance += self.rules["advancement_bonus"]

        comfortable_treasury = (
            self.rules["comfortable_treasury_per_stage"]
            * next_stage_number
        )

        if civilisation.treasury >= comfortable_treasury:
            chance += 10

        if civilisation.infrastructure > next_stage["min_infrastructure"]:
            chance += 10

        if civilisation.technology > next_stage["min_technology"]:
            chance += 10

        damaging_event = any(
            effect["amount"] < 0
            for effect in event["effects"].values()
        )

        if damaging_event:
            chance -= self.rules["damaging_event_penalty"]

        chance = min(
            chance,
            self.rules["max_advancement_chance"]
        )

        roll = random.randint(0, 99)

        if roll < chance:
            civilisation.stage += 1
            return True

        return False
    
    def process_turn(self):
        self.civilisation.decrease_cooldowns() 
        # Move to the next year
        self.civilisation.advance_year()

        # Step 1: Update resources
        self.civilisation.update_resources(self.rules)

        # Step 2: Select and apply an event
        event = self.process_event()

        # Step 3: Choose an investment
        resource = self.choose_investment(event)

        # Step 4: Apply the investment, if one was selected
        if resource is not None:
            self.apply_investment(resource)

        # Step 5: Attempt stage advancement
        advanced = self.attempt_advancement(event)
        
        # Step 6: Capture resources at the end of the turn
        resources = {
            "Population": self.civilisation.population,
            "Food": self.civilisation.food,
            "Treasury": self.civilisation.treasury,
            "Infrastructure": self.civilisation.infrastructure,
            "Technology": self.civilisation.technology,
        }

        # Return the results of this turn
        return {
            "year": self.civilisation.year,
            "event": event,
            "investment": resource,
            "advanced": advanced,
            "resources": resources,
        }
    
    def run(self):
        zero_food_turns = 0

        while self.civilisation.year < Civilisation.MAX_YEAR:
            result = self.process_turn()

            # Track consecutive turns ending with zero food
            if self.civilisation.food == 0:
                zero_food_turns += 1
            else:
                zero_food_turns = 0

            # Display the turn results
            print(f"\n{'=' * 40}")
            print("Year:", result["year"])
            print("Event:", result["event"]["name"])
            print("Investment:", result["investment"])
            print("Advanced:", result["advanced"])

            self.civilisation.display_resources()

            # Check whether the simulation should end
            reason = self.civilisation.check_end_condition(
                self.rules, zero_food_turns
            )

            if reason is not None:
                print("\nSimulation ended:", reason)
                break
    
    def record_history(self, event=None, investment=None,
                       advancement="Starting state"):
        civilisation = self.civilisation

        stage_name = "Unknown"
        for stage in self.stages:
            if stage["number"] == civilisation.stage:
                stage_name = stage["name"]
                break

        record = [
            f"Student ID: {self.student_id}",
            f"Trait: {self.trait.NAME}",
            f"YEAR {civilisation.year}",
            f"Stage: {stage_name}",
            f"Population: {civilisation.population:,}",
            f"Food: {civilisation.food:,}",
            f"Treasury: {civilisation.treasury:,}",
            f"Infrastructure: {civilisation.infrastructure:,}",
            f"Technology: {civilisation.technology:,}",
        ]

        if civilisation.year > 0:
            record.append(
                f"Event: {event['name'] if event else 'None'}"
            )
            record.append(
                f"Investment: {investment if investment else 'None'}"
            )
            record.append(f"Advancement: {advancement}")

        self.history.append("\n".join(record))


if __name__ == "__main__":
    test_ids = [
        "560856330",
        "560856331",
        "560856332",
        "560856333",
        "560856334"
    ]

    for student_id in test_ids:
        trait = Simulation.get_trait(student_id)
        print(student_id, "->", trait.NAME)
