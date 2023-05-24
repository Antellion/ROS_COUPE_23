import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionClient

from interfaces.srv import Arduino
from interfaces.action import Omoteur
from interfaces.msg import Lid

class MasterCoupe(Node):

    # Initialisation du noeud
    def __init__(self):
        super().__init__('master_coupe')
        self._action_client = ActionClient(self,Omoteur,'action_moteur')

        self._client=self.create_client(Arduino,'commande_arduino')
        while not self._client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, wait')
        self.req = Arduino.Request()

        self._start_publisher= self.create_publisher(Lid,'Debut',10)

        self.subscription = self.create_subscription(
            Lid,
            'screen',
            self.listener_callback,
            10
        )
        self.subscription

        self.feuillederoute()

    # Communication avec arduino

    def wait_for_request(self,tag):
        self.req.commande = tag
        fut = self._client.call_async(self.req)
        rclpy.spin_until_future_complete(self,fut)
        return fut.result()

    def no_wait_request(self,tag):
        self.req.commande = tag
        fut = self.clients.call_async(self.req)
        fut.cancel()

    # Communication Odrive

    def send_goal(self,dist, at):
        goal_msg= Omoteur.Goal()
        goal_msg.distmm=dist
        goal_msg.aout=at

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_responce_callback)

    def goal_responce_callback(self, future):
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().info('goalRjected')
            return
        self.get_logger().info('goal accepted')

        self._get_result_future = self.goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        self.wait = future.result().result.arrive
        self.get_logger().info('fini')

    def feedback_callback(self, feedback_msg):
        self.retour=feedback_msg.feedback
        self.get_logger().info('Received : {0}'.format(self.retour.distr))


    def waitandspin(self):
        self.wait=False
        while not self.wait:
            rclpy.spin_once(self)
        self.get_logger().info('goal achieved succesfully')

    def cancel_callback(self, future):
        self.get_logger().info("goal cancelled")
        self.get_logger().info('goal cancelled last result : {0}'.format(self.retour.distr))


    #Sécance démarage

    def publishgo(self,init):
        msg=Lid()
        if init:
            msg.etat="go"
        else:
            msg.etat="Wait"
        self._start_publisher.publish(msg)
        self.get_logger().info('publish "%s"' %msg.etat)

    #side color

    def listener_callback(self,msg):
        self.get_logger().info('couleur "%s"' %msg.etat)
        self.couleur=msg.etat

    #Code de route 
    def coteV(self):
        self.send_goal(340,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(88,"Tourner")
        self.waitandspin()
        self.send_goal(995,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.wait_for_request(2)
        self.send_goal(-210,"Avancer")
        self.waitandspin()
        time.sleep(1)
        #pause marron
        self.send_goal(88,"Tourner")
        self.waitandspin()
        self.send_goal(440,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(93,"Tourner")
        self.waitandspin()
        self.send_goal(460,"Avancer")
        self.waitandspin()
        time.sleep(1)
        #pause jaune
        self.send_goal(92,"Tourner")
        self.waitandspin()
        self.send_goal(420,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(45,"Tourner")
        self.waitandspin()
        self.send_goal(45,"Tourner")
        self.waitandspin()
        self.send_goal(520,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.wait_for_request(2)
        #pause creme
        self.send_goal(-260,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(-183,"Tourner")
        self.waitandspin()
        self.send_goal(1600,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(-40,"Tourner")
        self.waitandspin()
        self.send_goal(400,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(45,"Tourner")
        self.waitandspin()
        self.send_goal(440,"Avancer")
        self.waitandspin()
        time.sleep(1)


    def coteB(self):
        self.send_goal(340,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(-88,"Tourner")
        self.waitandspin()
        self.send_goal(995,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.wait_for_request(2)
        self.send_goal(-210,"Avancer")
        self.waitandspin()
        time.sleep(1)
        #pause marron
        self.send_goal(-88,"Tourner")
        self.waitandspin()
        self.send_goal(440,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(-93,"Tourner")
        self.waitandspin()
        self.send_goal(460,"Avancer")
        self.waitandspin()
        time.sleep(1)
        #pause jaune
        self.send_goal(-92,"Tourner")
        self.waitandspin()
        self.send_goal(420,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(-45,"Tourner")
        self.waitandspin()
        self.send_goal(-45,"Tourner")
        self.waitandspin()
        self.send_goal(520,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.wait_for_request(2)
        #pause creme
        self.send_goal(-260,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(183,"Tourner")
        self.waitandspin()
        self.send_goal(1600,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(40,"Tourner")
        self.waitandspin()
        self.send_goal(400,"Avancer")
        self.waitandspin()
        time.sleep(1)
        self.send_goal(-45,"Tourner")
        self.waitandspin()
        self.send_goal(440,"Avancer")
        self.waitandspin()
        time.sleep(1)
        
    def feuillederoute(self):
        self.couleur='wait'
        while self.couleur!='Vert' and self.couleur!='Bleu':
            rclpy.spin_once(self)
            time.sleep(0.2)
        self.wait_for_request(1)
        self.publishgo(True)
        time.sleep(1.5)
        if self.couleur=='Vert':
            self.coteV()
        else:
            self.coteB()
        #self.send_goal(350,"Avancer")
        #self.waitandspin()
        #self.send_goal(90,"Tourner")
        #self.waitandspin()
        #self.send_goal(180,"Tourner")
        #self.waitandspin()
        #self.send_goal(90,"Tourner")
        #self.waitandspin()


def main():
    rclpy.init()

    rosmaster=MasterCoupe()

    rclpy.spin(rosmaster)

    rosmaster.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
