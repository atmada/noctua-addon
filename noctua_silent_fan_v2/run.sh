#!/usr/bin/with-contenv sh
set -e

pigpiod
sleep 2

python3 /pwm_fan_noctua.py
