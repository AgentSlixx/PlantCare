class Plant:
    def __init__(self, plant_name, light_limits, temperature_limits, humidity_limits, moisture_limits):
        self.plant_name = plant_name
        self.light_limits = light_limits
        self.temperature_limits = temperature_limits
        self.humidity_limits = humidity_limits
        self.moisture_limits = moisture_limits
    
    def is_plant_unhealthy_light(self):
        return self.light_current < self.light_limits[0] or self.light_current > self.light_limits[1]

    def is_plant_unhealthy_temperature(self):
        return self.temperature_current < self.temperature_limits[0] or self.temperature_current > self.temperature_limits[1]

    def is_plant_unhealthy_humidity(self):
        return self.humidity_current < self.humidity_limits[0] or self.humidity_current > self.humidity_limits[1]

    def is_plant_unhealthy_moisture(self):
        return self.moisture_current < self.moisture_limits[0] or self.moisture_current > self.moisture_limits[1]
