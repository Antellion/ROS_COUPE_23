import rclpy
from rclpy.node import Node
from pyrplidar import PyRPlidar
from interfaces.msg import Lid
import time

#connection au lidar
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3)

lidar.set_motor_pwm(660)

#variable globale
seuil=200 #distance d'arret
lastCall=False #evite les répétition d'envoi

class LidarPublisher(Node):

    def __init__(self):
        super().__init__('Lidar_pub')
        self.publisher_= self.create_publisher(Lid,'arret',10)
        self.scan_lidar()

    def callback(self,proche):
        msg=Lid()
        global lastCall
        if proche!=lastCall:
            if proche==True:
                lastCall=True
                msg.etat='stop'
            else:
                lastCall=False
                msg.etat='go'
            self.publisher_.publish(msg)
            self.get_logger().info('publishing: "%s"' % msg.etat)

    def scan_lidar(self):
        scan_generator = lidar.start_scan_express(3)
        anglemem=400
        angle=400
        tour=0
        a360=False
        tourmem=0
        for i,scan in enumerate(scan_generator()):
            scan = vars(scan)
            dist= scan["distance"]
            angle= int(scan["angle"])
            if angle==359:
                a360=True
            if angle==0 and a360:
                tour+=1
                a360=False
            if dist<=seuil and dist >= 50:
                self.callback(True)
                anglemem= angle
                tourmem=tour
            else:
                if anglemem==angle and tour>tourmem:
                    self.callback(False)
                    anglemem=400 

def main():
    rclpy.init()
    Lidar_node = LidarPublisher()

    rclpy.spin(Lidar_node)

    Lidar_node.destroy_node()
    rclpy.shutdown()

    #stop lidar
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()

if __name__=='__main__':
    main()





