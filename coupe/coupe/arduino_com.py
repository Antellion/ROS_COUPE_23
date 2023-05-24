from interfaces.srv import Arduino
import rclpy
from rclpy.node import Node
from smbus2 import SMBus


addr = 0x8
bus = SMBus(1)

class Arduinocom(Node):

    def __init__(self):
        super().__init__('arduino_com')
        self.srv = self.create_service(Arduino,'commande_arduino',self.com_callback)

    def com_callback(self,request,reponce):
        bus.write_byte(addr,request.commande)
        repond=bus.read_byte(addr)
        while repond != 0:
            repond=bus.read_byte(addr)
        reponce.realiser=True
        return reponce

def main():
    rclpy.init()

    ardcom= Arduinocom()

    rclpy.spin (ardcom)

    rclpy.shutdown()


if __name__=='__main__':
    main()
    
            
            
