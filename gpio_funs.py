import RPi.GPIO as GPIO
import time

PIN=7

def gpio_setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN, GPIO.OUT)

def gpio_on():
  _gpio_switch(True)

def gpio_off():
  _gpio_switch(False)

def _gpio_switch(on):
  GPIO.output(PIN, on)


if __name__ == '__main__':
  gpio_setup()
  n=0
  while True:
    n+=1
    _gpio_switch(n % 2 == 0)
    time.sleep(1)

