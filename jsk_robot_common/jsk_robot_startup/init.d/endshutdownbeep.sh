#!/bin/sh

if (echo $0|grep 'K..endshutdownbeep.sh' > /dev/null); then
    if type aplay &> /dev/null && [ -f "/usr/share/sounds/jsk_robot_startup/shutdown_sound.wav" ]; then
        aplay /usr/share/sounds/jsk_robot_startup/shutdown_sound.wav
    elif type beep &> /dev/null; then
        beep -f 783.99 -l 250 -n -f 659.26 -l 250 -n -f 587.33 -l 250 -n -f 523.25 -l 500
    fi
elif (echo $0|grep 'K..endshutdownstartbootbeep.sh' > /dev/null); then
    if type aplay &> /dev/null && [ -f "/usr/share/sounds/jsk_robot_startup/reboot_sound.wav" ]; then
        aplay /usr/share/sounds/jsk_robot_startup/reboot_sound.wav
    elif type beep &> /dev/null; then
        beep -f 783.99 -l 250 -n -f 659.26 -l 250 -n -f 587.33 -l 250 -n -f 523.25 -l 500
    fi
fi
