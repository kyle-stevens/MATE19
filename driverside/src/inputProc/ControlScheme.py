#the indices of values from joy message:
#index number of / joy.buttons:
#0 - A
#1 - B
#2 - X
#3 - Y
#4 - LB
#5 - RB
#6 - back
#7 - start
#8 - power
#9 - Button stick left
#10 - Button stick right

#index number of / joy.axis:
#0 - Left / Right Axis stick left
#1 - Up / Down Axis stick left
#2 - LT
#3 - Left / Right Axis stick right
#4 - Up / Down Axis stick right
#5 - RT
#6 - cross key left / right
#7 - cross key up / down
from lxml import etree
import rospy
from geometry_msgs.msg import Twist


class ControlScheme:
    def __init__(self):
        # this will contain an 2D array of different control schemes where the nth control scheme will be designated from
        # axesTarget[n] and the target for the mth index axis will be axesTarget[n][m]
        self.axesTarget = []
        self.buttonsTarget = []

        # Dictionary created whenever a joy message is received that matches a target control designated by the ControlScheme
        # with a value from the joy message
        self.targetControls = {}

        # Array of all of the different ControlScheme files to be parsed
        self.XMLfileNames = ["sample_control.xml","ControlScheme.xml"]
        self.index = 0

        #rospy.init_node('ControlOutput', anonymous=True)
        self.publisher = rospy.Publisher('ControlOutput', Twist, queue_size=10)

    # Parses all of the xml files with names in the XMLfileNames array and creates an array of axes and buttons to append
    # to the axesTarget and buttonsTarget arrays respectively
    # This is done so that all of the xml files can be read in at the same time and switching between them can be done by
    # switching the index
    def parseXML(self):
        for fileName in self.XMLfileNames:
            tree = etree.parse(fileName)
            root = tree.getroot()

            axes = [None]*8
            buttons = [None]*11

            for axis in root.findall("axis"):
                axes[int(axis.get("index"))] = axis.get("target")

            for button in root.findall("button"):
                buttons[int(button.get("index"))] = button.get("target")

            self.axesTarget.append(axes)
            self.buttonsTarget.append(buttons)

    # Populates the dictionary of targetControls by matching the incoming values with the designated targets
    def interpretJoyMsg(self, axes_values, buttons_values):
        for i in range(len(axes_values)):
            if(not self.axesTarget[self.index][i] == None):
                self.targetControls[self.axesTarget[self.index][i]] = axes_values[i]

        for i in range(len(buttons_values)):
            if(not self.buttonsTarget[self.index][i] == None):
                self.targetControls[self.buttonsTarget[self.index][i]] = buttons_values[i]

    #changes the index of control schemes
    def setIndex(self, n):
        self.index = n

    def sendTwistMessage(self):
        msg = Twist()
        msg.linear.x = self.targetControls["linear_x"]
        msg.linear.y = self.targetControls["linear_y"]
        msg.linear.z = self.targetControls["linear_z"]
        msg.angular.x = self.targetControls["angular_x"]
        msg.angular.y = self.targetControls["angular_y"]
        msg.angular.z = self.targetControls["angular_z"]

        while not rospy.is_shutdown():
            self.publisher.publish(msg)
