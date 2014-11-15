import RPi.GPIO as GPIO
import time
from thread import start_new_thread
from state_control import StateControl, State

_state = State(54.5, True)

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

def run_loop(state_control):
  gpio_setup()
  try:
    is_heating = _state.is_running
    while True:
      state_control.update(_state)
      temp = read_file()
      should_heat = _state.is_running and temp < _state.target_temperature
      print temp, should_heat
      if should_heat and not is_heating:
        gpio_on()
        is_heating = True
      elif not should_heat and is_heating:
        gpio_off()
        is_heating = False
      state_control.post_snapshot(Snapshot(target_temperature=_state.target_temperature,
                                           current_temperature=temp,
                                           is_running=_state.is_running,
                                           is_heating=is_heating))
      time.sleep(1)
  finally:
    GPIO.cleanup()

if __name__ == '__main__':
  run_loop(StateControl())
