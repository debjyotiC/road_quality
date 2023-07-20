import json
import matplotlib.pyplot as plt

d = json.load(open("data/road-quality-2.json"))

x_acc = d['rot_acc_x']
y_acc = d['rot_acc_y']
z_acc = d['rot_acc_z']
anomaly_time_stamps = [(data['start'], data['end']) for data in d['anomalies']]

# Create a figure and three subplots in a 3x1 grid
fig, axes = plt.subplots(3, 1, figsize=(10, 8))

# Plot data in each subplot
axes[0].plot(x_acc, label='x-axis', color='blue')
axes[1].plot(y_acc, label='y-axis', color='green')
axes[2].plot(z_acc, label='z-axis', color='red')

# Enable grid in each subplot
axes[0].grid(True)
axes[1].grid(True)
axes[2].grid(True)


# Customize each subplot (optional)
axes[0].set_ylabel('Acc. m/s^2')
axes[1].set_ylabel('Acc. m/s^2')
axes[2].set_ylabel('Acc. m/s^2')
axes[2].set_xlabel('Time')

axes[0].set_title('Acc. x-axis')
axes[1].set_title('Acc. y-axis')
axes[2].set_title('Acc. z-axis')

# Add a legend to each subplot
axes[0].legend()
axes[1].legend()
axes[2].legend()

# Adjust layout and padding
plt.tight_layout()

# Display the plot
plt.show()
