import unittest
import requests

BASE = "http://127.0.0.1:5000/"

data = [{"mission_name": "leon", "ip": "192.168.1.2", "port": 80, "type": "math", "duration": 10},
        {"mission_name": "tod", "ip": "172.111.2.0", "port": 101, "type": "geo", "duration": 256},
        {"mission_name": "john", "ip": "36.10.2.0", "port": 50, "type": "clown", "duration": 122}]

for i in range(len(data)):
    response = requests.put(BASE + "mission/" + str(i), data[i])
    print(response.json())


class TestGet(unittest.TestCase):
    def test_not_found(self):
        response = requests.get(BASE + "mission/6")
        self.assertEqual(response.status_code, 404)

    def test_found(self):
        response = requests.get(BASE + "mission/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mission_name"], "tod")
        self.assertEqual(response.json()["ip"], "172.111.2.0")
        self.assertEqual(response.json()["port"], 101)


class TestPut(unittest.TestCase):
    def test_put(self):
        requests.put(BASE + "mission/4", {"mission_name": "as", "ip": "121.222.4.4",
                                            "port": 123, "type": "new", "duration": 11})
        get = requests.get(BASE + "mission/4")
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.json()["mission_name"], "as")
        self.assertEqual(get.json()["ip"], "121.222.4.4")
        self.assertEqual(get.json()["duration"], 11)


class TestDelete(unittest.TestCase):
    def test_del_exist(self):
        requests.put(BASE + "mission/11", {"mission_name": "eleven", "ip": "122.122.2.4",
                                          "port": 124, "type": "ele", "duration": 12})
        deleted = requests.delete(BASE + "mission/11")
        response = requests.get(BASE + "mission/11")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(deleted.json()["mission_name"], "eleven")
        self.assertEqual(deleted.json()["ip"], "122.122.2.4")
        self.assertEqual(deleted.json()["duration"], 12)

    def test_del_not_exist(self):
        deleted = requests.delete(BASE + "mission/21")
        self.assertEqual(deleted.status_code, 404)


class TestPatch(unittest.TestCase):
    def test_patch_exist(self):
        response = requests.get(BASE + "mission/0")
        self.assertEqual(response.json()["duration"], 10)
        patched = requests.patch(BASE + "mission/0", {"duration": 24})
        self.assertEqual(patched.json()["duration"], 24)

    def test_patch_dont_exist(self):
        patched = requests.patch(BASE + "mission/22", {"duration": 24})
        self.assertEqual(patched.status_code, 404)


if __name__ == "__main__":
    unittest.main()
