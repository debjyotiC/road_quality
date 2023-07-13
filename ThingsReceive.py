import requests

url = "http://consentiuminc.online/feeds"


class ThingsReceive:
    def __init__(self, receive_key, all_data):
        status = "true" if all_data else "false"
        self.payload = {"receive_key": receive_key, "all": status}
        self._data_dict = requests.get(url, params=self.payload).json()['feeds'][0]

    @property
    def sensor_data(self):
        return self._data_dict["sensor_data"]

    @property
    def sensor_info(self):
        return self._data_dict["sensor_info"]