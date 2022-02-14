# aero-ros-pkg-private

## Installation
Install aero-ros-pkg on ROS workspace
```
mkdir -p ~/ros/aero/src
cd ~/ros/aero/src
git clone https://github.com/seed-solutions/aero-ros-pkg
git clone -b aero-master https://github.com/iory/jsk_robot
```

## Install Dependencies on ROS workspace
```
rosdep update
rosdep install -y -r --from-paths src --ignore-src
```

## Build and setup aero_startup
```
catkin build aero_description
catkin build jsk_aero_shop
roscd aero_description
./setup.sh jsk_aero_shop/typeJSK
catkin build jsk_aero_startup
source ~/.bashrc
```

## Bringup Aero
Connect PC to JSK_AERO network
```
ssh aerov
```
Launch files
```
roslaunch jsk_aero_private aero.launch
```

## Control from eus interface
Follow https://github.com/taichiH/jsk_robot/tree/master/jsk_aero_robot/aeroeus \
If you are JSK lab member, choose `JSK Robot Model` in `Create eusmodel`

```
roscd aeroeus
catkin build aeroeus
roseus aero-interface.l
(aero-init)
(setq *aero* *robot*)
(objects (list *robot*))
```

## Control SeedHand by angle
```
(start-pinch :rarm)
(stop-pinch :rarm)
```

## Setting spot
Spot is managed by seed-solutions spot_manager.\
Please see seed-solutions link for more information.\
https://github.com/seed-solutions/aero-ros-pkg/blob/master/aero_std/README.md

Demo spot is already registered on spot.yaml file.\
https://github.com/taichiH/jsk_robot/blob/master/jsk_aero_robot/jsk_aero_startup/rooms/610/spot.yaml

## Setup PS4 joystick controller

- Disable drivers/apps for PS3 joy

    ```bash
    sudo systemctl stop sixad.service
    sudo systemctl disable sixad.service
    sudo reboot
    ```

- Install driver for PS4 joysticks

    ```bash
    sudo pip install ds4drv
    ```

- Register the joystick driver as a startup application

    Save the file below:

    ```conf
    # /etc/systemd/system/ds4drv.service
    [Unit]
    Description=ds4drv daemon
    Requires=bluetooth.service
    After=bluetooth.service

    [Service]
    ExecStart=/usr/local/bin/ds4drv --hidraw
    Restart=on-abort

    [Install]
    WantedBy=bluetooth.target
    ```

    And then register the file as a service:

    ```bash
    sudo systemctl enable ds4drv.service
    sudo systemctl start ds4drv.service
    ```

- Pairing the joystick

    ```bash
    leus@aerov:~$ sudo bluetoothctl
    [NEW] Controller 7C:5C:F8:F8:0F:BF leus [default]
    [bluetooth]# scan on  ### Here, long press PS+SHARE buttons until the LED starts blinking quickly.
    Discovery started
    [CHG] Controller 7C:5C:F8:F8:0F:BF Discovering: yes
    [NEW] Device DB:AD:99:F0:51:B1 DB-AD-99-F0-51-B1
    [NEW] Device 73:D8:6D:DB:B6:CD 73-D8-6D-DB-B6-CD
    [CHG] Device 73:D8:6D:DB:B6:CD RSSI: -65
    [CHG] Device 73:D8:6D:DB:B6:CD Name: 73B2
    [CHG] Device 73:D8:6D:DB:B6:CD Alias: 73B2
    [NEW] Device 43:51:A9:0D:DC:6F 43-51-A9-0D-DC-6F
    [NEW] Device 94:65:2D:BF:ED:8C OnePlus 5T
    [NEW] Device 80:56:F2:6A:85:B6 80-56-F2-6A-85-B6
    [CHG] Device 80:56:F2:6A:85:B6 Name: BRAVIA
    [CHG] Device 80:56:F2:6A:85:B6 Alias: BRAVIA
    [CHG] Device 80:56:F2:6A:85:B6 UUIDs: 00001200-0000-1000-8000-00805f9b34fb
    [NEW] Device 1C:66:6D:7B:C6:0A Wireless Controller  #### <- This is the one!
    [CHG] Device DB:AD:99:F0:51:B1 RSSI: -63
    [CHG] Device 73:D8:6D:DB:B6:CD RSSI: -76
    [NEW] Device 7A:66:83:17:E5:63 7A-66-83-17-E5-63
    [NEW] Device B4:B6:76:E9:B2:D5 B4-B6-76-E9-B2-D5

    [bluetooth]# pair 1C:66:6D:7B:C6:0A  ### Here, long press PS+SHARE buttons.
    Attempting to pair with 1C:66:6D:7B:C6:0A
    [CHG] Device 1C:66:6D:7B:C6:0A Connected: yes
    [CHG] Device 1C:66:6D:7B:C6:0A Modalias: usb:v054Cp05C4d0100
    [CHG] Device 1C:66:6D:7B:C6:0A UUIDs: 00001124-0000-1000-8000-00805f9b34fb
    [CHG] Device 1C:66:6D:7B:C6:0A UUIDs: 00001200-0000-1000-8000-00805f9b34fb
    [CHG] Device 1C:66:6D:7B:C6:0A Paired: yes
    Pairing successful
    [CHG] Device 1C:66:6D:7B:C6:0A Connected: no
    ```

    (Note: If pairing fails, try the following commands)
    ```
    [bluetooth]# pair 28:C1:3C:81:1A:1D
    Attempting to pair with 28:C1:3C:81:1A:1D
    [CHG] Device 28:C1:3C:81:1A:1D Connected: yes
    Failed to pair: org.bluez.Error.AuthenticationFailed
    [CHG] Device 28:C1:3C:81:1A:1D Connected: no

    [bluetooth]# agent on
    Agent registered
    [bluetooth]# default-agent
    Default agent request successful
    [bluetooth]# power on
    Changing power on succeeded
    [bluetooth]# discoverable on
    Changing discoverable on succeeded
    [bluetooth]# pairable on
    Changing pairable on succeeded
    When asked for pincode, type '0000'
    [bluetooth]# pair 28:C1:3C:81:1A:1D
    Attempting to pair with 28:C1:3C:81:1A:1D
    [CHG] Device 28:C1:3C:81:1A:1D Connected: yes
    Request PIN code
    [agent] Enter PIN code: 0000
    [CHG] Device 28:C1:3C:81:1A:1D Paired: yes
    Pairing successful
    [CHG] Device 28:C1:3C:81:1A:1D Connected: no
    ```
    (End note)
    ```
    ## Next, trust the device, otherwise the connection will never be established.
    [bluetooth]# trust 1C:66:6D:7B:C6:0A
    [CHG] Device 1C:66:6D:7B:C6:0A Trusted: yes
    Changing 1C:66:6D:7B:C6:0A trust succeeded
    [bluetooth]# info 1C:66:6D:7B:C6:0A
    Device 1C:66:6D:7B:C6:0A
            Name: Wireless Controller
            Alias: Wireless Controller
            Class: 0x002508
            Icon: input-gaming
            Paired: yes
            Trusted: yes
            Blocked: no
            Connected: no
            LegacyPairing: no
            UUID: Human Interface Device... (00001124-0000-1000-8000-00805f9b34fb)
            UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
            Modalias: usb:v054Cp05C4d0100

    # Here, press the PS button, and you will see the LED is illuminated blue.
    [Wireless Controller]# info 1C:66:6D:7B:C6:0A
    Device 1C:66:6D:7B:C6:0A
            Name: Wireless Controller
            Alias: Wireless Controller
            Class: 0x002508
            Icon: input-gaming
            Paired: yes
            Trusted: yes
            Blocked: no
            Connected: yes   ### <== Changed from `no`
            LegacyPairing: no
            UUID: Human Interface Device... (00001124-0000-1000-8000-00805f9b34fb)
            UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
            Modalias: usb:v054Cp05C4d0100
    ```
- Write the following settings in udev rules as `73-controller.rules` and save.

```
SUBSYSTEMS=="input", KERNEL=="js[0-9]*", ATTRS{name}=="Sony Computer Entertainment Wireless Controller", SYMLINK+="sensors/ps4joy"
```

After that, reboot PC.

## Control from Joy
Control mode is divided into `ik-mode` and `basic-mode`.
Furthermore, `basic-mode` is divided into `joint-mode` and `base-mode`

In the standard, control mode is a `ik-mode`.

```
Push 1 (L-stick button): Change to a `basic-mode`

In basic-mode
Push 5 (options button): Switch to a `base-mode`
```

![ps4_controller](https://user-images.githubusercontent.com/22497720/54115852-ca9e4600-4430-11e9-82fb-06bf0c3f04b2.JPG)

![ps4_controller2](https://user-images.githubusercontent.com/22497720/54115856-cbcf7300-4430-11e9-9af1-0ed643d24059.JPG)

## IK mode
Control larm with 15 (L2 button) \\
Control rarm with 17 (R2 button) \\
Basically, solve fullbody inverse kinematics,
when you want to  keep another arm end-coords, control arm with 14 (L1 button) \\
Examples \\
Move larm forward
```
Forward 1 (L-stick) with 14 (L2 button)
```

Move larm Right
```
Rightward 2 (R-stick) with 14 (L2 button)
```

Rotate yaw
```
Push 13 or 11 with 14 (L2 button)
```

|Button|Function                        |
|:-----|:-------------------------------|
|0     |---                             |
|1     |Control Larm                    |
|2     |Control Rarm                    |
|3     |---                             |
|4     |---                             |
|5     |---                             |
|6     |Rotate Pitch -                  |
|7     |Rotate Role +                   |
|8     |Rotate Pitch +                  |
|9     |Rotate Role -                   |
|10    |Grasp                           |
|11    |Rotate Yaw +                    |
|12    |Open                            |
|13    |Rotate Yaw -                    |
|14    |---                             |
|15    |Larm prefix                     |
|16    |Keep arm prefix                 |
|17    |Rarm prefix                     |
