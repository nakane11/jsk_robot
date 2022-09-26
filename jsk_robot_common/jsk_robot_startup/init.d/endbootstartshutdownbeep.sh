#!/bin/sh

SCRIPT_DIR=$0

# boot
start() {
    echo "$SCRIPT_DIR"
    echo -n "Starting sound: "
    if type aplay &> /dev/null && [ -f "/usr/share/sounds/jsk_robot_startup/start_sound.wav" ]; then
        aplay /usr/share/sounds/jsk_robot_startup/start_sound.wav
    elif type beep &> /dev/null; then
        beep -f 523.25 -l 250 -n -f 587.33 -l 250 -n -f 659.26 -l 250 -n -f 783.99 -l 500
    fi
    return 0
}
# shut down
stop() {
    echo "$SCRIPT_DIR"
    echo -n "Stopping sound: "
    if type aplay &> /dev/null && [ -f "/usr/share/sounds/jsk_robot_startup/stop_sound.wav" ]; then
        aplay /usr/share/sounds/jsk_robot_startup/stop_sound.wav
    elif type beep &> /dev/null; then
        beep -f 783.99 -l 250 -n -f 659.26 -l 250 -n -f 587.33 -l 250 -n -f 523.25 -l 500
    fi
    return 0
}
echo "$1"
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
esac
