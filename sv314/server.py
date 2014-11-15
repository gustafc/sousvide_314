import os
import random
import json
import thread
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
    return jsonify(**read_state())

@app.route("/state/target_temperature", methods=["POST"])
def set_target_temperature():
    desired_temp = request.get_json(force=True)
    print "Set temperature to", desired_temp
    return jsonify(**read_state())

if __name__ == "__main__":
    use_dummy = json.loads(os.getenv("SV314_USE_DUMMY", "false"))
    if use_dummy:
      import dummy_control
      run_loop = dummy_control.run_loop
    else:
      import heater_control
      run_loop = heater_control.run_loop
    thread.start_new_thread(run_loop, (_state_control,))
    app.run(debug=True, host="0.0.0.0")
