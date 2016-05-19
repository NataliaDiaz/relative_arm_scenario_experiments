#!/usr/bin/env python

import roslaunch
import rospy
import time
import os
from sensor_msgs.msg import (JointState, Image, CompressedImage)

import baxter_interface
from baxter_interface import CHECK_VERSION

sub_folder = '_'.join(time.ctime().split())
data_folder = '/home/mukhtar/git/catkin_ws/data/'+sub_folder
os.mkdir(data_folder)

recording_rate = 10
cameras_fps = 50
cameras_resolution = (320,200)

cameras = ['/cameras/head_camera/image', '/cameras/right_hand_camera/image']
def republished_name(topic): return topic+"/republished"
topics_to_record = [republished_name(topic)+"/compressed" for topic in cameras] + ['/robot/joint_states']
topics_arg = ' '.join(topics_to_record)

rospy.set_param("~image_transport", "compressed")


try:
    rospy.wait_for_service('/cameras/list', timeout=1) # test if the service is available
    _REAL_ROBOT = True
    print("You're using the robot")
    rospy.loginfo("You're using the robot")
except rospy.ROSException: # if not, it is probably cause we're using the simulator
    _REAL_ROBOT = False
    print("You're using the simulator")
    rospy.loginfo("You're using the simulator")

def set_cameras():
    if _REAL_ROBOT:
        head_cam = baxter_interface.CameraController('head_camera')
        
        right_hand_cam = baxter_interface.CameraController('right_hand_camera')
        head_cam.resolution = cameras_resolution
        head_cam.fps = cameras_fps
        right_hand_cam.resolution = cameras_resolution
        right_hand_cam.fps = cameras_fps


def main():
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    republishers = []
    for topic in cameras:
        republishers.append(launch.launch(roslaunch.core.Node('image_transport', 'republish', args="raw in:="+topic+" out:="+republished_name(topic) )))
    babbler = launch.launch(roslaunch.core.Node('ann4smc', 'atomic_babbler.py', args=('-ph' if _REAL_ROBOT else '') ))
    recorder = launch.launch(roslaunch.core.Node('ann4smc', 'record_state.py', args='-r '+str(recording_rate)+' -p '+data_folder+' -t '+topics_arg))

    while(not babbler.is_alive()): time.sleep(1)
    print('babbling has started')
    while(babbler.is_alive()): time.sleep(1)
    print('babbling has finished')

    try: 
        recorder.stop()
        for rep in republishers: rep.close()	
    except Exception: pass
    launch.stop()


if __name__ == '__main__':
    print("Initializing node... ")
    rospy.init_node('Experience_launcher')
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    print("Enabling robot... ")
    rs.enable()
    print("Running. Ctrl-c to quit")

    set_cameras()
    main()