#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose
import colorsys
import random

# this seems wrong
# from custom_msgs.msg import DetectedPersonArray 

class MarkerPublisher(Node):

    def __init__(self):
        super().__init__('marker_publisher')
        self.get_logger().info("marker publisher has been initialized")

        # publisher
        self.person_markers_pub = self.create_publisher(MarkerArray, "/person_markers", 10)
        self.pub_timer = self.create_timer(1, self.publish_person_markers_command)

        # subscriber
        self.detected_people_sub = self.create_subscription(
            # Pose + int32?, '/detected_people', self.subscribe_detected_people, 10
        )
        
        self.recent_msg = Pose + int32 ()??

        # id : color pair
        self.hashmap = {}
        self.available_colors = []
        for h in range(0, 361, 30):
            for s in [0.5, 0.8, 1.0]:
                for v in [0.5, 0.8, 1.0]:
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h/360, s, v)]
                    self.available_colors.append([r, g, b])

    def publish_person_markers_command(self):
        markers = []
        for r in range(self.recent_msg):
            marker = Marker()
            if r.id in hashmap:
                color = self.hashmap[r.id]
            else:
                color = random.choice(self.available_colors)   

            marker.pose = r.pose
            marker.color color

            markers.append(marker)

        self.person_markers_pub.publish(markers)

    def subscribe_detected_people(self, msg: "Pose + int32"):
        self.get_logger().info(msg)

        self.recent_msg = msg

def main(args=None):
    rclpy.init(args=args)
    node = MarkerPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
