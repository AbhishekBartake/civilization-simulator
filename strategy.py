class Strategy:
    BASE_PRIORITIES = {
        "Population": 15,
        "Food": 28,
        "Treasury": 12,
        "Infrastructure": 22,
        "Technology": 18
    }

    TIE_BREAK_ORDER = [
        "Population",
        "Food",
        "Treasury",
        "Infrastructure",
        "Technology"
    ]

    def __init__(self, trait):
        self.trait = trait

    def get_base_priority(self, resource):
        base_priority = self.BASE_PRIORITIES[resource]
        trait_bonus = self.trait.priority_bonus(resource)

        return base_priority + trait_bonus

    def get_resource_need(self, resource, civilisation, rules):
        if resource == "Food":
            food_consumption = (
                civilisation.population * rules["food_per_person"]
            )

            if civilisation.food < food_consumption:
                return 25

        elif resource == "Infrastructure":
            capacity = (
                civilisation.infrastructure
                * rules["capacity_per_infrastructure"]
            )

            if civilisation.population > 0.90 * capacity:
                return 25
            elif civilisation.population > 0.75 * capacity:
                return 12

        elif resource == "Technology":
            if civilisation.technology < 3:
                return 10

        elif resource == "Treasury":
            infrastructure_cost = (
                civilisation.infrastructure
                * rules["infrastructure_investment_cost"]
            )
            technology_cost = (
                civilisation.technology
                * rules["technology_investment_cost"]
            )

            if (
                infrastructure_cost > civilisation.treasury
                and technology_cost > civilisation.treasury
            ):
                return 15

        return 0
    
    def get_event_recovery_bonus(self, resource, event):
        effect = event["effects"].get(resource)

        if effect is None:
            return 0

        if effect["amount"] >= 0:
            return 0

        recovery_bonuses = {
            "Food": 20,
            "Population": 15,
            "Treasury": 15,
            "Infrastructure": 25,
            "Technology": 20
        }

        return recovery_bonuses.get(resource, 0)
    
    def get_advancement_need(self, resource, civilisation, stages):
        next_stage_number = civilisation.stage + 1
        next_stage = None

        for stage in stages:
            if stage["number"] == next_stage_number:
                next_stage = stage
                break

        if next_stage is None:
            return 0

        requirements = {
            "Population": (
                civilisation.population,
                next_stage["min_population"]
            ),
            "Infrastructure": (
                civilisation.infrastructure,
                next_stage["min_infrastructure"]
            ),
            "Technology": (
                civilisation.technology,
                next_stage["min_technology"]
            )
        }

        if resource not in requirements:
            return 0

        current_value, required_value = requirements[resource]

        if current_value >= required_value:
            return 0

        missing_requirements = 0

        for current, required in requirements.values():
            if current < required:
                missing_requirements += 1

        bonus = 20

        if missing_requirements == 1:
            bonus += 15

        return bonus
    
    def get_priority_score(self, resource, civilisation, rules, stages, event):
        base_priority = self.get_base_priority(resource)

        resource_need = self.get_resource_need(
            resource, civilisation, rules
        )

        advancement_need = self.get_advancement_need(
            resource, civilisation, stages
        )

        event_effect = self.get_event_recovery_bonus(
            resource, event
        )

        return (
            base_priority
            + resource_need
            + advancement_need
            + event_effect
        )
    

    def can_invest(self, resource, civilisation, rules):
        if resource in civilisation.investment_cooldowns:
            return False

        cost_key = resource.lower() + "_investment_cost"
        cost_rate = rules[cost_key]

        if resource in ("Population", "Food"):
            cost = int(civilisation.population * cost_rate)

        elif resource == "Treasury":
            cost = 0

        else:
            resource_value = getattr(civilisation, resource.lower())
            cost = int(resource_value * cost_rate)

        return civilisation.treasury >= cost


    def choose_investment(self, civilisation, rules, stages, event):
        eligible_resources = []

        for resource in civilisation.RESOURCE_NAMES:
            if self.can_invest(resource, civilisation, rules):
                eligible_resources.append(resource)

        if not eligible_resources:
            return None

        food_production = int(
            civilisation.population
            * (
                rules["food_base_production"]
                + rules["food_production_per_technology"]
                * civilisation.technology
            )
        )

        food_consumption = int(
            civilisation.population * rules["food_per_person"]
        )

        projected_food = (
            civilisation.food + food_production - food_consumption
        )

        if projected_food < food_consumption:
            if "Food" in eligible_resources:
                return "Food"
            if "Infrastructure" in eligible_resources:
                return "Infrastructure"

        scores = {}

        for resource in eligible_resources:
            scores[resource] = self.get_priority_score(
                resource, civilisation, rules, stages, event
            )

        highest_score = max(scores.values())

        for resource in self.TIE_BREAK_ORDER:
            if resource in scores and scores[resource] == highest_score:
                return resource
