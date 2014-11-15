import RPi.GPIO as GPIO
import time
from Queue import Queue, Empty

_turned_on = True
_target_temperature = 54.5
_update_queue = Queue()

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

def set_target_temperature(new_temp):
  def update(): _target_temperature = new_temp
  _update_queue.put_nowait(update)

def set_turned_on(should_run):
  def update(): _turned_on = should_run
  _update_queue.put_nowait(update)

def _flush_updates():
  try:
    while True:
      update = queue.get_nowait()
      update()
  except Empty:
    pass

if __name__ == '__main__':
  gpio_setup()
  try:
    is_heating=False
    while True:
      _flush_updates()
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
