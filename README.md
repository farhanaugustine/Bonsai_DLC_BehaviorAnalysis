# Bonsai_DLC_BehaviorAnalysis
![Presentation3](https://github.com/farhanaugustine/Bonsai_DLC_BehaviorAnalysis/assets/54376988/e4076c89-a964-44e4-b428-9acb84143d19)

# Mouse Behavior Analysis

## This Python script analyzes mouse behavior data from a CSV file. The data includes whether a mouse’s body part is in various regions of interest (ROIs) and the x and y coordinates of the body part.

# Metrics Calculated
## The script calculates the following Ten metrics for each ROI:

1. $\textcolor{yellow}{Total\ Entries\:}$ The total number of times the body part entered the ROI.
2. $\textcolor{yellow}{Total\ Exits\:}$ The total number of times the body part exited the ROI.
3. $\textcolor{yellow}{Average\ Speed\ (Pixels/Frames):}$ The average speed of the body part when it’s in the ROI, calculated as the Euclidean distance between the current position and the previous position.
4. $\textcolor{yellow}{Average\ Angle\ (Degrees)\:}$ The average angle of movement of the body part when it’s in the ROI, calculated as the angle between the vector formed by the current position and the previous position, and the positive x-axis.
     - ##### $\textcolor{green}{Note\: that\ this\ angle\ is\ measured\ counter-clockwise\ from\ the\ positive\ x-axis\,\ and\ it\ ranges\ from\ -180\ to\ +180\ degrees\.\}$ $\textcolor{green}{A\ positive\ angle\ represents\ a\ counter-clockwise\ rotation\, while\ a\ negative\ angle\ represents\ a\ clockwise\ rotation\.}$

5. $\textcolor{yellow}{Total\ Immobility\ Frames\ (>10 frames)\:}$ The total number of frames where the body part was immobile (i.e., moved less than 2 pixels) for more than 10 consecutive frames.
6. $\textcolor{yellow}{Time\ Spent\ in\ ROI\ (Frames)\:}$ The total number of frames that the body part spent in the ROI.
7. $\textcolor{yellow}{Total\ Distance\ Traveled\ (Pixels)\:}$ The total distance traveled by the body part.
8. $\textcolor{yellow}{Total\ Distance\ Traveled\ in\ ROI\ (Pixels)\:}$ The total distance traveled by the body part within the ROI.
9. $\textcolor{yellow}{Number\ of\ Direction\ Changes\:}$ The total number of times the body part changed direction.
10. $\textcolor{yellow}{Path\ Efficiency\:}$ The ratio of the straight-line distance between the start and end points of the mouse’s path to the total distance traveled by the mouse.

# Code Explanation
- The script starts by importing the necessary libraries and loading the CSV file into a pandas DataFrame:

```
import pandas as pd
import numpy as np
data = pd.read_csv(r'Path to CSV from Bonsai-rx')
```
- A DataFrame is then initialized to store the results:
```
results = pd.DataFrame()
```
- The script then defines a function to calculate the angle of movement:
```
def calculate_angle(dx, dy):
    return np.degrees(np.arctan2(dy, dx))
```
- The script then enters a loop that iterates over each ROI (from ‘Item1’ to ‘Item6’). For each ROI, it calculates the number of entries and exits, the average speed, the average angle, the total number of immobility frames, the time spent in the ROI, the total distance traveled, the total distance traveled within the ROI, the number of direction changes, and the path efficiency:

#### $\textcolor{yellow}{Change\ the\ range\ to\ match\ your\ own\ dataset/ROI\ (i.e\.\,\ Item1\ ,\ Item2\ ,\ Item3\,\ .\ .\.)}$
```
# For each ROI (In my case Item1 -to- Item6 since I have 6 ROIs).
for i in range(1, 7): # inclusive of 1 and exclusive of 7
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
```
- Finally, the results are saved to a new CSV file:
```
  # Save the results to a new CSV file
results.to_csv(r'Path for the Output CSV', index=False)
```
