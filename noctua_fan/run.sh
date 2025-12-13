#!/bin/bash

# Lancer pigpio en daemon
pigpiod

# Attendre un peu pour s'assurer que pigpio démarre
sleep 2

# Lancer le script Python en boucle
python3 /pwm_fan_noctua.py
