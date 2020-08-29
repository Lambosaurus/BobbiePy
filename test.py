import bobbie
import time

if __name__ == "__main__":
    bobbie = bobbie.Bobbie("COM6")
    
    while True:

        bobbie.poll()
        time.sleep(0.01)

