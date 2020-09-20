import bobbie
import time

from bobbie.config import Config

if __name__ == "__main__":
    bobbie = bobbie.Bobbie("COM7")

    node = bobbie.immediate_node.config.set( Config.SerialBridge, 2 )
    nodes = bobbie.discover_nodes().wait()
    for n in nodes:
        n.error.subscribe(lambda x: print(x), True)
        print(n)
    
    bobbie.wait_for_promises()

    servo = bobbie.nodes[3]
    servo.config.set( Config.FeedbackActive, 100 )
    servo.config.set( Config.FeedbackIdle, 100)
    servo.voltage.subscribe( lambda x: print("Voltage: {}".format(x)) )

    while True:
        for i in range(1000, 2000, 50):
            bobbie.poll()
            time.sleep(0.1)
            n.pulse([(0,i)])

