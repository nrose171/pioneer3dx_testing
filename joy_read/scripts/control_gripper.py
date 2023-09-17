#!usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from p2os_msgs.msg import GripperState
from p2os_msgs.msg import GripState
from p2os_msgs.msg import LiftState
import time

gripPub = None
gripSt = None
liftSt = None

def main():
    global gripPub
    rospy.init_node('joy_reader', anonymous=False)  # Initialize a non anonymous node
    rospy.Subscriber('/joy', Joy, callback)  # Subscribe to the joy topic
    rospy.Subscriber('/gripper_state', GripperState, callback2)
    gripPub = rospy.Publisher('/gripper_control', GripperState)
    rospy.spin()  # Keep running ros node
    time.sleep(2)

# Run the data event function for receiving data from joy topic
def callback(data):
    global gripPub
    global gripSt
    # if( data.buttons[0] == 1 ):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.buttons)
    rospy.loginfo(rospy.get_caller_id() + "%s", data.axes)

    # Move the Lift up or down or stop it
    publishLift(1, int(data.axes[7]), 1.0)

    # Move the Gripper Left
    if( data.axes[2] <= 0.75 ):
        publishGrip(1, -1, False, False, True, True)
    # Move the Gripper Right
    elif( data.axes[5] <= 0.75 ):
        publishGrip(1, 1, False, False, True, True)
    # Stop Moving Gripper
    elif( data.axes[2] > 0.75 or data.axes[5] > 0.75 ):
        publishGrip(1, 0, False, False, True, True)

def callback2(data):
    global gripSt
    global liftSt
    gripSt = data.grip
    liftSt = data.lift
    rospy.loginfo(rospy.get_caller_id() + "%s", gripSt)
    rospy.loginfo(rospy.get_caller_id() + "%s", liftSt)

def publishLift(state, dir, position):
    global gripPub
    global gripSt
    grip = gripSt if gripSt is not None else GripState(2, 0, False, False, True, True)
    lift = LiftState(state, dir, position)
    gripPub.publish(grip, lift)

def publishGrip(state, dir, inner_b, outer_b, left_con, right_con):
    global gripPub
    global liftSt
    lift = liftSt if liftSt is not None else liftSt(1, 0, 1.0)
    grip = GripState(state, dir, inner_b, outer_b, left_con, right_con)
    gripPub.publish(grip, lift)

if __name__ == '__main__':
    main()