class Civilisation:
    MAX_YEAR = 3000
    RESOURCE_NAMES=[
        "Population",
        "Food",
        "Treasury",
        "Infrastructure",
        "Technology"
    ]
    def __init__(self,student_id):
        self.student_id=student_id
        self.year=0
        self.stage=1
        
        digits = [int(digit) for digit in student_id]
        
        ABC=int(student_id[0:3])
        DEF=int(student_id[3:6])
        GHI = int(student_id[6:9])
        
        self.population = 800 + ABC *2
        self.food = 2000+DEF*3
        self.treasury=1000+GHI*2
        
        self.infrastructure = 1+(
            digits[0]+digits[3]+digits[6]
        )%4
        
        self.technology = 1+(
            digits[2]+digits[5]+digits[8]
        )%3
        
    @staticmethod
    def is_valid_student_id(student_id):
        return(
            len(student_id)==9
            and student_id.isdigit()
        )

    def display_resources(self):
        print(f"Student ID: {self.student_id}")
        print(f"Year: {self.year}")
        print(f"Stage: {self.stage}")
        print(f"Population: {self.population:,}")
        print(f"Food: {self.food:,}")
        print(f"Treasury: {self.treasury:,}")
        print(f"Infrastructure: {self.infrastructure:,}")
        print(f"Technology: {self.technology:,}")
    
    def update_resources(self, rules):
        production = int(
            self.population
            * (
                rules["food_base_production"]
                + rules["food_production_per_technology"]
                * self.technology
            )
        )

        consumption = int(
            self.population * rules["food_per_person"]
        )

        self.food += production - consumption

        storage_limit = int(
            self.population * rules["food_storage_turns"]
        )

        if self.food > storage_limit:
            self.food = storage_limit

        capacity = (
            self.infrastructure
            * rules["capacity_per_infrastructure"]
        )

        if self.food < 0:
            self.food = 0
            self.population = int(
                self.population * (1 - rules["famine_loss"])
            )

        elif self.population > capacity:
            self.population = max(
                capacity,
                int(
                    self.population
                    * (1 - rules["overcrowding_loss"])
                )
            )

        else:
            self.population = min(
                capacity,
                int(
                    self.population * (1 + rules["growth_rate"])
                )
            )

        income = int(
            self.population * rules["tax_per_person"]
        )

        upkeep = (
            self.infrastructure
            * rules["upkeep_per_infrastructure"]
        )

        self.treasury = max(
            0,
            self.treasury + income - upkeep
        )

        self.population = max(0, self.population)
        self.food = max(0, self.food)
        self.treasury = max(0, self.treasury)
        self.infrastructure = max(1, self.infrastructure)
        self.technology = max(1, self.technology)
    
    def apply_event(self, event):
        for resource, effect in event["effects"].items():
            amount = effect["amount"]

            if effect["is_percentage"]:
                current_value = getattr(
                    self, resource.lower()
                )

                change = int(current_value * amount / 100)
            else:
                change = amount

            attribute = resource.lower()
            current_value = getattr(self, attribute)
            new_value = current_value + change

            if attribute in ("infrastructure", "technology"):
                new_value = max(1, new_value)
            else:
                new_value = max(0, new_value)

            setattr(self, attribute, new_value)

    @staticmethod
    def find_event(event_number, events):
        for event in events:
            if (
                event["lower"]
                <= event_number
                <= event["upper"]
            ):
                return event

        return {
            "name": "No Major Event",
            "lower": 0.95,
            "upper": 0.99,
            "effects": {}
        }
