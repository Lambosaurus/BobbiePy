import bobbie
import time

from bobbie.node_config import Config

if __name__ == "__main__":
    bobbie = bobbie.Bobbie("COM7")

    node = bobbie.create_node(-1)
    node.config.set( Config.SerialBridge, 2 )
    
    for i in range(10):
        bobbie.poll()
        time.sleep(0.1)

    bobbie.discover_nodes()

    while True:
        bobbie.poll()
        time.sleep(0.01)

