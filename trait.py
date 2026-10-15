class AgriculturalTrait:
    NAME = "Agricultural"

    def adjust_rules(self, rules):
        adjusted_rules = rules.copy()
        adjusted_rules["tax_per_person"] *= 0.90
        return adjusted_rules

    def priority_bonus(self, resource):
        return 0

    def investment_gain(self, resource, base_gain):
        if resource.lower() == "food":
            return int(base_gain * 1.10)
        return base_gain


class CommercialTrait:
    NAME = "Commercial"

    def adjust_rules(self, rules):
        adjusted_rules = rules.copy()
        adjusted_rules["growth_rate"] *= 0.90
        return adjusted_rules

    def priority_bonus(self, resource):
        return 0

    def investment_gain(self, resource, base_gain):
        if resource.lower() == "treasury":
            return int(base_gain * 1.10)
        return base_gain


class MilitaristicTrait:
    NAME = "Militaristic"

    def adjust_rules(self, rules):
        adjusted_rules = rules.copy()
        adjusted_rules["upkeep_per_infrastructure"] *= 1.10
        return adjusted_rules

    def priority_bonus(self, resource):
        return 0

    def investment_gain(self, resource, base_gain):
        return base_gain

    def reduce_event_loss(self, resource, amount):
        return int(amount * 0.75)



class ScientificTrait:
    NAME = "Scientific"

    def adjust_rules(self, rules):
        adjusted_rules = rules.copy()
        adjusted_rules["upkeep_per_infrastructure"] *= 1.10
        return adjusted_rules

    def priority_bonus(self, resource):
        return 0

    def investment_gain(self, resource, base_gain):
        if resource.lower() == "technology":
            return base_gain + 1
        return base_gain


class EngineeringTrait:
    NAME = "Engineering"

    def adjust_rules(self, rules):
        adjusted_rules = rules.copy()
        adjusted_rules["growth_rate"] *= 0.95
        return adjusted_rules

    def priority_bonus(self, resource):
        if resource.lower() == "infrastructure":
            return 6
        return 0

    def investment_gain(self, resource, base_gain):
        if resource.lower() == "infrastructure":
            return base_gain + 1
        return base_gain
