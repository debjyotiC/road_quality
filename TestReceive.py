from ThingsReceive import ThingsReceive

d = ThingsReceive(receive_key="C4EUQWKMRDFBT1ZX1S14PG", all_data=False)

sensor_data = d.sensor_data
sensor_info = d.sensor_info

print(sensor_data)
print(sensor_info)
