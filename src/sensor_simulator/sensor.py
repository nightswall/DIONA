import numpy as np
import matplotlib.pyplot as plt

class Sensor:
    def __init__(self, name, value_name):
        self.value = None
        self.name = name
        self.value_name = value_name

    def get_value(self):
        return self.value

    def update_value(self):
        pass

    def alter_value(self, fun):
        pass

    def get_value(self):
        pass

class Digital_Sensor(Sensor):
    """
    Digital sensor dependent of a threshold and poisson distribution that generate value 0 or 1
    """
    def __init__(self, l, threshold, name, value_name):
        super().__init__(name, value_name)
        self.l = l
        self.threshold = threshold
        self.value = False

    def update_value(self):
        if np.random.poisson(self.l) > self.threshold:
            self.value = not self.value

    def alter_value(self, fun):
        pass

    def get_value(self):
        pass

class Analog_Sensor(Sensor):
    """
    Analog sensor dependent of a intensity and uniform distribution that generate value between 0 and 1023
    """
    def __init__(self, intensity, name, value_name):
        super().__init__(name, value_name)
        self.intensity = intensity*1023
        self.value = 511

    def update_value(self):
        if self.value+self.intensity > 1023: self.value += int(np.random.uniform(-2*self.intensity, -self.intensity))
        elif self.value-self.intensity < 0: self.value += int(np.random.uniform(self.intensity, 2*self.intensity))
        else: self.value += int(np.random.uniform(-self.intensity, self.intensity))

    def alter_value(self, fun):
        return fun(self.get_value())

    def get_value(self):
        pass

class Temperature_Sensor(Analog_Sensor):
    def __init__(self, intensity, init_val=None):
        super().__init__(intensity, "Temperature Sensor", "Temperature (°C)")
        if init_val:
            self.value = int(init_val*10.0+500)

    def get_value(self):
        return (self.value-500)/10.0 ;

class Light_Sensor(Analog_Sensor):
    def __init__(self, intensity, init_val=None):
        super().__init__(intensity, "Light Sensor", "Luminance",)
        if init_val:
            self.value = 102400/(init_val*150+100)

    def get_value(self):
        return ((1024-self.value)*1000)/(150*self.value)

class Pressure_Sensor(Analog_Sensor):
    def __init__(self, intensity, init_val=None):
        super().__init__(intensity, "Pressure Sensor", "Pressure (kPa)")
        if init_val:
            self.value = (init_val+13.4)/0.59

    def get_value(self):
        return 0.59*self.value-13.4

class Occupancy_Sensor(Digital_Sensor):
    def __init__(self):
        super().__init__(10, 15, "Occupancy Sensor", "Is Occupancy")

class Motion_Sensor(Digital_Sensor):
    def __init__(self):
        super().__init__(10, 12, "Motion Sensor", "Is Motion")