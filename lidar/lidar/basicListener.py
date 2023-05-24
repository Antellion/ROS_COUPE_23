import rclpy
from rclpy.node import Node
from interfaces.msg import Lid


class ListenerLid(Node):

    def __init__(self):
        super().__init__('basicListener')
        self.subscription = self.create_subscription(
            Lid,
            'arret',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self,msg):
        self.get_logger().info('etat: "%s"' % msg.etat)

def main():
    rclpy.init()

    basicListener = ListenerLid()

    rclpy.spin(basicListener)

    basicListener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    
