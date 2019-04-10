import json

v = {
    1:'db',
    2:'sb',
}

s = json.dumps(v)
print(json.loads(s))

