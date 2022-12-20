import threading, time
from logger import Plotter
from sensor import *

alive = threading.Event()

def driver(sensor_instance, logger_instance, time_diff):
    global alive
    t=0;
    while alive.is_set():
        sensor_instance.update_value()
        v = sensor_instance.get_value()
        logger_instance.update_arrays(t*time_diff, v)
        t+=1
        time.sleep(time_diff)

if __name__ == "__main__":
    alive.set()
    plotter = Plotter(30, alive, 0.1)
    # sensor = Light_Sensor(0.03, 100)
    # plotter.start([0,1000], sensor.name, sensor.value_name)
    sensor = Temperature_Sensor(0.03, 24)
    plotter.start([-20, 80], sensor.name, sensor.value_name)
    # sensor = Pressure_Sensor(0.007, 40)
    # plotter.start([-20, 200], sensor.name, sensor.value_name)
    # sensor = Motion_Sensor()
    # plotter.start([0, 1], sensor.name, sensor.value_name)
    driver_thread = threading.Thread(target=driver, args=(sensor, plotter, 0.1))
    driver_thread.start()
    plotter.run()
    driver_thread.join()