
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

        data = loader.load_all()

        if data is None:
            raise RuntimeError("Simulation could not load the required data files.")

        self.rules, self.events, self.stages = data


        self.trait = self.get_trait(student_id)
        self.civilisation = Civilisation(student_id, self.trait)
        self.strategy = Strategy(self.trait)
        self.history = []
    
    def record_history(self, result=None):
        civilisation = self.civilisation

        if result is None:
            resources = {
                "Population": civilisation.population,
                "Food": civilisation.food,
                "Treasury": civilisation.treasury,
                "Infrastructure": civilisation.infrastructure,
                "Technology": civilisation.technology,
            }
            year = civilisation.year
        else:
            resources = result["resources"]
            year = result["year"]

        stage_name = "Unknown"

        for stage in self.stages:
            if stage["number"] == civilisation.stage:
                stage_name = stage["name"]
                break

        self.history.append({
            "year": year,
            "stage": civilisation.stage,
            "stage_name": stage_name,
            "resources": resources.copy(),
            "event": result["event"] if result else None,
            "investment": result["investment"] if result else None,
            "advancement": result["advanced"] if result else {
                "status": "Starting state",
                "chance": None,
                "stage": None,
            },
        })


    def write_history(self, end_reason):
        try:
            with open("civilisation_history.txt", "w") as history_file:
                history_file.write(f"Student ID: {self.student_id}\n")
                history_file.write(f"Trait: {self.trait.NAME}\n\n")

                for entry in self.history:
                    history_file.write(f"YEAR {entry['year']}\n")
                    history_file.write(f"Stage: {entry['stage_name']}\n")

                    for resource, value in entry["resources"].items():
                        history_file.write(f"{resource}: {value:,}\n")

                    if entry["year"] == 0:
                        history_file.write("Advancement: Starting state\n\n")
                        continue

                    history_file.write(
                        f"Event: {entry['event']['name']}\n"
                    )
                    history_file.write(
                        f"Investment: {entry['investment']}\n"
                    )

                    advancement = entry["advancement"]

                    if advancement["status"] == "Requirements not met":
                        message = "Requirements not met"
                    elif advancement["status"] == "Failed":
                        message = f"Failed (chance {advancement['chance']}%)"
                    else:
                        message = (
                            f"ADVANCED to {advancement['stage']} "
                            f"(chance {advancement['chance']}%)"
                        )

                    history_file.write(f"Advancement: {message}\n\n")

                history_file.write(
                    f"SIMULATION ENDED IN YEAR "
                    f"{self.civilisation.year}: {end_reason.upper()}\n" 
                )


        except OSError as error:
            print(f"Error writing history file: {error}")
            return False

        return True

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
        if not self.civilisation.can_advance_stage(self.stages):
            return {
                "status": "Requirements not met",
                "chance": None,
                "stage": None,
            }

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
            self.rules["comfortable_food_turns"] * consumption
        )

        if civilisation.food >= comfortable_food:
            chance += self.rules["advancement_bonus"]

        comfortable_treasury = (
            self.rules["comfortable_treasury_per_stage"]
            * next_stage_number
        )


        if civilisation.treasury >= comfortable_treasury:
            chance += self.rules["advancement_bonus"]


        if civilisation.infrastructure > next_stage["min_infrastructure"]:
            chance += self.rules["advancement_bonus"]


        if civilisation.technology > next_stage["min_technology"]:
            chance += self.rules["advancement_bonus"]

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
            return {
                "status": "ADVANCED",
                "chance": chance,
                "stage": next_stage["name"],
            }

        return {
            "status": "Failed",
            "chance": chance,
            "stage": None,
        }

    
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
        end_reason = "Year 3000 reached"

        # Record the starting state at Year 0
        self.record_history()
        print("\nStarting civilisation:")
        self.civilisation.display_resources()

        while self.civilisation.year < Civilisation.MAX_YEAR:
            result = self.process_turn()
            self.record_history(result)

            # Track consecutive turns ending with zero food
            if self.civilisation.food == 0:
                zero_food_turns += 1
            else:
                zero_food_turns = 0

            # Check whether the simulation should end
            reason = self.civilisation.check_end_condition(
                self.rules, zero_food_turns
            )

            # Display results every 100 years, on advancement,
            # or on the final turn
            if (
                result["year"] % 100 == 0
                or result["advanced"]["status"] == "ADVANCED"
                or reason is not None
            ):
                print("\n" + "-" * 65)
                print(
                    f"📅 YEAR {result['year']}  |  STAGE {self.civilisation.stage}")
                print("-" * 65)

                print("\n⚡ EVENT")
                print(f"   {result['event']['name']}")

                print("\n📈 INVESTMENT")
                investment = result["investment"]
                if investment is None:
                    print("   No investment made")
                else:
                    print(f"   Invested in {investment}")

                print("\n🏛️ ADVANCEMENT")
                advancement = result["advanced"]

                if advancement["status"] == "ADVANCED":
                    print(
                        f"   ✨ Advanced to {advancement['stage']} "
                        f"(chance {advancement['chance']}%)"
                    )
                elif advancement["status"] == "Failed":
                    print(
                        f"   Not advanced "
                        f"(chance {advancement['chance']}%)"
                    )
                else:
                    print("   Requirements not met")

                self.civilisation.display_resources()

            # End the simulation if a stopping condition is met
            if reason is not None:
                end_reason = reason
                print("\n\n" + "=" * 65)
                print("                 🏆 SIMULATION COMPLETE")
                print(f"                 {reason}")
                print("=" * 65)
                break

        # Write the complete simulation history
        if self.write_history(end_reason):
            print("History saved to civilisation_history.txt")
