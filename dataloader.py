
class DataLoader:
    COMMENT_PREFIX = "#"

    @staticmethod
    def parse_number(value):
        """Convert a string to an integer or float."""
        try:
            return int(value)
        except ValueError:
            return float(value)

    def load_rules(self):
        rules = {}

        with open("rules.txt", "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith(self.COMMENT_PREFIX):
                    continue

                try:
                    name, value = line.split("=", 1)
                    name = name.strip()
                    value = value.strip()

                    if not name:
                        raise ValueError("Missing rule name")

                    rules[name] = self.parse_number(value)

                except ValueError:
                    print(
                        f"Warning: Invalid line {line_number} "
                        "in rules.txt. Skipping."
                    )

        return rules

    def load_events(self):
        events = []

        with open("events.txt", "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith(self.COMMENT_PREFIX):
                    continue

                try:
                    parts = line.split(",", 3)

                    if len(parts) != 4:
                        raise ValueError("Incorrect number of fields")

                    name = parts[0].strip()
                    lower = float(parts[1].strip())
                    upper = float(parts[2].strip())
                    effects_text = parts[3].strip()

                    if not name or not (0 <= lower <= upper <= 0.99):
                        raise ValueError("Invalid event fields")

                    effects = {}

                    if effects_text:
                        for effect in effects_text.split(";"):
                            resource, change = effect.strip().split(":", 1)
                            resource = resource.strip()
                            change = change.strip()

                            if not resource or not change:
                                raise ValueError("Invalid effect")

                            is_percentage = change.endswith("%")

                            if is_percentage:
                                change = change[:-1]

                            amount = int(change)

                            effects[resource] = {
                                "amount": amount,
                                "is_percentage": is_percentage
                            }

                    events.append({
                        "name": name,
                        "lower": lower,
                        "upper": upper,
                        "effects": effects
                    })

                except ValueError:
                    print(
                        f"Warning: Invalid line {line_number} "
                        "in events.txt. Skipping."
                    )

        return events

    def load_stages(self):
        stages = []

        with open("stages.txt", "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith(self.COMMENT_PREFIX):
                    continue

                try:
                    parts = line.split(",", 4)

                    if len(parts) != 5:
                        raise ValueError("Incorrect number of fields")

                    stage = {
                        "number": int(parts[0].strip()),
                        "name": parts[1].strip(),
                        "min_population": int(parts[2].strip()),
                        "min_infrastructure": int(parts[3].strip()),
                        "min_technology": int(parts[4].strip())
                    }

                    if stage["number"] < 1 or not stage["name"]:
                        raise ValueError("Invalid stage")

                    if min(
                        stage["min_population"],
                        stage["min_infrastructure"],
                        stage["min_technology"]
                    ) < 0:
                        raise ValueError("Negative requirement")

                    stages.append(stage)

                except ValueError:
                    print(
                        f"Warning: Invalid line {line_number} "
                        "in stages.txt. Skipping."
                    )

        return stages

    def load_all(self):
        try:
            rules = self.load_rules()
            events = self.load_events()
            stages = self.load_stages()

            return rules, events, stages

        except OSError as error:
            print(f"Error loading data files: {error}")
            print("Simulation cannot start.")
            return None
