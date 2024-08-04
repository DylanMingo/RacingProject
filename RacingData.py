import pandas as pd
import matplotlib.pyplot as plt
import glob


# Define a function to plot each graph
def plot_graph(x, y, xlabel, ylabel, title, ax):
    for i in range(len(y)):
        ax.plot(x[i], y[i], label=f'Lap {i + 1}')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()


# Initialize lists to hold data for each lap
time_data = []
speed_data = []
rpm_data = []
gear_data = []
accel_data = []
clutch_data = []
steering_data = []

# Read each CSV file (assuming they are named 'lap1.csv', 'lap2.csv', etc.)
file_pattern = "testlap*.csv"
files = glob.glob(file_pattern)

for file in files:
    df = pd.read_csv(file)

    # Filter the data to include only points where speed > 3 mph
    df = df[df['Vehicle Speed (mph)'] > 3]

    # Adjust the time data to start from zero for each lap
    df['Time (sec)'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]

    # Replace gear position 15 with 0 (neutral)
    df['Gear Current (Gear)'] = df['Gear Current (Gear)'].replace(15, 0)

    time_data.append(df['Time (sec)'])
    speed_data.append(df['Vehicle Speed (mph)'])
    rpm_data.append(df['Engine RPM (RPM)'])
    gear_data.append(df['Gear Current (Gear)'])
    accel_data.append(df['Accel. Pedal Pos. (%)'])
    clutch_data.append(df['Clutch Pedal Pos. (%)'])
    steering_data.append(df['(TC) Steering Wheel Angle (degrees)'])

# Create subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 20))

# Plot each graph
plot_graph(time_data, speed_data, 'Time (s)', 'Speed (km/h)', 'Speed over Time', axs[0, 0])
plot_graph(time_data, rpm_data, 'Time (s)', 'Engine RPM', 'Engine RPM over Time', axs[0, 1])
plot_graph(time_data, gear_data, 'Time (s)', 'Gear', 'Gear over Time', axs[1, 0])
plot_graph(time_data, accel_data, 'Time (s)', 'Accelerator Pedal Position (%)', 'Accelerator Pedal Position over Time',
           axs[1, 1])
plot_graph(time_data, clutch_data, 'Time (s)', 'Clutch Pedal Position (%)', 'Clutch Pedal Position over Time',
           axs[2, 0])
plot_graph(time_data, steering_data, 'Time (s)', 'Steering Wheel Angle (degrees)', 'Steering Wheel Angle over Time',
           axs[2, 1])

plt.tight_layout()
plt.show()
