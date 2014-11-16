import os
import random
import json
import threading
from flask import Flask, render_template, jsonify, request
from state_control import StateControl

app = Flask(__name__)

_state_control = StateControl()

def read_state():
    ss = _state_control.read_snapshot()
    return dict(target_temperature=ss.target_temperature,
                current_temperature=ss.current_temperature,
                running=ss.is_running,
                heating=ss.is_heating)

@app.route("/")
def hello():
    return render_template('index.html', state=read_state())

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(**read_state())

@app.route("/state/running", methods=["POST"])
def set_running():
    desired_state = request.get_json(force=True)
    print "Set running to", desired_state
    _state_control.set_running(desired_state)
    return jsonify(**read_state())

@app.route("/state/target_temperature", methods=["POST"])
def set_target_temperature():
    desired_temp = request.get_json(force=True)
    _state_control.set_target_temperature(desired_temp)
    print "Set temperature to", desired_temp
    return jsonify(**read_state())

@app.before_first_request
def start_thread():
  use_dummy = json.loads(os.getenv("SV314_USE_DUMMY", "false"))
  if use_dummy:
    import dummy_control
    run_loop = dummy_control.run_loop
  else:
    import heater_control
    run_loop = heater_control.run_loop
  threading.Thread(target=run_loop, args=(_state_control,), name="sv314 heater control thread").start()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
