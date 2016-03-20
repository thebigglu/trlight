from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import re
import json
import math

KEYS = (
    "1110111",
    "0010010",
    "1011101",
    "1011011",
    "0111010",
    "1101011",
    "1101111",
    "1010010",
    "1111111",
    "1111011")

def encode(numbers):
    def reduce_encode(acc, elem):
        if elem == 10:
            elem = 0
        if not KEYS[elem] in acc:
            acc.append(KEYS[elem])
        return acc

    return reduce(reduce_encode, numbers, [])

def check_working(working, code):
    if not working:
        return list(code)

    def map_check_working(first, second):
        return (first == "0" and second == "1") and "1" or first

    return map(map_check_working, working, list(code))

def append_ten(acc, elem):
    acc.append(elem)
    if (elem == 0) and (not 10 in acc):
        acc.append(10)
    return acc

def get_numbers(code, working):
    code_list = list(code)

    def check(i, elem):
        if (elem == "0") and (code_list[i] == "1"):
            return False
        if (elem == "1") and (code_list[i] == "0") and (working[i] == "1"):
            return False
        return True

    return reduce(append_ten, [KEYS.index(elem) for elem in KEYS if all(
        [check(i, y) for i, y in enumerate(list(elem))]
    )], [])

def filter_numbers(prev, cur):
    if not prev:
        return cur
    return reduce(append_ten, [c for c in cur if any([c + 1 == p for p in prev])], [])

def check_mis(numbers, code, missing, working, count):
    numbers_encoded = encode(numbers)
    code_list = list(code)

    if ("".join(working) == '0000000') and (count > 3):
        return '1111111'

    def check(i, elem):
        check_sector = all([list(n)[i] == "1" for n in list(numbers_encoded)])
        return (check_sector and code_list[i] == "0") and "1" or elem

    return "".join([check(i, elem) for i, elem in enumerate(list(missing))])

def check_mis_range(missing, working, numbers):
    def check(i, elem):
        check_sector = any([
            list(n)[i] == "1" and working[i] == "0" for n in encode(numbers)
        ])
        return check_sector and "1" or elem

    return "".join([check(i, elem) for i, elem in enumerate(list(missing))])

def check_left_mis_range(missing, working, start, finish):
    numbers = []
    start_floor = int(math.floor(start / 10))
    finish_floor = int(math.floor(finish / 10))

    while start_floor >= finish_floor:
        numbers.append(start_floor)
        start_floor -= 1

    return check_mis_range(missing, working, numbers)

def check_right_mis_range(missing, working, start, finish):
    numbers = []

    while start >= finish:
        value = int(start - (math.floor(start / 10) * 10))
        if not value in numbers:
            numbers.append(value)
        start -= 1

    return check_mis_range(missing, working, numbers)

def generate_start(left, right, count):
    def generate(acc, left_elem):
        acc.extend([(left_elem * 10 + r + count) for r in right if r < 10])
        return acc

    return [x for x in reduce(generate, [l for l in left if l < 10], []) if x > count and x < 100]

def init_state(collection):
    state = {
        "start": "",
        "prevL": "",
        "numbersL": "",
        "numbersR": "",
        "misL": "0000000",
        "misR": "0000000",
        "workL": "",
        "workR": "",
        "count": 0,
        "red": False,
        "no_solutions": False}
    return str(collection.insert_one({"state": json.dumps(state)}).inserted_id)

def clear_sequences(collection):
    return collection.delete_many({}).deleted_count

def get_state(collection, seq):
    try:
        record = collection.find_one({"_id": ObjectId(seq)})
    except InvalidId:
        return False

    if not record:
        return False
    return json.loads(record["state"])

def set_state(collection, seq, state):
    return collection.update_one(
        {"_id": ObjectId(seq)},
        {"$set": {"state": json.dumps(state)}}
    ).modified_count

def validate(request):
    request_keys = request.keys()

    if len(request_keys) != 2:
        return False
    if not "observation" in request_keys:
        return False
    if not 'sequence' in request_keys:
        return False

    observation = request["observation"]
    observation_keys = observation.keys()

    if not "color" in observation_keys:
        return False
    if not re.match("^(green)|(red)$", observation["color"]):
        return False

    if observation["color"] == "red":
        if len(observation) == 1:
            return True
        else:
            return False

    if not "numbers" in observation_keys:
        return False
    if len(observation["numbers"]) != 2:
        return False
    if not all([re.match("^[01]{7}$", x) for x in observation["numbers"]]):
        return False

    return True

def get_response(request, collection):
    if not validate(request):
        return {"status": "error", "msg": "The wrong format of request"}

    state = get_state(collection, request["sequence"])

    if not state:
        return {"status": "error", "msg": "The sequence isn't found"}

    if state["no_solutions"]:
        return {"status": "error", "msg": "No solutions found"}

    if state["red"]:
        return {"status": "error", "msg": "The red observation should be the last"}

    response = {"status": "ok", "response": {}}

    if request["observation"]["color"] == "red":
        state["red"] = True
        set_state(collection, request["sequence"], state)

        if not state["count"]:
            return {"status": "error", "msg": "There isn't enough data"}

        if not state["count"] in state["start"]:
            return {"status": "error", "msg": "No solutions found"}

        response["response"]["start"] = [state["count"]]
        response["response"]["missing"] = [
            check_left_mis_range(state["misL"], state["workL"], state["count"], 0),
            check_right_mis_range(state["misR"], state["workR"], state["count"], 0)
        ]
        return response

    left = request["observation"]["numbers"][0]
    right = request["observation"]["numbers"][1]

    if (state["prevL"] != left) or (len(state["numbersR"]) == 1 and state["numbersR"][0] == "0"):
        state["workL"] = check_working(state["workL"], left)
        state["numbersL"] = filter_numbers(state["numbersL"], get_numbers(left, state["workL"]))
        state["misL"] = check_mis(
            state["numbersL"],
            left,
            state["misL"],
            state["workL"],
            state["count"])
        state["prevL"] = left

    state["workR"] = check_working(state["workR"], right)
    state["numbersR"] = filter_numbers(state["numbersR"], get_numbers(right, state["workR"]))
    state["misR"] = check_mis(
        state["numbersR"],
        right,
        state["misR"],
        state["workR"],
        state["count"])

    current_start = generate_start(state["numbersL"], state["numbersR"], state["count"])

    if not state["start"]:
        state["start"] = current_start

    state["start"] = [x for x in state["start"] if x in current_start]

    if len(state["start"]) == 0:
        state["no_solutions"] = True
        set_state(collection, request["sequence"], state)
        return {"status": "error", "msg": "No solutions found"}

    if len(state["start"]) == 1:
        start = state["start"][0]
        finish = start - state["count"]
        state["misL"] = check_left_mis_range(state["misL"], state["workL"], start, finish)
        state["misR"] = check_left_mis_range(state["misR"], state["workR"], start, finish)

    response["response"]["start"] = state["start"]
    response["response"]["missing"] = [state["misL"], state["misR"]]

    state["count"] += 1

    set_state(collection, request["sequence"], state)

    return response

