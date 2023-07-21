import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

path = "data/road-quality-2.json"
d = json.load(open(path))

x_acc = np.array(d['rot_acc_x'])
y_acc = np.array(d['rot_acc_y'])
z_acc = np.array(d['rot_acc_z'])
anomaly_time_stamps = [(data['start'], data['end']) for data in d['anomalies']]

acc_vec = np.sqrt(x_acc ** 2 + y_acc ** 2 + z_acc ** 2)


def mark_time_ranges(pl, time_ranges):
    for time_range in time_ranges:
        pl.fill_betweenx(y=[acc_vec.min(), acc_vec.max()], x1=time_range[0], x2=time_range[1], color='red', alpha=0.6)


# Create a figure and a subplot
fig, ax = plt.subplots()

plt.plot(acc_vec, label='Acc. vector', color='green')
mark_time_ranges(ax, anomaly_time_stamps)
plt.title('Acceleration vector')
plt.xlabel('Time')
plt.ylabel('Amp. m/s^2')

# Add a legend for the highlighted area
highlighted_area_patch = mpatches.Patch(facecolor='red', alpha=0.6, label='Anomalies')
plt.legend(handles=[highlighted_area_patch])

# Adjust layout and padding
plt.tight_layout()
plt.grid(True)
plt.show()
