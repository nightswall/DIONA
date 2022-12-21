import time
import numpy as np

day_part = [{"part": "night",
                "diff_temp": -1.0
            },
            {"part": "morning",
                "diff_temp": 0.5
            },
            {"part": "noon",
                "diff_temp": 1.0
            },
            {"part": "evening",
                "diff_temp": -0.5
            }]

week_part = [{"part": "mon",
                "critical_temp":{"max": 7, "min": -3},
             },
             {"part": "tue",
                "critical_temp":{"max": 8, "min": -4},
             },
             {"part": "wed",
                "critical_temp":{"max": 5, "min": -9},
             },
             {"part": "thu",
                "critical_temp":{"max": 4, "min": 1},
             },
             {"part": "fri",
                "critical_temp":{"max": 9, "min": 3},
             },
             {"part": "sat",
                "critical_temp":{"max": 10, "min": 2},
             },
             {"part": "sun",
                "critical_temp":{"max": 14, "min": 0},
             }]


class analogImitation:
    def __init__(self, init_val, effect):
        self.value = init_val
        self.effect = effect
    
    def update_val(self, critical, change):
        if self.value > critical['max']: self.value -= abs(np.random.uniform(0.4*change, 0.6*change))
        elif self.value < critical['min']: self.value += abs(np.random.uniform(0.4*change, 0.6*change))
        else: self.value += np.random.uniform(2*change, change)
        
    def get_value(self):
        return self.value
    
    def effect_function(self, value):
        return value*(1-self.effect)+self.value*self.effect

def simulator(t, imitation):
    w_index = t//144 % 7
    d_index = t//36 % 4
    imitation.update_val(week_part[w_index]["critical_temp"], day_part[d_index]["diff_temp"])

# if __name__ == "__main__":
#     t=0
#     environ_temperature = randomAnalog(3, 0.1)
#     while True:
#         w_index = t//144 % 7
#         d_index = t//36 % 4
#         print(week_part[w_index]["part"], day_part[d_index]["part"], f'{t//6 % 24}:{t%6}0 tempeture: {"{:.2f}".format(environ_temperature.get_value())}')
#         environ_temperature.update_val(week_part[w_index]["critical_temp"], day_part[d_index]["diff_temp"])
#         t+=1
#         time.sleep(0.1)