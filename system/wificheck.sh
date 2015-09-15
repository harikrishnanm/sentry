#!/bin/bash
state=`cat /sys/class/net/wlan0/operstate`

if [ "$state" == "down" ]
then
        logger -t $0 "Wifi Down!!!! Restarting"
	sudo ifdown --force wlan0
	sleep 10
        sudo ifup wlan0
else
	logger -t $0 "Wifi up"
fi
