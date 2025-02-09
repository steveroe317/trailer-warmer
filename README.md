This project implements a simple thermostat using a Raspberry Pi,
a temperature sensor, an IoT Relay, and a heater. It is meant to keep a small
T@B trailer from freezing during the winter. 

The project has hard-coded temperature limits.  When the measured temperature
drops to 35 degrees Fahrenheit or below, the IoT Relay powers on heating
elements (in this case incandescent lights). When the temperature rises to
38 degrees or above, the IoT Relay powers off the heating elements.

The project can be run either as a standalone app or installed as a system
service that restarts on failure or reboot.

It's prudent to winterize any trailer too, rather than relying solely on an
active system 😉

# Materials

Raspberry Pi with a working WiFi connection.
The WiFi connection is used to download the app's github repo
and required packages.

HiLetgo 
[DHT22/AM2302 temperature/humidty sensor](https://www.amazon.com/dp/B0795F19W6?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

Digital Loggers
[IoT Relay](https://www.amazon.com/dp/B00WV7GMA2?ref=ppx_yo2ov_dt_b_fed_asin_title)

Jumper wires such as
* [Chanzon Dupont Cable Line Connector Assorted Kit Set](https://www.amazon.com/dp/B09FPGT7JT?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
* [EdgeLec Breadboard Jumper Wires](https://www.amazon.com/dp/B07GD3KDG9?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

A heater which turns on when power is supplied.
One or two incandescent lights will do
if the temperature does not drop too low.

# Setup

Connect the hardware components.

DHT22 AM2302 temperature/humidity sensor
* Connect the Raspberry Pi pin 20 (GND) to the DHT22 AM2302 "-" terminal
* Connect the Raspberry Pi pin 18 (GPIO24) to the DHT22 AM2302 "out" terminal
* Connect the Raspberry Pi pin 17 (3.3V) to the DHT22 AM2302 "+" terminal

IoT Relay
* Connect the Raspberry Pi pin 30 (GND) to the IoT Relay "-" control terminal
* Connect the Raspberry Pi pin 29 (GPIO5) to the Iot Relay "+" control terminal

Plug the heater(s) into the IoT relay's "normally off" outlet.
The Raspberry Pi can be plugged into the relay's "always on" outlet.

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

Heater control can be tested by running the following code manually
in a python instance in the virtual enviroment.

```
import adafruit_dht
import board
import digitalio
heater_control = digitalio.DigitalInOut(board.D5)
heater_control.direction = digitalio.Direction.OUTPUT
heater_control.value = True
heater_control.value = False
```

The heater should turn on when the control value is set to True
and off when the control value is set to False.

Make sure to exit the python instance before running the app
so that the is not a resource conflict with the gpio pins.

# Running the App

The app runs inside a python virtual environment.
It reads temperature and humidity from the sensor
and drives heater control outputs to the IoT Relay.
The time, temperature, humidity, and heater control are logged to a file
and written to the app's standard output.

To run the app, follow these steps:

If not already active, activate the Python virtual environment.

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

If the measured temperature drops to 35 degrees Fahrenheit
or below the heater control signal will turn on

```
2025/02/09 01:50:52,36,72,HEATER_OFF
2025/02/09 01:51:53,36,72,HEATER_OFF
2025/02/09 01:52:53,35,72,HEATER_ON
2025/02/09 01:53:53,36,72,HEATER_ON
```

When the temperature rises to 38 degrees Fahrenheit or above
the heater control signal will turn off

```
2025/02/09 02:31:03,37,72,HEATER_ON
2025/02/09 02:32:03,37,71,HEATER_ON
2025/02/09 02:33:03,38,71,HEATER_OFF
2025/02/09 02:34:04,38,71,HEATER_OFF
```

# Installing the App as a Linux Service

Installing the app as a system service allows it to restart after errors
or after a reboot (such as after a power outage). Follow these steps to
install it as a system service.

Modify the repo's trailer-warmer.service file for your enviroment.

* Change the WorkingDirectory entry to the trailer-warmer repo root
* Change the ExecStart entry to env/bin/python within the repo root
* Change User entry from steveroe to the login that will run the app
* Change Group entry from steveroe to the login that will run the app

Copy the modified trailer-warmer.service file to systemctl's service
directory

```
sudo cp trailer-warmer.service /etc/systemd/system
```

Make sure the app is not already running. If is, there will be resource
conflicts with the GPIO libraries.

Start the service with this command

```
sudo systemctl start trailer-warmer.service
```

Check that the service by watching for new entries in
/var/log/trailer-warmer/thermostat.log

```
tail -f /var/log/trailer-warmer/thermostat.log
```

and/or by running

```
sudo systemctl status trailer_warmer.service
```

systemd logs for the service can be viewd by running

```
journalctl -u trailer-warmer.service -f
```

Enable the service to start at boot by running

```
sudo systemctl enable trailer-warmer.service
```

Check that the service is enabled at boot by running

```
sudo systemctl is-enabled trailer-warmer.service
```

Service startup at boot can be tested by rebooting

```
sudo systemctl reboot
```

The service can be stopped, started, restarted, enabled, or disabled with these
commands

```
sudo systemctl stop trailer-warmer.service
sudo systemctl start trailer-warmer.service
sudo systemctl restart trailer-warmer.service
sudo systemctl enable trailer-warmer.service
sudo systemctl disable trailer-warmer.service
```

# References

PiMyLife 
[DHT22 humidity sensor how-to](https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/)
article.
The external resistor in the article is not needed for the HiLetgo 
DHT22 AM2302 sensor.

Digital Loggers
[IoT Relay page](https://www.digital-loggers.com/iot2.html)

RedHat
[systemctl how-to](https://www.redhat.com/en/blog/linux-systemctl-manage-services)
article

Medium
[Linux service how-to](https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6)
article
