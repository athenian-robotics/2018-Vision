#!/bin/bash

### BEGIN INIT INFO
# Provides: memes and an image pipe
# Required-Start:   
# Required-Stop:     
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: foo bar baz
# Description: foo bar baz
### END INIT INFO

v4l2-ctl --set-ctrl=brightness=30
v4l2-ctl --set-ctrl=contrast=10
v4l2-ctl --set-ctrl=white_balance_temperature=4500
v4l2-ctl --set-ctrl=saturation=85
v4l2-ctl --set-ctrl=exposure_auto=1
v4l2-ctl --set-ctrl=exposure_absolute=156
echo 200 > /sys/kernel/debug/tegra_fan/target_pwm

mkfifo /tmp/img
chmod a+wr /tmp/img

