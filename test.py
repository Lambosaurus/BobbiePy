import bobbie
import time

from bobbie.config import Config

if __name__ == "__main__":
    bobbie = bobbie.Bobbie("COM7")

    node = bobbie.immediate_node.config.set( Config.SerialBridge, 2 )
    nodes = bobbie.discover_nodes().wait()
    for n in nodes:
        n.check_exists().callback( lambda x: print(x) )
        n.error.subscribe(lambda x: print(x), True)
        #print( n.check_exists().wait() )
    
    bobbie.wait_for_promises()

    while True:
        bobbie.poll()
        time.sleep(0.01)

