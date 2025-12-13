FROM ghcr.io/home-assistant/aarch64-base:3.19

# Installer Python + pigpio
RUN apk add --no-cache python3 py3-pip pigpio

# Copier les fichiers de l'addon
COPY run.sh /run.sh
COPY pwm_fan_noctua.py /pwm_fan_noctua.py

RUN chmod +x /run.sh


CMD [ "/run.sh" ]
