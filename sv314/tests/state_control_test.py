import unittest
from sv314.state_control import StateControl, State, Snapshot

class UpdateQueueTest(unittest.TestCase):

  def setUp(self):
    self.instance = StateControl()
    self.state = State(1, False)

  def test_set_target_temperature(self):
    self.instance.set_target_temperature(42)
    self.instance.set_target_temperature(666)
    self.instance.update(self.state)
    self.assertEquals(666, self.state.target_temperature)

  def test_set_running(self):
    self.instance.set_running(False)
    self.instance.set_running(True)
    self.instance.update(self.state)
    self.assertEquals(True, self.state.is_running)

  def test_read_snapshot(self):
    self.instance.post_snapshot(Snapshot(target_temperature=12,
                                         current_temperature=34,
                                         is_running=False,
                                         is_heating=False))
    snapshot = self.instance.read_snapshot()
    self.assertEquals(12, snapshot.target_temperature)
    self.assertEquals(34, snapshot.current_temperature)
