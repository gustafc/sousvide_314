from Queue import Queue, Empty

class State(object):
  def __init__(self, target_temperature, is_running):
    self.target_temperature = target_temperature
    self.is_running = is_running

class Snapshot(object):
  def __init__(self, target_temperature, current_temperature, is_running, is_heating):
    self.target_temperature = target_temperature
    self.current_temperature = current_temperature
    self.is_running = is_running
    self.is_heating = is_heating

class StateControl(object):
  _last_snapshot = None   # Read from consumer thread
  _update_queue = Queue()   # Messages from consumer -> producer
  _snapshot_queue = Queue() # Messages from producer -> consumer

  def set_target_temperature(self, temp):
    def update(state):
      state.target_temperature = temp
    self._update_queue.put_nowait(update)

  def set_running(self, run):
    def update(state):
      state.is_running = run
    self._update_queue.put_nowait(update)

  def update(self, state):
    try:
      while True:
        update = self._update_queue.get_nowait()
        update(state)
    except Empty:
      pass

  def post_snapshot(self, snapshot):
    self._snapshot_queue.put_nowait(snapshot)

  def read_snapshot(self):
    try:
      while True:
        self._last_snapshot = self._snapshot_queue.get_nowait()
    except Empty:
      if self._last_snapshot is None:
        self._last_snapshot = self._snapshot_queue.get()
    return self._last_snapshot
