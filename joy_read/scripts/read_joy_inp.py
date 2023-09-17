#!usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import time

def main():
    rospy.init_node('joy_reader', anonymous=False)  # Initialize a non anonymous node
    rospy.Subscriber('/joy', Joy, callback)  # Subscribe to the joy topic
    rospy.spin()  # Keep running ros node

# Run the data event function for receiving data from joy topic
def callback(data):
    # if( data.buttons[0] == 1 ):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.buttons)
    rospy.loginfo(rospy.get_caller_id() + "%s", data.axes)

if __name__ == '__main__':
    main()