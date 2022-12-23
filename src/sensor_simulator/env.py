import time, json
import numpy as np

class analogImitation:
    def __init__(self, init_val, effect):
        self.value = init_val
        self.effect = effect
    
    def update_val(self, critical, change):
        if self.value > critical["max"]: self.value -= abs(np.random.uniform(0.4*change, 0.6*change))
        elif self.value < critical["min"]: self.value += abs(np.random.uniform(0.4*change, 0.6*change))
        else: self.value += np.random.uniform(2*change, change)
        
    def get_value(self):
        return self.value
    
    def effect_function(self, value):
        return value*(1-self.effect)+self.value*self.effect

class digitalImitation:
    def __init__(self):
        self.lmbda = 0
        self.threshold = 0

    def update_val(self, threshold, lmbda, step):
        self.lmbda = self.lmbda+step if self.lmbda else lmbda
        self.threshold = threshold

    def effect_function(self, lmbda, threshold):
        return int(self.lmbda), int(threshold-self.lmbda*self.threshold)

class Environment:
    def __init__(self, path):
        with open(path, "r") as f:
            variables = json.load(f)
        self.weekly_data = variables["weekly"]
        self.daily_data = variables["daily"]
        self.w_index = None
        self.d_index = None

    def simulator(self, t, imitation, sensor_specs):
        self.w_index = t//144 % 7
        self.d_index = t//36 % 4
        if sensor_specs["type"] == "analog":
            imitation.update_val(self.weekly_data[str(self.w_index)][sensor_specs["type"]][sensor_specs["week"]], 
                                    self.daily_data[str(self.d_index)][sensor_specs["type"]][sensor_specs["day"]]
                                )
        elif sensor_specs["type"] == "digital":
            half_d_index = t//72 % 8
            prev_lmbda = self.daily_data[str(half_d_index % 4)][sensor_specs["type"]][sensor_specs["day"]]
            next_lmbda = self.daily_data[str((half_d_index+1) % 4)][sensor_specs["type"]][sensor_specs["day"]]
            step = (next_lmbda-prev_lmbda)/72
            imitation.update_val(self.weekly_data[str(self.w_index)][sensor_specs["type"]][sensor_specs["week"]], 
                                    prev_lmbda,
                                    step
                                )
    
    def get_name(self, d):
        if d == "w":
            return self.weekly_data[str(self.w_index)]["name"]
        elif d == "d":
            return self.daily_data[str(self.d_index)]["name"]

# if __name__ == "__main__":
#     t=0
#     temp_imit = analogImitation(3, 0.1)
#     env = Environment("./environment.json")
#     while True:
#         env.simulator(t, temp_imit)
#         print(env.get_name("w"), env.get_name("d"), f'{t//6 % 24}:{t%6}0 tempeture: {"{:.2f}".format(temp_imit.get_value())}')
#         t+=1
#         time.sleep(0.1)