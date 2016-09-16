#!/usr/bin/env python
import sys
import rospy

import baxter_interface
from baxter_interface import Limb, Head, Gripper, RobotEnable, CHECK_VERSION
from std_msgs.msg import Empty


names = ['head_pan', 'l_gripper_l_finger_joint', 'l_gripper_r_finger_joint', 'left_e0', 'left_e1', 'left_s0', 'left_s1', 'left_w0', 'left_w1', 'left_w2', 'r_gripper_l_finger_joint', 'r_gripper_r_finger_joint', 'right_e0', 'right_e1', 'right_s0', 'right_s1', 'right_w0', 'right_w1', 'right_w2']
positions = [1.9175123711079323e-09, 3.0089229734974557e-05, 1.1656136997545379e-08, -1.5557922490972862, 1.4869254432037105, 0.2966753816741825, -0.043254170670461, 1.4459875320633593, 1.4934273103021356, -0.5197388002153112, 0.020833031933134405, 3.920833833842966e-08, 1.1897546738059388, 1.9397502577790355, -1.25925592718432, -0.9998100343641312, -0.6698868022939237, 1.029853661574463, 0.4999199143249742]

positions_dico = {names[i]:positions[i] for i in range(len(names))}

def main():
    head = Head()
    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')
    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
    lj = left.joint_names()
    rj = right.joint_names()

    left.move_to_joint_positions({joint:positions_dico[joint] for joint in lj})
    right.move_to_joint_positions({joint:positions_dico[joint] for joint in rj})
    grip_left.close()
    head.set_pan(0)


if __name__ == '__main__':
    try:
        rospy.init_node("goto_initpose")
        print("waiting for simulator ready... ")
        rospy.wait_for_message("/robot/sim/started", Empty)
        print("Enabling robot... ")
        rs = RobotEnable(CHECK_VERSION)
        rs.enable()
        print('Moving to initial pose ...')
        sys.exit( main() )
        print('Done')
    except rospy.ROSInterruptException,e :
        pass
