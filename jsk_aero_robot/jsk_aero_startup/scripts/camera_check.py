#!/usr/bin/env python

from __future__ import division

import os
import time
import collections
import fcntl
import subprocess
import traceback

import rostopic
import rospy
import diagnostic_updater
import diagnostic_msgs
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError
from sound_play.msg import SoundRequest

from jsk_tools.sanity_lib import checkUSBExist


class CameraCheck(object):

    def __init__(self, device_path=None):
        self.bridge = CvBridge()
        self.topic_names = rospy.get_param('~topic_names', [])
        self.device_type = rospy.get_param("~device_type", 'usb')
        self.device_path = rospy.get_param('~device_path', None)
        self.vendor_id = rospy.get_param('~vid', None)
        self.product_id = rospy.get_param('~pid', None)
        self.auto_restart = rospy.get_param("~auto_restart", False)
        self.duration = rospy.get_param('~duration', 5.0)
        self.init_duration = rospy.get_param('~init_duration', 10)
        self.frequency = rospy.get_param('~frequency', None)
        self.speak_enabled = rospy.get_param("~speak", True)
        self.speak_pub = rospy.Publisher(
            "/robotsound", SoundRequest, queue_size=1)

        # nodelet manager name for restarting
        self.camera_nodelet_manager_name = rospy.get_param(
            "~camera_nodelet_manager_name", None)
        if self.camera_nodelet_manager_name is not None:
            self.child_camera_nodelet_manager_name = rospy.get_param(
                "~child_camera_nodelet_manager_name",
                os.path.basename(self.camera_nodelet_manager_name))
        self.restart_camera_command = rospy.get_param(
            '~restart_camera_command', None)

        self.diagnostic_updater = diagnostic_updater.Updater()
        self.diagnostic_updater.setHardwareID(rospy.get_param("~hardware_id", 'none'))
        self.diagnostic_updater.add('connection', self.check_connection)
        self.diagnostic_updater.add('image', self.check_topic)

        self._is_subscribing = False

    def subscribe(self):
        self.subs = []
        self.topic_msg_dict = {}
        for topic_name in self.topic_names:
            self.topic_msg_dict[topic_name] = []
            msg_class, _, _ = rostopic.get_topic_class(topic_name, blocking=True)
            sub = rospy.Subscriber(topic_name, msg_class,
                                   callback=lambda msg : self.callback(topic_name, msg),
                                   queue_size=1)
            self.subs.append(sub)
        self._is_subscribing = True

    def unsubscribe(self):
        if self._is_subscribing is False:
            return
        for sub in self.subs:
            sub.unregister()
        self._is_subscribing = False

    def speak(self, speak_str):
        rospy.logerr(
            "[%s] %s", self.__class__.__name__, speak_str)
        if self.speak_enabled:
            msg = SoundRequest()
            msg.sound = SoundRequest.SAY
            msg.command = SoundRequest.PLAY_ONCE
            msg.arg = speak_str
            self.speak_pub.publish(msg)

    def callback(self, topic_name, msg):
        self.topic_msg_dict[topic_name].append(msg)

    def is_connected(self):
        if self.device_type == 'usb':
            if self.device_path is not None:
                if os.path.exists(self.device_path):
                    connected = True
                else:
                    connected = False
            elif (self.vendor_id is not None) and (self.product_id is not None):
                if checkUSBExist(self.vendor_id, self.product_id):
                    connected = True
                else:
                    connected = False
        else:
            raise NotImplementedError("device_type {} is not yet supported".
                                      format(self.device_type))
        return connected

    def check_connection(self, stat):
        if self.device_type == 'usb':
            if self.device_path is not None:
                if os.path.exists(self.device_path):
                    stat.summary(diagnostic_msgs.msg.DiagnosticStatus.OK,
                                 'device exists : {}'.format(self.device_path))
                else:
                    stat.summary(diagnostic_msgs.msg.DiagnosticStatus.ERROR,
                                 'device not exists : {}'.format(self.device_path))
            elif (self.vendor_id is not None) and (self.product_id is not None):
                rospy.loginfo('Device checking {}'.format(checkUSBExist(self.vendor_id, self.product_id)))
                if checkUSBExist(self.vendor_id, self.product_id):
                    stat.summary(diagnostic_msgs.msg.DiagnosticStatus.OK,
                                 'device exists : {}:{}'.format(
                                     self.vendor_id, self.product_id))
                else:
                    stat.summary(diagnostic_msgs.msg.DiagnosticStatus.ERROR,
                                 'device not exists : {}:{}'.format(
                                     self.vendor_id, self.product_id))
        else:
            raise NotImplementedError("device_type {} is not yet supported".
                                      format(self.device_type))
        return stat

    def reset_usb(self):
        if self.device_path is None:
            rospy.logwarn('device_path is not exists. '
                          'Please set device_path')
            return False
        fd = os.open(self.device_path, os.O_WROMLY)
        if fd < 0:
            rospy.logerr("Could not open {}".format(self.device_path))
            return False
        rospy.loginfo("Resetting USB device")
        # Equivalent of the _IO('U', 20) constant in the linux kernel.
        USBDEVFS_RESET = ord('U') << (4*2) | 20
        try:
            rc = fcntl.ioctl(fd, USBDEVFS_RESET, 0)
        finally:
            os.cloose(fd)

    def check_topic(self, stat):
        for topic_name in self.topic_msg_dict.keys():
            msgs = self.topic_msg_dict[topic_name]
            if len(msgs) == 0:
                stat.summary(diagnostic_msgs.msg.DiagnosticStatus.ERROR,
                             'topic {} not available'.format(topic_name))
            else:
                if self.frequency == None:
                    stat.summary(diagnostic_msgs.msg.DiagnosticStatus.OK,
                                 'topic {} available'.format(topic_name))
                else:
                    topic_hz = len(msgs) / self.duration
                    if topic_hz >= self.frequency:
                        stat.summary(diagnostic_msgs.msg.DiagnosticStatus.OK,
                                     'topic {} available'.format(topic_name))
                    else:
                        stat.summary(diagnostic_msgs.msg.DiagnosticStatus.ERROR,
                                     'topic {} available'.format(topic_name))
                    stat.add('topic {} {} Hz'.format(topic_name, topic_hz))
        return stat

    def is_topic_received(self):
        received = True
        for topic_name in self.topic_msg_dict.keys():
            msgs = self.topic_msg_dict[topic_name]
            if len(msgs) == 0:
                received = False
                break
        return received

    def is_image_valid(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            sum_of_pixels = max(cv2.sumElems(cv_image))
        except CvBridgeError as e:
            rospy.logerr(
                "[%s] failed to convert image to cv",
                self.__class__.__name__)
            return False
        rospy.loginfo(
            "[%s] sum of pixels is %d at %s",
            self.__class__.__name__,
            sum_of_pixels, msg.header.stamp.secs)
        if sum_of_pixels == 0:
            return False
        return True

    def restart_camera_node(self):
        rospy.logerr("Restart camera node")
        try:
            # 1. usbreset...
            # self.speak("resetting u s b")
            # self.reset_usb()
            # time.sleep(10)
            # 2. kill nodelet manager
            if self.camera_nodelet_manager_name is not None:
                self.speak("something wrong with camera node, "
                           "I'll restart it, killing nodelet manager")
                proc = subprocess.Popen(
                    'rosnode kill %s' %
                    (self.camera_nodelet_manager_name), shell=True)
                proc.wait()
                # time.sleep(10)

                # 3. pkill
                self.speak("killing child processes")
                rospy.loginfo('kill {}'.format(self.child_camera_nodelet_manager_name))
                proc = subprocess.Popen(
                    'pkill -f %s' %
                    self.child_camera_nodelet_manager_name,
                    shell=True)
                # time.sleep(10)
                proc.wait()

            # 4 restarting
            self.speak("restarting processes")
            rospy.loginfo('restart command: {}'.format(self.restart_camera_command))
            proc = subprocess.Popen(
                self.restart_camera_command, shell=True)
            proc.wait()
            rospy.loginfo('restarted command: {}'.format(self.restart_camera_command))
        except Exception as e:
            rospy.logerr('[%s] Unable to kill kinect node, caught exception:\n%s',
                         self.__class__.__name__, traceback.format_exc())

    def wait_init(self):
        init_time = rospy.Time.now()
        rate = rospy.Rate(10)
        while not rospy.is_shutdown() \
              and (rospy.Time.now() - init_time).to_sec() > self.init_duration:
            rate.sleep()

    def run(self):
        self.wait_init()
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.subscribe()
            start_time = rospy.Time.now()
            while not rospy.is_shutdown() \
                    and (rospy.Time.now() - start_time).to_sec() < self.duration:
                rate.sleep()
                if self.is_topic_received():
                    self.unsubscribe()
            self.unsubscribe()
            if self.auto_restart \
               and self.is_connected() \
               and self.is_topic_received() is False:
                self.restart_camera_node()
            self.diagnostic_updater.update()


def main():
    rospy.init_node('camera_check')
    cc = CameraCheck()
    cc.run()
    rospy.spin()


if __name__ == '__main__':
    main()