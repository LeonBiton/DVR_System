import requests

BASE = "http://127.0.0.1:5000/"

data = [{"mission_name": "leon", "ip": "192.168.1.2", "port": 80, "type": "math", "duration": 10},
        {"mission_name": "tod", "ip": "172.111.2.0", "port": 101, "type": "geo", "duration": 256},
        {"mission_name": "john", "ip": "36.10.2.0", "port": 50, "type": "clown", "duration": 122}]

for i in range(len(data)):
    response = requests.put(BASE + "mission/" + str(i), data[i])
    print(response.json())


input()
response = requests.get(BASE + "mission/6")
print(response.json())
response = requests.get(BASE + "mission/1")
print(response.json())
