
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
