import rclpy
from rclpy.node import Node
from interfaces.srv import Arduino


class clientest(Node):
    def __init__(self):
        super().__init__('client_test')
        self.cli = self.create_client(Arduino,'commande_arduino')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, wait')
        self.req = Arduino.Request()
        self.taskcall()

    def wait_for_request(self,tag):
        self.req.commande = tag
        fut = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self,fut)
        return fut.result()

    def no_wait_request(self,tag):
        self.req.commande = tag
        fut = self.cli.call_async(self.req)
        fut.cancel()

    def taskcall(self):
        fait = self.wait_for_request(1)
        self.get_logger().info('resultat : %d' %fait.realiser)
        fait = False
        self.no_wait_request(2)
        self.get_logger().info('resultat : %d' %fait)
        fait = self.wait_for_request(3)
        self.get_logger().info('resultat : %d' %fait.realiser)


def main():
    rclpy.init()

    mclient = clientest()
    rclpy.spin(mclient)

    mclient.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()

        
