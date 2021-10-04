#!/usr/bin/env python

import random
import rospy
from std_msgs.msg import String


class MessageBusiness():

    def DataGroupGenerator(self):
        """
        Generates 4 digits data group for serial.
        """
        return str(random.randint(0, 1)) + "{:03d}".format(random.randint(0, 255)) 
        # first digit 0 or 1, others come from random library formatted as 3 digits


    def ArmMessageGenerator(self):
        """
        Generates 26 digits data for robotic arm serial message.
        """
        arm_message = "A"  # add A
        for x in range(6):
            arm_message += self.DataGroupGenerator()  # add 24 digits
        arm_message += "B"  # add B

        return arm_message
        

    def DriveMessageGenerator(self):
        """
        Generates 18 digits data for robotic arm serial message.
        """
        drive_message = "A"  # add A
        for x in range(4):
            drive_message += self.DataGroupGenerator()  # add 16 digits
        drive_message += "B"  # add B

        return drive_message


    def MessageParserReader(self, message):
        """
        Parses and reads the message came from ros topic.
        """
        x = 1
        data_list = []
        final_message = ""
        for i in range((len(message)-2)/4):  # string parsing
            data_list.append(message[x:x+4])
            x+=4
        for data in data_list:
            if data[0]=="0":  # data sign determining
                data = "-" + str(data[1:4]) 
                if int(data) < -255:
                    data = "-255"
            else:
                data = str(data[1:4])
                if int(data) > 255:
                    data = "255"

            final_message += (data + " ") # add the data to the final message

        return final_message


    def node_init(self):
        rospy.init_node('arm_serial_node')  # initializes arm_serial_node
        self.arm_serial_pub = rospy.Publisher('/serial/arm', String, queue_size=1)

        
        self.drive_serial_pub = rospy.Publisher('/serial/drive', String, queue_size=1)

        
        self.arm_data_pub = rospy.Publisher('/position/robotic_arm', String, queue_size=1)
        self.drive_data_pub = rospy.Publisher('/position/drive', String, queue_size=1)


    def arm_callback(self, data):
        self.arm_data_pub.publish(data.data)


    def drive_callback(self, data):
        self.drive_data_pub.publish(data.data)


    def __init__(self):
        self.node_init()

        rate = rospy.Rate(10) 

        while not rospy.is_shutdown():
            self.arm_serial_pub.publish(self.MessageParserReader(self.ArmMessageGenerator()))  # publishes the arm serial data
            self.drive_serial_pub.publish(self.MessageParserReader(self.DriveMessageGenerator()))  # publishes the drive serial data

            rospy.Subscriber("/serial/arm", String, self.arm_callback)
            rospy.Subscriber("/serial/drive", String, self.drive_callback)
            rate.sleep()

    
if __name__ == "__main__":
    try:
        ata_parlar = MessageBusiness()
    except rospy.ROSInterruptException:
        pass
    


