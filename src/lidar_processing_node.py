import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from custom_msgs.msg import DetectedPersonArray 
import math

class LidarProcessingNode(Node):
    def __init__(self):
        super().__init__('lidar_processing_node')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)
        self.publisher_ = self.create_publisher(DetectedPersonArray, '/detected_people', 10)

    def lidar_callback(self, msg):
        points = self.convert_lidar_data_to_points(msg)
        clusters = self.cluster_points(points)
        self.publish_detected_people(clusters)

    def convert_lidar_data_to_points(self, msg):
        points = []
        for i, range in enumerate(msg.ranges):
            if msg.range_min < range < msg.range_max:
                angle = msg.angle_min + i * msg.angle_increment
                x = range * math.cos(angle)
                y = range * math.sin(angle)
                points.append((x, y))
        return points

    def cluster_points(self, points, distance_threshold=0.5):
        clusters = []
        visited = set()
        
        def find_cluster(start_idx):
            cluster = []
            to_visit = [start_idx]
            while to_visit:
                idx = to_visit.pop()
                if idx in visited:
                    continue
                visited.add(idx)
                cluster.append(points[idx])
                for j, point in enumerate(points):
                    if j not in visited and self.distance(points[idx], point) < distance_threshold:
                        to_visit.append(j)
            return cluster

        for i in range(len(points)):
            if i not in visited:
                cluster = find_cluster(i)
                if len(cluster) > 3:
                    clusters.append(cluster)
        return clusters

    def distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def publish_detected_people(self, clusters):
        detected_people = DetectedPersonArray()
        for cluster_id, cluster in enumerate(clusters):
            person_msg = DetectedPerson()
            avg_x = sum([p[0] for p in cluster]) / len(cluster)
            avg_y = sum([p[1] for p in cluster]) / len(cluster)
            person_msg.id = cluster_id  
            person_msg.position.x = avg_x
            person_msg.position.y = avg_y
            detected_people.people.append(person_msg)
        self.publisher_.publish(detected_people)

def main(args=None):
    rclpy.init(args=args)
    node = LidarProcessingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
