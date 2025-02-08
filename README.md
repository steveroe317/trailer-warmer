This project implements a simple thermostat using a Raspberry Pi,
a temperature sensor, and an IoT Relay.

# Requirements

**Hardware**

Raspberry Pi

DHT22/AM2302 Temperature/Humidty sensor from HiLetgo
https://www.amazon.com/dp/B0795F19W6?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

IoT Relay from Digital Loggers
https://www.amazon.com/dp/B00WV7GMA2?ref=ppx_yo2ov_dt_b_fed_asin_title

Jumper wires such as
Chanzon 120pcs 10cm 20cm 30cm Long Header Jumper Wire
Dupont Cable Line Connector Assorted Kit Set
https://www.amazon.com/dp/B09FPGT7JT?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

**Software**

* WiFi connection
* git
* python3
* pip for python3 - if needed, run
`sudo apt install python3-dev python3-pip`

#Hardware Setup

DHT22 AM2302 temperature/humidity sensor
* Connect the Raspberry Pi pin 20 (GND) to the DHT22 AM2302 "-" terminal
* Connect the Raspberry Pi pin 18 (GPIO24) to the DHT22 AM2302 "out" terminal
* Connect the Raspberry Pi pin 17 (3.3V) to the DHT22 AM2302 "+" terminal


IoT Relay
* Connect the Raspberry Pi pin 30 (GND) to the IoT Relay "-" control terminal
* Connect the Raspberry Pi pin 29 (GPIO5) to the Iot Relay "+" control terminal

# Software Installation

Clone the trailer-warmer repository and set up a virtual environment.

```
git clone https://github.com/steveroe317/trailer-warmer.git
cd trailer-warmer
python -m venv env
source env/bin/activate
python -m pip install adafruit-circuitpython-dht
```

# Log Directory Setup

* sudo mkdir /var/log/trailer-warmer
* sudo chown steveroe:steveroe /var/log/trailer-warmer/

# Running the Trailer Warmer Software

# Setting up a Linux service to run the software

Change User and Group in trailer_warmer.service from steveroe to your username

sudo cp trailer-warmer.service /etc/systemd/system

sudo systemctl daemon-reload

sudo systemctl start trailer-warmer.service

sudo systemctl enable trailer-warmer.service


# Restarting the service

sudo systemctl restart trailer-warmer.service

sudo systemctl reboot

# Monitoring

sudo systemctl is-enabled trailer_warmer.service

tail -f /var/log/trailer_warmer/thermostat.log

sudo systemctl status trailer_warmer.service

journalctl -u trailer_warmer.service -f

# References

https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all#i2c-on-pi

https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6
