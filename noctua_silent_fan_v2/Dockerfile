ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip pigpio

COPY pwm_fan_noctua.py /pwm_fan_noctua.py
COPY executer.sh /run.sh

RUN chmod +x /run.sh

CMD [ "/run.sh" ]
