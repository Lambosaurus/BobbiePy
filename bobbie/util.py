import time
import bobbie.node_config as cfg

def scan_bus(bobbie):
    host_node = bobbie.create_node(-1)
    
    host_node.config.set(cfg.Config.SerialBridge, cfg.SerialBridge.Local)
    host_node.config.get(cfg.Config.Address)
    
    nodes = []
    start = time.time()
    while time.time() - start > 1.0:
        bobbie.poll()

    node.remove()
    return nodes

