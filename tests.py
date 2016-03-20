import app
import json
import unittest

class AppTestCase(unittest.TestCase):

    ROUTES = {
        "create_sequence": "/sequence/create",
        "observation_add": "/observation/add",
        "clear": "/clear"}

    def setUp(self):
        self.app = app.app.test_client()
        response = json.loads(self.app.post(self.ROUTES["create_sequence"]).data)
        self.sequence = response["response"]["sequence"]

    def tearDown(self):
        self.app.post(self.ROUTES["clear"])

    def get_observ_res(self, data):
        for item in data:
            json_data = json.dumps({"observation": item, "sequence": self.sequence})
            response = self.app.post(
                self.ROUTES["observation_add"],
                data=json_data,
                content_type="application/json").data
        return json.loads(response)

    def check_ok_observ_res(self, res, start, mis_l, mis_r):
        assert res["status"] == "ok"
        assert res["response"]["start"] == start
        assert res["response"]["missing"][0] == mis_l
        assert res["response"]["missing"][1] == mis_r

    def check_no_solutions(self, res):
        assert res["status"] == "error"
        assert res["msg"] == "No solutions found"


    def test_first_case(self):
        """ 11 | 1010000 : 0000000 """
        data = (
            {"color": "green", "numbers": ["0000010", "0010010"]},
            {"color": "green", "numbers": ["0000010", "1110111"]},
            {"color": "green", "numbers": ["0100111", "1111011"]},
            {"color": "green", "numbers": ["0100111", "1111111"]},
            {"color": "green", "numbers": ["0100111", "1010010"]},
            {"color": "green", "numbers": ["0100111", "1101111"]},
            {"color": "green", "numbers": ["0100111", "1101011"]},
            {"color": "green", "numbers": ["0100111", "0111010"]},
            {"color": "green", "numbers": ["0100111", "1011011"]},
            {"color": "green", "numbers": ["0100111", "1011101"]},
            {"color": "green", "numbers": ["0100111", "0010010"]},
            {"color": "red"})

        self.check_ok_observ_res(self.get_observ_res(data), [11], "1010000", "0000000")

    def test_second_case(self):
        """ 89 | 0000000 : 0100011 """
        data = (
            {"color": "green", "numbers": ["1111111", "1011000"]},
            {"color": "green", "numbers": ["1111111", "1011100"]},
            {"color": "green", "numbers": ["1111111", "1010000"]})

        self.check_ok_observ_res(self.get_observ_res(data), [89], "0000000", "0100011")

    def test_third_case(self):
        """ 49 | 1110111 : 1011111 """
        data = (
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0000000"]},
            {"color": "green", "numbers": ["0001000", "0100000"]},
            {"color": "green", "numbers": ["0000000", "0100000"]})

        self.check_ok_observ_res(self.get_observ_res(data), [49], "1110111", "1011111")

    def test_fourth_case(self):
        """ 49 | 0000000 : 0000000 """
        data = (
            {"color": "green", "numbers": ["0111010", "1111011"]},
            {"color": "green", "numbers": ["0111010", "1111111"]},
            {"color": "green", "numbers": ["0111010", "1010010"]},
            {"color": "green", "numbers": ["0111010", "1101111"]},
            {"color": "green", "numbers": ["0111010", "1101011"]},
            {"color": "green", "numbers": ["0111010", "0111010"]},
            {"color": "green", "numbers": ["0111010", "1011011"]},
            {"color": "green", "numbers": ["0111010", "1011101"]},
            {"color": "green", "numbers": ["0111010", "0010010"]},
            {"color": "green", "numbers": ["0111010", "1110111"]},
            {"color": "green", "numbers": ["1011011", "1111011"]})

        self.check_ok_observ_res(self.get_observ_res(data), [49], "0000000", "0000000")

    def test_fifth_case(self):
        """ 11 | 0000000 : 1111111 """
        data = (
            {"color": "green", "numbers": ["0010010", "0000000"]},
            {"color": "green", "numbers": ["0010010", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "green", "numbers": ["1110111", "0000000"]},
            {"color": "red"})

        self.check_ok_observ_res(self.get_observ_res(data), [11], "0000000", "1111111")

    def test_sixth_case(self):
        """ 29 | 1111111 : 0000000 """
        data = (
            {"color": "green", "numbers": ["0000000", "1111011"]},
            {"color": "green", "numbers": ["0000000", "1111111"]},
            {"color": "green", "numbers": ["0000000", "1010010"]},
            {"color": "green", "numbers": ["0000000", "1101111"]},
            {"color": "green", "numbers": ["0000000", "1101011"]},
            {"color": "green", "numbers": ["0000000", "0111010"]},
            {"color": "green", "numbers": ["0000000", "1011011"]},
            {"color": "green", "numbers": ["0000000", "1011101"]},
            {"color": "green", "numbers": ["0000000", "0010010"]},
            {"color": "green", "numbers": ["0000000", "1110111"]},
            {"color": "green", "numbers": ["0000000", "1111011"]},
            {"color": "green", "numbers": ["0000000", "1111111"]},
            {"color": "green", "numbers": ["0000000", "1010010"]},
            {"color": "green", "numbers": ["0000000", "1101111"]},
            {"color": "green", "numbers": ["0000000", "1101011"]},
            {"color": "green", "numbers": ["0000000", "0111010"]},
            {"color": "green", "numbers": ["0000000", "1011011"]},
            {"color": "green", "numbers": ["0000000", "1011101"]},
            {"color": "green", "numbers": ["0000000", "0010010"]},
            {"color": "green", "numbers": ["0000000", "1110111"]},
            {"color": "green", "numbers": ["0000000", "1111011"]},
            {"color": "green", "numbers": ["0000000", "1111111"]},
            {"color": "green", "numbers": ["0000000", "1010010"]},
            {"color": "green", "numbers": ["0000000", "1101111"]},
            {"color": "green", "numbers": ["0000000", "1101011"]},
            {"color": "green", "numbers": ["0000000", "0111010"]},
            {"color": "green", "numbers": ["0000000", "1011011"]},
            {"color": "green", "numbers": ["0000000", "1011101"]},
            {"color": "green", "numbers": ["0000000", "0010010"]},
            {"color": "red"})

        self.check_ok_observ_res(self.get_observ_res(data), [29], "1111111", "0000000")

    def test_seventh_case(self):
        """ 21 | 1111111 : 1111111 """
        data = (
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "green", "numbers": ["0000000", "0000000"]},
            {"color": "red"})

        self.check_ok_observ_res(self.get_observ_res(data), [21], "1111111", "1111111")

    def test_eights_case(self):
        """ 7 | 0010110 : 1000100 """
        data = (
            {"color": "green", "numbers": ["1100001", "0010010"]},
            {"color": "green", "numbers": ["1100001", "0101011"]},
            {"color": "green", "numbers": ["1100001", "0101011"]},
            {"color": "green", "numbers": ["1100001", "0111010"]},
            {"color": "green", "numbers": ["1100001", "0011011"]},
            {"color": "green", "numbers": ["1100001", "0011001"]},
            {"color": "green", "numbers": ["1100001", "0010010"]},
            {"color": "red"})

        self.check_ok_observ_res(self.get_observ_res(data), [7], "0010110", "1000100")

    def test_repeat_observation(self):
        data = (
            {"color": "green", "numbers": ["1110111", "1111111"]},
            {"color": "green", "numbers": ["1110111", "1111111"]})

        self.check_no_solutions(self.get_observ_res(data))

    def test_missing_observation(self):
        data = (
            {"color": "green", "numbers": ["1110111", "1011011"]},
            {"color": "green", "numbers": ["1110111", "0010010"]},
            {"color": "red"})

        self.check_no_solutions(self.get_observ_res(data))

    def test_inconsistent_observation(self):
        data = (
            {"color": "green", "numbers": ["1110111", "1011011"]},
            {"color": "green", "numbers": ["1111111", "1111111"]},
            {"color": "green", "numbers": ["1110111", "0010010"]},
            {"color": "red"})

        self.check_no_solutions(self.get_observ_res(data))

    def test_unknow_sequence(self):
        json_data = json.dumps({
            "observation": {"color": "green", "numbers": ["1111111", "1111111"]},
            "sequence": "wrong_sequence"})
        res = json.loads(self.app.post(
            self.ROUTES["observation_add"],
            data=json_data,
            content_type="application/json").data)

        assert res["status"] == "error"
        assert res["msg"] == "The sequence isn't found"

    def test_first_red(self):
        res = self.get_observ_res(({"color": "red"},))

        assert res["status"] == "error"
        assert res["msg"] == "There isn't enough data"

    def test_observation_after_red(self):
        data = (
            {"color": "green", "numbers": ["1110111", "1011101"]},
            {"color": "green", "numbers": ["1110111", "0010010"]},
            {"color": "red"},
            {"color": "green", "numbers": ["0000000", "0000000"]})

        res = self.get_observ_res(data)

        assert res["status"] == "error"
        assert res["msg"] == "The red observation should be the last"

    def test_wrong_format_observation(self):
        data = (
            {"1observation": {"color": "green", "numbers": ["1111111", "1111111"]},\
            "sequence": "12345"},
            {"observation": {"1color": "green", "numbers": ["1111111", "1111111"]},\
            "sequence": "12345"},
            {"observation": {"color": "yellow", "numbers": ["1111111", "1111111"]},\
            "sequence": "12345"},
            {"observation": {"color": "green", "number": ["1111111", "1111111"]},\
            "sequence": "12345"},
            {"observation": {"color": "green", "numbers": ["2111111", "1111111"]},\
            "sequence": "12345"},
            {"observation": {"color": "green", "numbers": ["1111111", "111111"]},\
            "sequence": "12345"},
            {"observation": {"color": "green", "numbers": ["1111111", "1111111"]},\
            "1sequence": "12345"})

        for item in data:
            res = json.loads(self.app.post(
                self.ROUTES["observation_add"],
                data=json.dumps(item),
                content_type="application/json").data)

            assert res["status"] == "error"
            assert res["msg"] == "The wrong format of request"

if __name__ == '__main__':
    unittest.main()

