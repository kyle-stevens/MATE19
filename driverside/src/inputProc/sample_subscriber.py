from ControlScheme import ControlScheme
import rospy
import yaml
from sensor_msgs.msg import Joy

#Calls the interpretJoyMsg method of the test ControlScheme whenever a joy message is received
def recieve (data):
    test.interpretJoyMsg(data.axes, data.buttons)
    test.sendTwistMessage()

if __name__ == "__main__":
    test = ControlScheme()
    test.parseXML()
    try:
        rospy.init_node("ControlHandler")
        rospy.Subscriber("joy", Joy, recieve)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            rate.sleep()
    except rospy.ROSInterruptException: pass