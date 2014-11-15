import time, random
from thread import start_new_thread
from state_control import StateControl, State, Snapshot

_state = State(54.5, True)

def run_loop(state_control):
  is_heating = _state.is_running
  temp = _state.target_temperature / 2
  while True:
    state_control.update(_state)
    temp += random.uniform(0, 3) * 1 if is_heating else -1
    should_heat = _state.is_running and temp < _state.target_temperature
    print temp, should_heat
    if should_heat and not is_heating:
      is_heating = True
    elif not should_heat and is_heating:
      is_heating = False
    state_control.post_snapshot(Snapshot(target_temperature=_state.target_temperature,
                                         current_temperature=temp,
                                         is_running=_state.is_running,
                                         is_heating=is_heating))
    time.sleep(5)
