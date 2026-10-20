class Civilisation:
    MAX_YEAR = 3000

    RESOURCE_NAMES = [
        "Population",
        "Food",
        "Treasury",
        "Infrastructure",
        "Technology"
    ]

    def __init__(self, student_id, trait):
        self.student_id = student_id
        self.trait = trait
        self.year = 0
        self.stage = 1
        self.investment_cooldowns = {}

        digits = [int(digit) for digit in student_id]

        ABC = int(student_id[0:3])
        DEF = int(student_id[3:6])
        GHI = int(student_id[6:9])

        self.population = 800 + ABC * 2
        self.food = 2000 + DEF * 3
        self.treasury = 1000 + GHI * 2

        self.infrastructure = 1 + (
            digits[0] + digits[3] + digits[6]
        ) % 4

        self.technology = 1 + (
            digits[2] + digits[5] + digits[8]
        ) % 3

    @staticmethod
    def is_valid_student_id(student_id):
        return (
            len(student_id) == 9
            and student_id.isdigit()
        )

    def make_progress_bar(self, value, maximum, width=20):
        percentage = max(0, min(value / maximum, 1))
        filled = int(percentage * width)

        bar = "█" * filled + "░" * (width - filled)

        return f"[{bar}] {percentage:.0%}"

    def display_resources(self):
        print("\n" + "=" * 65)
        print("                 🏛️  CIVILISATION SUMMARY")
        print(f"                 📅 YEAR {self.year}  |  STAGE {self.stage}")
        print("=" * 65)

        resources = [
            ("Population", self.population, 200_000),
            ("Food", self.food, 1_500_000),
            ("Treasury", self.treasury, 150_000),
            ("Infrastructure", self.infrastructure, 100),
            ("Technology", self.technology, 50)
        ]

        icons = ["👥", "🌾", "💰", "🏗️", "🔬"]

        print("RESOURCE OVERVIEW")
        print("-" * 65)

        for (name, value, maximum), icon in zip(resources, icons):
            bar = self.make_progress_bar(value, maximum)
            label = f"{icon} {name}"
            separator = "    " if name == "Infrastructure" else "  "
            print(f"{label:<23} {value:>10,}{separator}{bar}")

    def update_resources(self, rules):
        adjusted_rules = self.trait.adjust_rules(rules)

        production = int(
            self.population
            * (
                adjusted_rules["food_base_production"]
                + adjusted_rules["food_production_per_technology"]
                * self.technology
            )
        )

        consumption = int(
            self.population * adjusted_rules["food_per_person"]
        )

        self.food += production - consumption


        storage_limit = int(
            self.population
            * adjusted_rules["food_per_person"]
            * adjusted_rules["food_storage_turns"]
        )

        if self.food > storage_limit:
            self.food = storage_limit

        capacity = (
            self.infrastructure
            * adjusted_rules["capacity_per_infrastructure"]
        )

        if self.food < 0:
            self.food = 0
            self.population = int(
                self.population * (1 - adjusted_rules["famine_loss"])
            )

        elif self.population > capacity:
            self.population = max(
                capacity,
                int(
                    self.population
                    * (1 - adjusted_rules["overcrowding_loss"])
                )
            )

        else:
            self.population = min(
                capacity,
                int(
                    self.population
                    * (1 + adjusted_rules["growth_rate"])
                )
            )

        income = int(
            self.population * adjusted_rules["tax_per_person"]
        )

        upkeep = int(
            self.infrastructure
            * adjusted_rules["upkeep_per_infrastructure"]
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
            attribute = resource.lower()
            current_value = getattr(self, attribute)

            if effect["is_percentage"]:
                change = int(current_value * amount / 100)
            else:
                change = amount

            if change < 0 and self.trait.NAME == "Militaristic":
                change = self.trait.reduce_event_loss(resource, change)

            new_value = current_value + change

            if attribute in ("infrastructure", "technology"):
                new_value = max(1, new_value)
            else:
                new_value = max(0, new_value)

            setattr(self, attribute, new_value)

    
    def  apply_investment(self,resource,rules):
        if resource == "Population":
            cost = int(self.population * rules["population_investment_cost"])
            gain = int(self.population * rules["population_investment_gain"])
        elif resource == "Food":
            cost = int(self.population * rules["food_investment_cost"])
            gain = int(self.population * rules["food_investment_gain"])
        elif resource == "Treasury":
            cost = 0
            gain = int(self.population * rules["treasury_investment_gain"])
        elif resource == "Infrastructure":
            cost = int(self.infrastructure *
                    rules["infrastructure_investment_cost"])
            gain = rules["infrastructure_investment_gain"]
        elif resource == "Technology":
            cost = int(self.technology * rules["technology_investment_cost"])
            gain = rules["technology_investment_gain"]
        else:
            return
        gain = self.trait.investment_gain(resource, gain)

        self.treasury -= cost

        if resource == "Population":
            self.population += gain

        elif resource == "Food":
            self.food += gain

        elif resource == "Treasury":
            self.treasury += gain

        elif resource == "Infrastructure":
            self.infrastructure += gain

        elif resource == "Technology":
            self.technology += gain
        self.population = max(0, self.population)


        self.food = max(0, self.food)
        self.treasury = max(0, self.treasury)
        self.infrastructure = max(1, self.infrastructure)
        self.technology = max(1, self.technology)
        self.start_cooldown(resource, rules)


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
    
    def decrease_cooldowns(self):
     for resource in list(self.investment_cooldowns):
        self.investment_cooldowns[resource] -= 1

        if self.investment_cooldowns[resource] <= 0:
            del self.investment_cooldowns[resource]
    
    def start_cooldown(self, resource, rules):
        self.investment_cooldowns[resource] = (
            rules["cooldown_turns"] + 1
        )

    def can_advance_stage(self, stages):
        next_stage_number = self.stage + 1

        for stage in stages:
            if stage["number"] == next_stage_number:
                return (
                    self.population >= stage["min_population"]
                    and self.infrastructure >= stage["min_infrastructure"]
                    and self.technology >= stage["min_technology"]
                    and self.food > 0
                    and self.treasury > 0
                )

        return False
    
    def advance_year(self):
        self.year += 10
    
    def check_end_condition(self, rules, zero_food_turns):
        if self.population < rules["minimum_population"]:
            return "Population fell below the minimum"

        if zero_food_turns >= rules["max_zero_food_turns"]:
            return "Food has been zero for two consecutive turns"

        if self.stage == 10:
            return "SPACE COLONY REACHED"

        if self.year >= self.MAX_YEAR:
            return "Year 3000 reached"

        return None
