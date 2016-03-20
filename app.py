from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from trlight import init_state, get_response, clear_sequences

app = Flask(__name__)
app.config.from_object(__name__)

def get_collection():
    return MongoClient("mongodb://db:27017").trl.seq

@app.route("/sequence/create", methods=['POST'])
def create_sequence():
    response = {"status": "ok", "response": {"sequence": init_state(get_collection())}}
    return jsonify(**response)

@app.route("/observation/add", methods=['POST'])
def observation_add():
    json = request.get_json()
    if not json:
        return abort(400)
    response = get_response(json, get_collection())
    return jsonify(**response)

@app.route("/clear", methods=["POST"])
def clear():
    clear_sequences(get_collection())
    response = {"status": "ok", "response": "ok"}
    return jsonify(**response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
