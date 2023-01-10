import threading, time
from logger import *
from sensor import *
from env import *

alive = threading.Event()

def driver(sensor_instance, logger_instance, time_diff, env_imitation, env_object):
    global alive
    t=0;
    while alive.is_set():
        sensor_instance.update_value()
        # For sensors without enviroment changes and simple logger
        v = sensor_instance.get_value()
        logger_instance.update_arrays(t*time_diff, v)

        # # For sensors with enviroment changes and calendar logger
        # v = sensor_instance.alter_value(env_imitation.effect_function)
        # env_object.simulator(t, env_imitation, sensor_instance.specs)
        # logger_instance.update_arrays(t*time_diff, v, env_object.get_name("w"), env_object.get_name("d"))
        t+=1
        time.sleep(time_diff)

if __name__ == "__main__":
    alive.set()
    # plotter = calendarPlotter(30, alive, 0.1)
    plotter = Plotter(30, alive, 0.1)
    environment = Environment("./environment.json")
    # sensor = Light_Sensor(0.03, 100)
    # plotter.start([0,1000], sensor.name, sensor.value_name)
    # sensor = Temperature_Sensor(0.005, 24)
    # imitation = analogImitation(3, 0.99)
    # plotter.start([-20, 80], sensor.name, sensor.value_name)
    sensor = Pressure_Sensor(0.007, 40)
    imitation = None
    plotter.start([-20, 200], sensor.name, sensor.value_name)
    # sensor = Occupancy_Sensor()
    # imitation = digitalImitation()
    # plotter.start([0, 1], sensor.name, sensor.value_name)
    driver_thread = threading.Thread(target=driver, args=(sensor, plotter, 0.1, imitation, environment))
    driver_thread.start()
    plotter.run()
    driver_thread.join()