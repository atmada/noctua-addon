#!/usr/bin/with-contenv bashio
set -e

# Lancement de pigpiod en mode "nodaemon" pour qu'il ne bloque pas le script
pigpiod -g
sleep 2

# Lancement de votre script Python
python3 /pwm_fan_noctua.py
