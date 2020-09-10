#!/bin/bash

cd /opt/scripts/tools/software/mjpg-streamer/
#resolution can be changed in mjpg-streamer.service
sudo ./install_mjpg_streamer.sh

cd /home/debian/robot_control

node server

#if code: 'ERR_STREAM_DESTROYED'->run sudo python test.py before

