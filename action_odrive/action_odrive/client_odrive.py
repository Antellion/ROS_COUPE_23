import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionClient

from interfaces.action import Omoteur


class clientMoteur(Node):
    def __init__(self):
        super().__init__('odrive_client')
        self._action_client = ActionClient(self,Omoteur,'action_moteur')
        self.feuillederoute()

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

    def feuillederoute(self):
        self.send_goal(10000,"Avancer")
        self.waitandspin()
        #self.send_goal(90,"Tourner")
        #self.waitandspin()
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

    action_client = clientMoteur()

    rclpy.spin(action_client)

if __name__=='__main__':
    main()
    

