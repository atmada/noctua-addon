#!/usr/bin/env python3
import pigpio
import time
import json
import os
from datetime import datetime

GPIO_PIN = 18
FREQUENCY = 25000
STATE_FILE = "/data/fan_state.json"

T_MIN = 45
T_START = 50
T_MAX = 70

HYST = 4
BOOST_SPEED = 40
BOOST_TIME = 0.8
MIN_SPEED = 22


def get_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return int(f.read()) / 1000


def night_mode_limit(speed):
    hour = datetime.now().hour
    if hour >= 23 or hour < 7:
        return min(speed, 50)
    return speed


def calc_speed(temp, last_speed):
    if temp <= T_MIN - HYST:
        return 0

    if temp >= T_MAX:
        return 100

    ratio = (temp - T_START) / (T_MAX - T_START)
    speed = MIN_SPEED + ratio * (100 - MIN_SPEED)

    speed = max(0, min(100, int(speed)))

    if abs(speed - last_speed) < 5:
        return last_speed

    return speed


def apply_speed(pi, pct):
    if pct < MIN_SPEED:
        duty = 0
    else:
        duty = int(pct * 1000000 / 100)
    pi.hardware_PWM(GPIO_PIN, FREQUENCY, duty)


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"speed": 0}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(speed):
    with open(STATE_FILE, "w") as f:
        json.dump({"speed": speed}, f)


def main():
    pi = pigpio.pi()
    if not pi.connected:
        raise RuntimeError("pigpiod non disponible")

    state = load_state()
    last_speed = state["speed"]
    boosted = False

    while True:
        temp = get_temp()

        speed = calc_speed(temp, last_speed)
        speed = night_mode_limit(speed)

        if last_speed == 0 and speed > 0 and not boosted:
            apply_speed(pi, BOOST_SPEED)
            time.sleep(BOOST_TIME)
            boosted = True

        if speed != last_speed:
            apply_speed(pi, speed)
            last_speed = speed
            save_state(speed)
            print(f"{temp:.1f}°C → {speed}%")

            if speed == 0:
                boosted = False

        time.sleep(5)


if __name__ == "__main__":
    main()
