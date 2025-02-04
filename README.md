This project implements a simple thermostat using a Raspberry Pi,
a temperature sensor, and an IoT Relay.

# Requirements

## Hardware

Raspberry Pi

DHT22/AM2302 Temperature/Humidty sensor from HiLetgo
https://www.amazon.com/dp/B0795F19W6?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

IoT Relay from Digital Loggers
https://www.amazon.com/dp/B00WV7GMA2?ref=ppx_yo2ov_dt_b_fed_asin_title

Jumper wires such as
Chanzon 120pcs 10cm 20cm 30cm Long Header Jumper Wire
Dupont Cable Line Connector Assorted Kit Set
https://www.amazon.com/dp/B09FPGT7JT?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

## Software

python3

pip for python3 - if needed, run
`sudo apt install python3-dev python3-pip`

# Setup

md trailer-warmer

cd trailer-warmer

python3 -m venv env

source env/bin/activate

python3 -m pip install adafruit-circuitpython-dht

sudo mkdir /var/log/trailer-warmer

sudo chown steveroe:steveroe /var/log/trailer-warmer/

Change User and Group in trailer_warmer.service from steveroe to local values

sudo cp trailer_warmer.service /etc/systemd/system

sudo systemctl daemon-reload

sudo systemctl start trailer_warmer.service

# Restarting

sudo systemctl restart trailer_warmer.service

sudo systemctl reboot

# Monitoring

sudo systemctl is-enabled trailer_warmer.service

tail -f /var/log/trailer_warmer/thermostat.log

sudo systemctl status trailer_warmer.service

journalctl -u trailer_warmer.service -f

# References

https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all#i2c-on-pi

https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
