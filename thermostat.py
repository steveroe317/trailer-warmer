#!/usr/bin/env python3
"""Implements a simple thermostat on a Raspberry Pi for winter RV heating.

The thermostat measures temperature using a DHT22 AM2303 sensor and activates
a heater using a GPIO pin.

The thermostat has a low temperature threshold which activates the heater and
then deactivates the heater once a high temperature threshold is reached.

The thresholds, sampling period, and log file name are hard-coded.
"""

import adafruit_dht # type: ignore
import board # type: ignore
import datetime
import digitalio # type: ignore
import os
import time
import shutil
import sys

# Heater control limits. The heater turns on when the temperature drops below
# the "on" threshold and turns off when the temperature rises above the "off"
# threshold.
heater_on_threshold_f = 35
heater_off_threshold_f = 38

sample_period_s = 60.0

log_name = '/var/log/trailer-warmer/thermostat.log'
log_size_limit = 2_000_000_000
log_rotate_count = 4


def rotate_logs(log_name: str) -> None:
	"""Rotates log files, keeps log_rotate_count-1 old logs."""

	log_names = [f'{log_name}.{index}' for index in range(log_rotate_count)]
	log_names[0] = log_name

	for index in reversed(range(log_rotate_count - 1)):
		if os.path.isfile(log_names[index]):
			shutil.move(log_names[index], log_names[index+1])


# Set up interface for temperature sensor.
dht_device = adafruit_dht.DHT22(board.D4)

# Set up control for heater on Iot Relay.
heater_control = digitalio.DigitalInOut(board.D25)
heater_control.direction = digitalio.Direction.OUTPUT
heater_control.value = False

while True:
	try:
		# Read temperature and humidity from the sensor.  The humidity value
		# is not used for heater control, but if it is None an error is assumed
		# to have occurred.
		temperature_c = dht_device.temperature
		if temperature_c is None:
			continue
		temperature_f = temperature_c * (9 / 5) + 32
		humidity = dht_device.humidity
		if humidity is None:
			continue

		temperature_c = round(temperature_c)
		temperature_f = round(temperature_f)
		humidity = round(humidity)

		# Control the heater based on the temperature.
		# Only apply a change if the heater is not in the right state.
		if temperature_f <= heater_on_threshold_f:
			if heater_control.value != True:
				heater_control.value = True
		elif temperature_f >= heater_off_threshold_f:
			if heater_control.value != False:
				heater_control.value = False

		# Rotate log files if needed.
		if os.path.isfile(log_name):
			if os.path.getsize(log_name) > log_size_limit:
				rotate_logs(log_name)

		# Log the current sensor readings and heater state.
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y/%m/%d %H:%M:%S')
		heater_state = 'HEATER_ON' if heater_control.value else 'HEATER_OFF'
		message = f'{timestamp},{temperature_f},{humidity},{heater_state}\n'
		print(message, end='')
		with open(log_name, 'a') as f:
			f.write(message)

	except RuntimeError as err:
		print(err.args[0])

	# Wait N seconds before checking the temperature again.
	time.sleep(sample_period_s)

# If the loop terminates, exit with an error
sys.exit(1)
