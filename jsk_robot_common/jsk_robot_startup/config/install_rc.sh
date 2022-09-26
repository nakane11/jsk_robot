#!/bin/bash

jsk_robot_startup=$(builtin cd "`dirname "${BASH_SOURCE[0]}"`"/.. > /dev/null && pwd)

cd $jsk_robot_startup/init.d
for file in $(ls *.sh); do
    if [ -e /etc/init.d/$file ]; then
        file_bk=$file.$(date "+%Y%m%d_%H%M%S")
        sudo cp /etc/init.d/$file /etc/init.d/$file_bk
        echo "backup /etc/init.d/$file to /etc/init.d/$file_bk"
    fi

    sudo cp $file /etc/init.d/
    sudo chown root:root /etc/init.d/$file
    sudo chmod 755 /etc/init.d/$file
    echo "copied jsk_robot_startup/init.d/$file to /etc/init.d/$file"
done

if [ ! -d /usr/share/sounds/jsk_robot_startup ]; then
  sudo mkdir -p /usr/share/sounds/jsk_robot_startup
fi
cd $jsk_robot_startup/data
sudo cp start_sound.wav /usr/share/sounds/jsk_robot_startup/
sudo cp stop_sound.wav /usr/share/sounds/jsk_robot_startup/
# Created by VOICEVOX:四国めたん

sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc1.d/S99endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc2.d/S99endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc3.d/S99endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc4.d/S99endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc5.d/S99endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc1.d/K00endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc2.d/K00endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc3.d/K00endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc4.d/K00endbootstartshutdownbeep.sh
sudo ln -sf /etc/init.d/endbootstartshutdownbeep.sh /etc/rc5.d/K00endbootstartshutdownbeep.sh

# If you add a new script,
#   1) put it in jsk_robot_startup/init.d
#   2) make links from each runlevel in which the script is executed
