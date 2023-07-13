from ConsentiumThings import ThingsUpdate
import time

api_key = "TKQT-OKP81PWSYYRZYBSZQ"

board = ThingsUpdate(key=api_key)

sensor_val = [1, 2, 3, 4, 5, 6, 7]
info_buff = ["a", "b", "c", "d", "e", "f", "g"]

while True:
    r = board.sendREST(sensor_val=sensor_val, info_buff=info_buff)
    print(r)
    time.sleep(5)
