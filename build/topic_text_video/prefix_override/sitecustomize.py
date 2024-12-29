import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/wstlxy/ROS2_Learning_copy/install/topic_text_video'
