import random
import json
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

def read_state():
    target = 54.5
    current = random.uniform(target - 5, target + .5)
    return dict(target_temperature=target,
                current_temperature=current,
                running=not random.randrange(2),
                heating=current <= target)

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
    app.run(debug=True, host="0.0.0.0")
