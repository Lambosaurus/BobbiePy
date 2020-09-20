import bobbie
import time
import random

from bobbie.config import Config
from plotter import Plotter


if __name__ == "__main__":

    bobbie = bobbie.Bobbie("COM7")

    node = bobbie.immediate_node.config.set( Config.SerialBridge, 2 )
    nodes = bobbie.discover_nodes().wait()
    for n in nodes:
        n.error.subscribe(lambda x: print(x), True)
        print(n)
    
    plot = Plotter(100, (0, 10.0))
    plot.start()
    
    servo = bobbie.nodes[3]
    servo.config.set( Config.FeedbackActive, 100 )
    servo.config.set( Config.FeedbackIdle, 100)
    servo.current.subscribe( lambda x: plot.update(x) )

    freq = 20
    while True:
        k = random.randint(-400, 400)
        for i in range(int(freq/2)):
            bobbie.poll()
            n.pulse([(0,1500+k),(1,1500-k)])
            time.sleep(1.0/freq)

