import RPi.GPIO as GPIO
import time

_turned_on = True
_target_temperature = 54.5

PIN=11
filename='/mnt/1wire/28.383E84050000/temperature'

def gpio_setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN, GPIO.OUT)

def gpio_on():
  _gpio_switch(True)

def gpio_off():
  _gpio_switch(False)

def _gpio_switch(on):
  GPIO.output(PIN, on)

def read_file():
  with file(filename) as f:
      return float(f.read())

def set_temperature(new_temp):
  _target_temperature = new_temp

if __name__ == '__main__':
  gpio_setup()
  try:
    is_heating=False
    while True:
      temp = read_file()
      should_heat = _turned_on and temp < _target_temperature
      print temp, should_heat
      if should_heat and not is_heating:
        gpio_on()
        is_heating = True
      elif not should_heat and is_heating:
        gpio_off()
        is_heating = False
      time.sleep(1)
  finally: 
    GPIO.cleanup()
    
