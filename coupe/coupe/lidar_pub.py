import rclpy
from rclpy.node import Node
from pyrplidar import PyRPlidar
from interfaces.msg import Lid
from Time_Manager import Time_Manager
import time

#connection au lidar
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3)


#variable globale
seuil=650 #distance d'arret
lastCall='go' #evite les répétition d'envoi

class LidarPublisher(Node):

    def __init__(self):
        super().__init__('Lidar_pub')
        self.publisher_= self.create_publisher(Lid,'arret',10)
        self.subscription = self.create_subscription(
            Lid,
            'Debut',
            self.callback_arret,
            10
        )
        self.subscription
        self.scan_lidar()

    def callback(self,proche,angle):
        msg=Lid()
        global lastCall
        if proche==True:
            if angle>=320 or angle<=40:
                msg.etat='stop_avant'
            elif angle>=120 and angle<=220:
                msg.etat='stop_arriere'
            else:
                msg.etat='go'
        else:
            msg.etat='go'
            
        if msg.etat!=lastCall:
            lastCall=msg.etat
            self.publisher_.publish(msg)
            self.get_logger().info('publishing: "%s"' % msg.etat)

    def callback_arret(self,msg):
        self.get_logger().info('demarage : %s' %msg.etat)
        if msg.etat=="go":
            self.action=False
        else:
            self.action=True
        

    def scan_lidar(self):
        self.action=True
        global timer
        timer = Time_Manager.Time()
        while self.action:
            rclpy.spin_once(self)
            time.sleep(0.2)
        timer.launch_counter()
        seuil=650
        lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3)
        lidar.set_motor_pwm(660)
        scan_generator = lidar.start_scan_express(3)
        anglemem=400
        angle=400
        tour=0
        a360=False
        tourmem=0
        err=0
        for i,scan in enumerate(scan_generator()):
            scan = vars(scan)
            dist= scan["distance"]
            angle= int(scan["angle"])
            if angle==359:
                a360=True
            if angle==0 and a360:
                tour+=1
                a360=False
            if (dist<=seuil and dist >= 100) and ((angle>=340 or angle<60)or(angle<200 and angle>140)):
                err+=1
                if err>=15:
                    self.callback(True,angle)
                    anglemem= angle
                    tour=0
                    err=0

            else:
                if anglemem<=angle and tour>15:
                    self.callback(False,angle)
                    anglemem=400
                    err=0 


            if timer.get_time() <= timer.seuil_time():
                self.callback(True,0)
                break

        lidar.stop()
        lidar.set_motor_pwm(0)
        lidar.disconnect()


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


