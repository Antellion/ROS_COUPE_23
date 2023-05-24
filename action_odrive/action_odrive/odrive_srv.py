import rclpy
from rclpy.node import Node
import odrive
from odrive.enums import *
from math import *
from interfaces.action import Omoteur
from interfaces.msg import Lid
import time

from rclpy.action import ActionServer
from rclpy.action import CancelResponse
from rclpy.action import GoalResponse
from rclpy.executors import MultiThreadedExecutor

D_roue = 71.06
L_robot = 267
P_roue = D_roue * pi
P_robot = L_robot * pi

my_drive = odrive.find_any()

class OdriveServeur(Node):

    def __init__(self):
        super().__init__('moteur_action_serveur')
        
        self.goal = Omoteur.Goal()

        
        print("Coucou, je suis bien connecte et ma tension est de " + str(my_drive.vbus_voltage) + "V !")
        my_drive.clear_errors()


        self._action_server = ActionServer(
            self,
            Omoteur,
            'action_moteur',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )
        self.subscription = self.create_subscription(
            Lid,
            'arret',
            self.listener_callback,
            10
        )
        self.subscription
        self.stop = False

    def goal_callback(self,goal_request):
        self.get_logger().info('Received goal request :')
        self.goal=goal_request
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('received cancel request')
        return CancelResponse.ACCEPT
    
    def listener_callback(self,msg):
        self.get_logger().info('etat: "%s"' % msg.etat)
        if msg.etat=='stop':
            self.stop=True
        else :
            self.stop=False

    def calcul_distance(self,Distance):
        tour = Distance/P_roue
        return tour

    #Valeur à entrée en °, +X° <=> Gauche et -X° <=> Droit
    def calcul_angle(self,Angle):
        rad = Angle*pi/180
        tour = (rad*P_robot)/(2*pi*P_roue)
        return tour

    def demarrage(self,posMax,posMin):
        my_drive.axis0.controller.input_pos = posMax
        my_drive.axis1.controller.input_pos = posMin
        while (my_drive.axis1.encoder.vel_estimate <= 0.1 and my_drive.axis0.encoder.vel_estimate <= 0.1):
            self.get_logger().info('attente de demarrage')
            time.sleep(0.2)
            print(my_drive.axis1.encoder.vel_estimate)
            print(my_drive.axis0.encoder.vel_estimate)
        return False

    def execute_callback(self, goal_handle):

        feedback_msg = Omoteur.Feedback()
        redemarage = False
        
        if self.goal.aout=="Avancer":
            time.sleep(0.2)
            print(self.goal.distmm)
            posvoulu=self.calcul_distance(self.goal.distmm)
            posArriver = my_drive.axis0.encoder.pos_estimate + posvoulu
            posmArriver = my_drive.axis1.encoder.pos_estimate - posvoulu
            my_drive.axis1.controller.input_pos = my_drive.axis1.encoder.pos_estimate - posvoulu
            my_drive.axis0.controller.input_pos = my_drive.axis0.encoder.pos_estimate + posvoulu
        else:
            time.sleep(0.2)
            posvoulu=self.calcul_angle(self.goal.distmm)
            print(self.goal.distmm)
            posArriver = my_drive.axis0.encoder.pos_estimate + posvoulu
            my_drive.axis1.controller.input_pos = my_drive.axis1.encoder.pos_estimate + posvoulu
            my_drive.axis0.controller.input_pos = my_drive.axis0.encoder.pos_estimate + posvoulu


        while (my_drive.axis1.encoder.vel_estimate <= 0.1 and my_drive.axis0.encoder.vel_estimate <= 0.1):
            self.get_logger().info('attente de demarrage')
            time.sleep(0.2)
            print(my_drive.axis1.encoder.vel_estimate)
            print(my_drive.axis0.encoder.vel_estimate)


        self.get_logger().info('partie')

        while (my_drive.axis1.encoder.vel_estimate != 0 and my_drive.axis0.encoder.vel_estimate != 0) or self.stop or redemarage:
            if self.stop and self.goal.aout=="Avancer":
                my_drive.axis1.controller.input_pos = my_drive.axis1.encoder.pos_estimate
                my_drive.axis0.controller.input_pos = my_drive.axis0.encoder.pos_estimate
                redemarage=True
            elif redemarage:
                self.get_logger().info('redemarrage asked')
                redemarage = self.demarrage(posArriver,posmArriver)
            else:
                feedback_msg.distr=posArriver-my_drive.axis0.encoder.pos_estimate
                self.get_logger().info('feedback {0}'.format(feedback_msg.distr))
                goal_handle.publish_feedback(feedback_msg)
            time.sleep(0.2)

        goal_handle.succeed()
        result = Omoteur.Result()
        result.arrive = True
        self.get_logger().info('goal succeed')

        return result
    
def main():
    rclpy.init()

    moteur_server= OdriveServeur()
    exut = MultiThreadedExecutor()
    rclpy.spin(moteur_server,executor=exut)

    moteur_server.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()





    
