import bobbie
import time

from bobbie.node_config import CONFIG

if __name__ == "__main__":
    bobbie = bobbie.Bobbie("COM8")

    node = bobbie.create_node(0)
    node.config.set( CONFIG.SerialBridge, 2 )

    while True:
        bobbie.poll()
        time.sleep(0.01)

