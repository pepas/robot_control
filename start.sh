#!/bin/bash

cd /opt/scripts/tools/software/mjpg-streamer/
#resolution can be changed in mjpg-streamer.service
sudo install -m 644 ./mjpg-streamer.service /etc/systemd/system
sudo systemctl daemon-reload || true
sudo systemctl restart mjpg-streamer || true

cd /home/debian/robot_control

node server

#if code: 'ERR_STREAM_DESTROYED'->run sudo python test.py before

