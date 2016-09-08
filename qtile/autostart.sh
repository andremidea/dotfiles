#!/usr/bin/bash
nm-applet &
gnome-screensaver &
xbacklight -set 40%

windows=$(xrandr --listmonitors | wc -l)

if [ ${windows} -gt 3 ]; then
    /home/andre/.screenlayout/trabalho.sh
elif [ ${windows} -eq 3 ]; then
    /home/andre/.screenlayout/casa.sh
fi
