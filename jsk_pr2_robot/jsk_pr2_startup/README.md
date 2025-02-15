# jsk_pr2_startup

## setup

###. rewrite `/etc/ros/robot.launch`

Please rewrite `/etc/ros/robot.launch` like following:
```xml
<launch>

    <!-- Robot Description --> <param name="robot_description" textfile="/etc/ros/groovy/urdf/robot.xml" />

    <!-- Robot Analyzer --> <rosparam command="load" file="$(find pr2_bringup)/config/pr2_analyzers.yaml" ns="diag_agg" />

    <!-- Robot bringup --> 
    <include file="$(find jsk_pr2_startup)/pr2_bringup.launch" />
    <!-- <group> -->
    <!--   <remap from="/joy" to="/joy_org"/> -->
    <!--   <include file="$(find pr2_bringup)/pr2.launch" /> -->
    <!-- </group> -->

    <!-- Web ui --> <!-- include file="$(find webui)/webui.launch" /> -->

    <!-- Android app --> <include file="$(find local_app_manager)/app_manager.launch" >
      <arg name="ROBOT_NAME" value="pr1012" />
      <arg name="ROBOT_TYPE" value="pr2" />
    </include>

    <!-- RobotWebTools --> <include file="$(find rwt_image_view)/launch/rwt_image_view.launch"/>

    <!-- kinect -->
    <include file="$(find jsk_pr2_startup)/jsk_pr2_sensors/kinect_head.launch">
      <arg name="respawn" value="false" />
    </include>
    <rosparam file="/etc/ros/robot.yaml"/>
</launch> 

```

### launch mongodb for multiple users

Different users in same unix group can't run mongod against single db owned by that group.
This is because `mongod` opens database files using the `O_NOATIME` flag to the open system call.
Open with `O_NOATIME` only works if the UID completelly matchs or the caller is priviledged (`CAP_FOWNER`) for security reasons.
So if you want to launch mongodb with shared database resouces, it's better to use POSIX Capabilities in Linux.

```bash
# In Ubuntu
$ sudo aptitude install libcap2-bin
$ sudo setcap cap_fowner+ep /usr/bin/mongod
```

### Hark with Microcone

#### documentation
- Hark installation: http://www.hark.jp/wiki.cgi?page=HARK+Installation+Instructions
- hark jsk installation: https://github.com/jsk-ros-pkg/jsk_3rdparty/blob/master/hark_jsk_plugins/INSTALL
- Microcone: http://www.hark.jp/wiki.cgi?page=SupportedHardware#p10


### Bind rfcomm device

By binding rfcomm device, we can connect bluetooth device via device file (e.g. `/dev/rfcomm1`). For example, rosserial with [this PR](https://github.com/ros-drivers/rosserial/pull/569) can be used over bluetooth connection.

For detail, please see https://github.com/jsk-ros-pkg/jsk_robot/blob/master/jsk_robot_common/jsk_robot_startup/README.md#launchrfcomm_bindlaunch

#### usage

Save the bluetooth device MAC address to file like `/var/lib/robot/rfcomm_devices.yaml` in PR2.

```
- name: device1
  address: XX:XX:XX:XX:XX:XX
- name: device2
  address: YY:YY:YY:YY:YY:YY
```

Then, bind rfcomm devices.

```
# login as root user in pr2
ssh pr2
su
# Assume the bluetooth dongle is plugged into c2
roslaunch jsk_pr2_startup pr2_rfcomm_bind.launch machine:=c2
```

To check how many devices are bound to rfcomm, use rfcomm command.
```
ssh pr2
ssh c2
rfcomm
```

#### management

Currently in PR2, `pr2_rfcomm_bind.launch` is started automatically by upstart.

The upstart config file is in `/etc/upstart/jsk-rfcomm-bind.conf` in PR2.
