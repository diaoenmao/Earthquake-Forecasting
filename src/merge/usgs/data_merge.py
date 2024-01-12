import pandas as pd
import random
#This code is for when you are checking for duplicate earthquakes

# set a random seed for reproducibility
random.seed(2023)

"""
Modify the relative path to access your data. It can differ on your machine.
"""
RELATIVE_PATH = "src/merge/usgs/input/"

# 1. Load the USGS files and concatenate them
usgs_1950_1999 = pd.read_csv(RELATIVE_PATH + "USGS1950-1999.csv")
usgs_2000_2023 = pd.read_csv(RELATIVE_PATH + "USGS2000-2023.csv")

# concatenate the entire dataset
usgs = pd.concat([usgs_1950_1999, usgs_2000_2023], ignore_index=True)

# 2. Load the SAGE file
sage_path = RELATIVE_PATH + "SAGE_1973_2023.txt"
sage = pd.read_csv(sage_path, delimiter='|', skiprows=4)

# 3. Use a two-pointer approach
i, j = 0, 0
result = []

while i < len(usgs) and j < len(sage):
    usgs_time = pd.Timestamp(usgs.iloc[i]['time'])
    sage_time = pd.Timestamp(sage.iloc[j]['Time'])

    if abs((usgs_time - sage_time).total_seconds()) <= 10:
        if (abs(usgs.iloc[i]['latitude'] - sage.iloc[j]['Latitude']) <= 0.1 and
            abs(usgs.iloc[i]['longitude'] - sage.iloc[j]['Longitude']) <= 0.1 and
            abs(usgs.iloc[i]['mag'] - sage.iloc[j]['Magnitude']) <= 0.2):
            
            # Consider as the same earthquake, choose randomly
            if random.choice([True, False]):
                result.append([usgs_time, usgs.iloc[i]['mag'], usgs.iloc[i]['longitude'], usgs.iloc[i]['latitude'], usgs.iloc[i]['depth']])
            else:
                result.append([sage_time, sage.iloc[j]['Magnitude'], sage.iloc[j]['Longitude'], sage.iloc[j]['Latitude'], sage.iloc[j]['Depth']])
            
            i += 1
            j += 1
            continue
    if usgs_time < sage_time:
        result.append([usgs_time, usgs.iloc[i]['mag'], usgs.iloc[i]['longitude'], usgs.iloc[i]['latitude'], usgs.iloc[i]['depth']])
        i += 1
    else:
        result.append([sage_time, sage.iloc[j]['Magnitude'], sage.iloc[j]['Longitude'], sage.iloc[j]['Latitude'], sage.iloc[j]['Depth']])
        j += 1

# 4. Convert the result list to DataFrame and export it
result_df = pd.DataFrame(result, columns=['DateTime', 'Magnitude', 'Longitude', 'Latitude', 'Depth'])
result_df.to_csv("src/merge/usgs/USGS_SAGE_MERGED.csv", index=False)
