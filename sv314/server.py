import random
from flask import Flask, render_template, jsonify
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

@app.route("/state")
def get_state():
    return jsonify(**read_state())

if __name__ == "__main__":
    app.run(debug=True)
