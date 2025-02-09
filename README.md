This project implements a simple thermostat using a Raspberry Pi,
a temperature sensor, and an IoT Relay.

# Requirements

Raspberry Pi

WiFi connection

HiLetgo 
[DHT22/AM2302 temperature/humidty sensor](https://www.amazon.com/dp/B0795F19W6?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

Digital Loggers
[IoT Relay](https://www.amazon.com/dp/B00WV7GMA2?ref=ppx_yo2ov_dt_b_fed_asin_title)

Jumper wires such as
* [Chanzon Dupont Cable Line Connector Assorted Kit Set](https://www.amazon.com/dp/B09FPGT7JT?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
* [EdgeLec Breadboard Jumper Wires](https://www.amazon.com/dp/B07GD3KDG9?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

# Setup

DHT22 AM2302 temperature/humidity sensor
* Connect the Raspberry Pi pin 20 (GND) to the DHT22 AM2302 "-" terminal
* Connect the Raspberry Pi pin 18 (GPIO24) to the DHT22 AM2302 "out" terminal
* Connect the Raspberry Pi pin 17 (3.3V) to the DHT22 AM2302 "+" terminal

IoT Relay
* Connect the Raspberry Pi pin 30 (GND) to the IoT Relay "-" control terminal
* Connect the Raspberry Pi pin 29 (GPIO5) to the Iot Relay "+" control terminal

Clone the trailer-warmer repository and set up a virtual environment.

```
git clone https://github.com/steveroe317/trailer-warmer.git
cd trailer-warmer
python -m venv env
source env/bin/activate
python -m pip install adafruit-circuitpython-dht
```

Set up the log directory, replacing "username"
with the login that will run the trailer warmer app.

```
sudo mkdir /var/log/trailer-warmer
sudo chown username:username /var/log/trailer-warmer/
```
# Running the Software

If needed, activate the Python virtual environment.

```
cd trailer-warmer
source env/bin/activate
```

At the root directory of the trailer-warmer repo, run

```
./thermostat.py
```

The app will start emitting log messages like

```
2025/02/08 15:47:15,40,71,HEATER_OFF
2025/02/08 15:48:16,40,71,HEATER_OFF
2025/02/08 15:49:16,40,71,HEATER_OFF
2025/02/08 15:50:16,40,71,HEATER_OFF
```

These messages will also be appended to /var/log/trailer-warmer/thermostat.log.
If the log file grows to over 1 megabyte in size, it will be rotated
through thermostat.log.1, 2, and 3.

If the measured termerature drops to 35 degrees Fahrenheit
or below the heater control signal will turn on

```
2025/02/04 06:27:48,36,67,HEATER_OFF
2025/02/04 06:28:48,36,67,HEATER_OFF
2025/02/04 06:29:49,35,67,HEATER_ON
2025/02/04 06:30:49,35,67,HEATER_ON
```

When the temperature rises to 38 degrees Fahrenheit or above
the heater control signal will turn off

```
2025/02/04 08:27:25,37,65,HEATER_ON
2025/02/04 08:29:26,37,66,HEATER_ON
2025/02/04 08:30:26,37,65,HEATER_ON
2025/02/04 08:31:26,38,65,HEATER_OFF
2025/02/04 08:32:27,38,65,HEATER_OFF
```

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
