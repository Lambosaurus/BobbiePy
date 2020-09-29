import bobbie
import time
import random

from bobbie.config import Config
#from plotter import Plotter


if __name__ == "__main__":
    bobbie = bobbie.Bobbie("COM6")

    node = bobbie.immediate_node.config.set( Config.SerialBridge, 2 )
    nodes = bobbie.discover_nodes().wait()
    for n in nodes:
        n.error.subscribe(lambda x: print(x), True)
        print(n)
    
    #plot = Plotter(100, (0, 10.0))
    #plot.start()
    
    servo = bobbie.nodes[3]
    servo.config.set( Config.FeedbackActive, 100 )
    servo.config.set( Config.FeedbackIdle, 100)
    #servo.current.subscribe( lambda x: plot.update(x) )

    motor = bobbie.nodes[2]
    motor.config.set( Config.MotorBrakeThreshold, 0 )

    freq = 20
    while True:
        for i in list(range(-256, 256, 4)) + list(range(256, -256, -4)):
            bobbie.poll()
            motor.throttle(i, i)
            time.sleep(1.0/freq)

