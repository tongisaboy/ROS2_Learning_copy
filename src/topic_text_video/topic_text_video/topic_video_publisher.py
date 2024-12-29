#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy                        # ROS2 Python接口库
from rclpy.node import Node         # ROS2 节点类
from sensor_msgs.msg import Image   # 图像消息类型
from cv_bridge import CvBridge      # ROS与OpenCV图像转换类
import cv2                          # Opencv图像处理库

"""
创建一个发布者节点
"""
class PublisherNode_2(Node):

    def __init__(self, name):
        super().__init__(name)                                           # ROS2节点父类初始化
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)  # 创建发布者对象（消息类型、话题名、队列长度）
        self.timer = self.create_timer(1.0/30, self.timer_callback)         # 创建一个定时器（单位为秒的周期，定时执行的回调函数）
        self.cap = cv2.VideoCapture('/path/to/your/video.mp4')            # 创建一个视频读取对象，读取本地视频文件
        self.cv_bridge = CvBridge()                                      # 创建一个图像转换对象，用于稍后将OpenCV的图像转换成ROS的图像消息

    def timer_callback(self):
        ret, frame = self.cap.read()                         # 一帧一帧读取图像
        if not ret:
            self.get_logger().warn('Video frame read failed')    # 如果图像读取失败，输出警告信息
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)            # 重置视频读取位置到开始
            ret, frame = self.cap.read()                       # 再次读取第一帧
        frame = cv2.resize(frame, (640, 480))                  # 将帧的大小调整为480p
        if ret:                                               # 如果图像读取成功
            self.publisher_.publish(
                self.cv_bridge.cv2_to_imgmsg(frame, 'bgr8'))   # 发布图像消息
            self.get_logger().info('Publishing video frame')  # 输出日志信息，提示已经完成图像话题发布
        else:
            self.get_logger().warn('Failed to publish video frame')  # 如果发布失败，输出警告信息

def main(args=None):                                 # ROS2节点主入口main函数
    rclpy.init(args=args)                            # ROS2 Python接口初始化
    node = PublisherNode_2("topic_video_publisher")        # 创建ROS2节点对象并进行初始化
    rclpy.spin(node)                                 # 循环等待ROS2退出
    node.destroy_node()                              # 销毁节点对象
    rclpy.shutdown()                                 # 关闭ROS2 Python接口