#!/user/bin/env python3
import rospy
from sensor_msgs.msg import Joy
import RPi.GPIO as rpi
import time

pinNum = 3

def main():
    rospy.init_node('joy_reader', anonymous=False)  # Initialize a non anonymous node
    rospy.Subscriber('/joy', Joy, callback)  # Subscribe to the joy topic
    rospy.spin()  # Keep running ros node

# Run the data event function for receiving data from joy topic
def callback(data):
    if( data.buttons[0] == 1 ):
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.buttons)
        print("[Calling Arduino code]")
        runTDR()
        time.sleep(20)

# Provide arduino with voltage through the Raspberry Pi GPIO pin
def runTDR():
    global pinNum
    rpi.setmode(rpi.BCM)
    rpi.setup(pinNum, rpi.OUT)
    rpi.output(pinNum, 1) #Switch to 3.3V
    time.sleep(1)
    rpi.output(pinNum, 0) #Switch to 0V


if __name__ == '__main__':
    main()