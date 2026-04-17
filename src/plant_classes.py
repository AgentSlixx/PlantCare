class Plant:
    def __init__(self, plant_name, light_limits, temperature_limits, humidity_limits, moisture_limits):
        self.plant_name = plant_name
        self.light_limits = light_limits
        self.temperature_limits = temperature_limits
        self.humidity_limits = humidity_limits
        self.moisture_limits = moisture_limits

    def _limits_for_metric(self, metric_name):
        limits = {
            "sunlight": self.light_limits,
            "temperature": self.temperature_limits,
            "humidity": self.humidity_limits,
            "moisture": self.moisture_limits,
        }
        return limits.get(metric_name)

    def metric_status(self, metric_name, current_value):
        limits = self._limits_for_metric(metric_name)
        if limits is None or current_value is None:
            return "unknown"

        min_value, max_value = limits
        if min_value is None or max_value is None:
            return "unknown"
        if current_value < min_value:
            return "low"
        if current_value > max_value:
            return "high"
        return "good"

    def overall_health(self, current_readings):
        # Health starts at 100 and loses points for each reading outside its ideal range
        score = 100
        for metric_name in ["humidity", "temperature", "moisture", "sunlight"]:
            current_value = current_readings.get(metric_name)
            limits = self._limits_for_metric(metric_name)
            if limits is None or current_value is None:
                score -= 10
                continue

            min_value, max_value = limits
            if min_value is None or max_value is None:
                score -= 10
            elif current_value < min_value:
                score -= min(25, int(min_value - current_value) + 5)
            elif current_value > max_value:
                score -= min(25, int(current_value - max_value) + 5)

        return max(0, min(100, score))

    def health_category(self, current_readings):
        score = self.overall_health(current_readings)
        return self.category_from_score(score)

    def health_change(self, current_readings):
        # Decreases plant health score based on how many metrics are out of range and how critical they are
        # Also increases health slightly if all metrics are good
        change = 0
        all_good = True
        for metric_name in ["humidity", "temperature", "moisture", "sunlight"]:
            current_value = current_readings.get(metric_name)
            status = self.metric_status(metric_name, current_value)
            if status == "unknown":
                change -= 0.5
                all_good = False
            elif status != "good":
                change -= 1
                all_good = False

            if metric_name in ["humidity", "moisture", "sunlight"] and current_value == 0:
                change -= 2

        if all_good:
            change += 0.5
        return change

    @staticmethod
    def category_from_score(score):
        if score >= 70:
            return "Healthy"
        if score >= 40:
            return "Warning"
        return "Critical"

    def care_advice(self, current_readings):
        advice = []
        advice_text = {
            ("moisture", "low"): "Add water",
            ("moisture", "high"): "Reduce watering",
            ("humidity", "low"): "Increase humidity",
            ("humidity", "high"): "Reduce humidity",
            ("temperature", "low"): "Move plant somewhere warmer",
            ("temperature", "high"): "Move plant somewhere cooler",
            ("sunlight", "low"): "Provide more sunlight",
            ("sunlight", "high"): "Move plant into shade",
        }

        for metric_name in ["moisture", "humidity", "temperature", "sunlight"]:
            status = self.metric_status(metric_name, current_readings.get(metric_name))
            message = advice_text.get((metric_name, status))
            if message:
                advice.append(message)

        if not advice:
            advice.append("Plant conditions are good")
        return advice

    def to_dict(self):
        return {
            "name": self.plant_name,
            "light_limits": self.light_limits,
            "temperature_limits": self.temperature_limits,
            "humidity_limits": self.humidity_limits,
            "moisture_limits": self.moisture_limits,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("name", "Unknown plant"),
            data.get("light_limits", (None, None)),
            data.get("temperature_limits", (None, None)),
            data.get("humidity_limits", (None, None)),
            data.get("moisture_limits", (None, None)),
        )