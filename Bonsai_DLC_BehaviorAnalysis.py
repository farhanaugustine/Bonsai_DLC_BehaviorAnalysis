import pandas as pd
import numpy as np

# Load the CSV file
data = pd.read_csv(r'C:\Users\Farha\Downloads\Bonsai Tutorial\30FPS_Mouse 1_Control_OFT.csv')

# Initialize a DataFrame to store the results
results = pd.DataFrame()

# Function to calculate angle
def calculate_angle(dx, dy):
    return np.degrees(np.arctan2(dy, dx))

# For each ROI (Item1 to Item6)
for i in range(1, 7):
    item = f'Item{i}'

    # Calculate Entries and Exits
    data[f'{item}_prev'] = data[item].shift(fill_value=data[item].iloc[0])
    data[f'{item}_entries'] = ((data[f'{item}_prev'] == False) & (data[item] == True)).astype(int)
    data[f'{item}_exits'] = ((data[f'{item}_prev'] == True) & (data[item] == False)).astype(int)

    # Sum up the entries and exits
    total_entries = data[f'{item}_entries'].sum()
    total_exits = data[f'{item}_exits'].sum()

    # Calculate the average speed when the body part is in the ROI
    data['x_prev'] = data['Item7.X'].shift(fill_value=data['Item7.X'].iloc[0])
    data['y_prev'] = data['Item7.Y'].shift(fill_value=data['Item7.Y'].iloc[0])
    data['dx'] = data['Item7.X'] - data['x_prev']
    data['dy'] = data['Item7.Y'] - data['y_prev']
    data['speed'] = np.sqrt(data['dx']**2 + data['dy']**2)
    avg_speed = data.loc[data[item] == True, 'speed'].mean()

    # Calculate the average angle when the body part is in the ROI
    data['angle'] = calculate_angle(data['dx'], data['dy'])
    avg_angle = data.loc[data[item] == True, 'angle'].mean()

    # Calculate the total number of immobility frames
    data['immobile'] = (data['speed'] < 2).astype(int)
    data['immobile_streak'] = data['immobile'] * (data['immobile'].groupby((data['immobile'] != data['immobile'].shift()).cumsum()).cumcount() + 1)
    total_immobility_frames = (data['immobile_streak'] > 10).sum()

    # Calculate the time spent in each ROI
    time_in_roi = data[item].sum()

    # Calculate the total distance traveled
    total_distance = data['speed'].sum()

    # Calculate the total distance traveled within each ROI
    total_distance_in_roi = data.loc[data[item] == True, 'speed'].sum()

    # Calculate the number of direction changes
    data['angle_change'] = data['angle'].diff().abs()
    direction_changes = (data['angle_change'] > 0).sum()

    # Calculate the path efficiency
    straight_line_distance = np.sqrt((data['Item7.X'].iloc[-1] - data['Item7.X'].iloc[0])**2 + (data['Item7.Y'].iloc[-1] - data['Item7.Y'].iloc[0])**2)
    path_efficiency = straight_line_distance / total_distance if total_distance != 0 else 0

    # Store the results
    results = pd.concat([results, pd.DataFrame({
      'ROI': [item],
      'Total Entries': [total_entries],
      'Total Exits': [total_exits],
      'Average Speed (Pixels/Frames)': [avg_speed],
      'Average Angle (Degrees)': [avg_angle],
      'Total Immobility Frames (>10 frames)': [total_immobility_frames],
      'Time Spent in ROI (Frames)': [time_in_roi],
      'Total Distance Traveled (Pixels)': [total_distance],
      'Total Distance Traveled in ROI (Pixels)': [total_distance_in_roi],
      'Number of Direction Changes': [direction_changes],
      'Path Efficiency': [path_efficiency]
    })], ignore_index=True)

# Save the results to a new CSV file
results.to_csv(r'C:\Users\Farha\Downloads\Bonsai Tutorial\Results_Mouse 1_Control_OFT.csv', index=False)
