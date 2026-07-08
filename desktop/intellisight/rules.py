"""The Rules Engine — 'when the camera sees X, do Y'.

Rules are evaluated each detection update against the current events (from the
EventDetector), the live detections, and the drawn zone. Firing is debounced by
a per-rule cooldown so a rule doesn't spam.
"""

COOLDOWN = 2.0  # seconds a rule must wait before it can fire again

# trigger value -> human phrase
TRIGGER_PHRASE = {
    "appears": "appears",
    "disappears": "disappears",
    "lingers": "lingers",
    "enters_zone": "enters the zone",
    "count_over": "in the zone",
}
_ACTION_PHRASE = {
    "alert": "show an alert",
    "notify": "notify me",
    "sound": "play a sound",
    "snapshot": "save a snapshot",
}
_FIRE_VERB = {
    "appears": "appeared",
    "disappears": "left",
    "lingers": "lingering",
    "enters_zone": "entered the zone",
}
# tracker event type -> rule trigger
_EVENT_TRIGGER = {"appeared": "appears", "disappeared": "disappears", "lingered": "lingers"}


class Rule:
    def __init__(self, rule_id, obj, trigger, action, threshold=2, enabled=True):
        self.id = rule_id
        self.obj = obj            # lowercased label, or None = anything
        self.trigger = trigger
        self.action = action
        self.threshold = threshold
        self.enabled = enabled
        self.last_fired = 0.0

    def describe(self) -> str:
        action = _ACTION_PHRASE.get(self.action, self.action)
        if self.trigger == "count_over":
            return f"When ≥ {self.threshold} in the zone → {action}"
        subject = self.obj.title() if self.obj else "Anything"
        return f"When {subject} {TRIGGER_PHRASE.get(self.trigger, self.trigger)} → {action}"

    def fired_text(self, label: str) -> str:
        if self.trigger == "count_over":
            return f"≥{self.threshold} in zone"
        return f"{label} {_FIRE_VERB.get(self.trigger, '')}".strip()


class RulesEngine:
    def __init__(self):
        self.rules = []
        self._next_id = 0
        self._prev_in_zone = {}
        self._prev_count = 0

    def add(self, obj, trigger, action, threshold=2) -> Rule:
        self._next_id += 1
        rule = Rule(self._next_id, obj, trigger, action, threshold)
        self.rules.append(rule)
        return rule

    def remove(self, rule_id) -> None:
        self.rules = [r for r in self.rules if r.id != rule_id]

    def reset_state(self) -> None:
        self._prev_in_zone = {}
        self._prev_count = 0

    def evaluate(self, events, detections, zone, zone_count, now) -> list:
        firings = []

        def fire(rule, label):
            if now - rule.last_fired < COOLDOWN:
                return
            rule.last_fired = now
            firings.append({"rule": rule, "text": rule.fired_text(label)})

        # Event-based triggers (appears / disappears / lingers)
        for event in events:
            trigger = _EVENT_TRIGGER.get(event["type"])
            if trigger is None:
                continue
            for rule in self.rules:
                if (
                    rule.enabled
                    and rule.trigger == trigger
                    and (rule.obj is None or rule.obj == event["label"].lower())
                ):
                    fire(rule, event["label"])

        # Zone-based triggers (enters zone / count over)
        if zone:
            in_zone = {}
            x1, y1, x2, y2 = zone
            for det in detections:
                box = det["box"]
                cx = (box["x1"] + box["x2"]) / 2
                cy = (box["y1"] + box["y2"]) / 2
                if x1 <= cx <= x2 and y1 <= cy <= y2:
                    in_zone[det["id"]] = det["label"]

            for oid, label in in_zone.items():
                if oid in self._prev_in_zone:
                    continue
                for rule in self.rules:
                    if (
                        rule.enabled
                        and rule.trigger == "enters_zone"
                        and (rule.obj is None or rule.obj == label.lower())
                    ):
                        fire(rule, label)

            for rule in self.rules:
                if rule.enabled and rule.trigger == "count_over":
                    if self._prev_count < rule.threshold <= zone_count:
                        fire(rule, str(zone_count))

            self._prev_in_zone = in_zone
            self._prev_count = zone_count
        else:
            self._prev_in_zone = {}
            self._prev_count = 0

        return firings
