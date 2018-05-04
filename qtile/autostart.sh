#!/usr/bin/bash
nm-applet &
xbacklight -set 40%

#windows=$(xrandr --listmonitors | wc -l)
#
#if [ ${windows} -gt 3 ]; then
#    /home/andre/.screenlayout/treescreens.sh
#elif [ ${windows} -lt 3 ]; then
#    /home/andre/.screenlayout/onescreen.sh
#fi

autorandr --change
xfce4-power-manager --restart
firefox &
spotify &
emacs &
