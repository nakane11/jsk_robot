#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

import actionlib
import actionlib_msgs.msg
import rospy
from sound_play.msg import SoundRequest
from sound_play.msg import SoundRequestAction
from sound_play.msg import SoundRequestGoal


if __name__ == '__main__':
    rospy.init_node("boot_sound")

    actionclient = actionlib.SimpleActionClient(
        '/robotsound_jp',
        SoundRequestAction)
    actionclient.wait_for_server()

    msg = SoundRequest()
    msg.sound = SoundRequest.SAY
    msg.command = SoundRequest.PLAY_ONCE
    msg.arg = "エアロ、起動"
    msg.volume = 1.0
    msg.arg2 = 'ja'

    goal = SoundRequestGoal()
    goal.sound_request = msg
    actionclient.send_goal(goal)
    result = actionclient.wait_for_result()
    while actionclient.get_state() == actionlib_msgs.msg.GoalStatus.ABORTED:
        actionclient.send_goal(goal)
        result = actionclient.wait_for_result()
        rospy.sleep(1.0)
