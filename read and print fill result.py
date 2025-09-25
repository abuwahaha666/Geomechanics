import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
import pandas as pd

input_file = 'G:/My Drive/Paper submission 2024/Field test and numerical simulation/Fill/Fill_CB_2023.post.res'################################################
# Example: Reading a text-based .dat file
directory = os.path.dirname(input_file)
with open(input_file, 'r') as file:
    lines = file.readlines()  # Read all lines into a list


# Function to process the data and extract values after a specific line
def extract_xy(lines, search_line, nodes_of_interest):
    start_index = -1
    j = 1
    extracted_data_x = []
    extracted_data_y = []
    # Find the line containing "Result Displacements Isochrones 0.100000E+01"
    for i, line in enumerate(lines):
        if search_line in line:
            linepart = line.split()
            step = float(linepart[3])
            start_index = i
            # Extract data after the identified line
            for line in lines[start_index + 2:start_index + 3576]:  # Skip the header lines 5480 for wide model##########################################
                # Split each line by whitespace to extract node number and x, y values
                parts = line.split()
                if len(parts) >= 3:  # Ensure there are enough parts in the line
                    node = parts[0]
                    node = int(node)
                    x_value = parts[1]
                    x_value = float(x_value)
                    y_value = parts[2]
                    y_value = float(y_value)
                    
                    # Only keep values after nodes of interest
                    if node in nodes_of_interest:
                        print(node)
                        extracted_data_x.append((j, node, x_value))
                        extracted_data_y.append((j, node, y_value))              
            j = j + 1    
    return extracted_data_x, extracted_data_y

def extract_single(lines, search_line, nodes_of_interest):
    start_index = -1
    j = 1
    extracted_data_x = []
    # Find the line containing "Result Displacements Isochrones 0.100000E+01"
    for i, line in enumerate(lines):
        if search_line in line:
            linepart = line.split()
            step = float(linepart[3])
            if step == j:
                start_index = i
                # Extract data after the identified line
                for line in lines[start_index + 2:start_index + 3442]:  # Skip the header lines 5297 for wide model#####################################
                    # Split each line by whitespace to extract node number and x, y values
                    parts = line.split()
                    if len(parts) == 2:  # Ensure there are enough parts in the line
                        node = parts[0]
                        node = int(node)
                        x_value = parts[1]
                        x_value = float(x_value)
                        
                        # Only keep values after nodes of interest
                        if node in nodes_of_interest:
                            print(node)
                            extracted_data_x.append((j, node, x_value))                
        j = j + 1    
    return extracted_data_x
# nodes_of_interest = [3920, 3209, 2723, 2064] #for the wide model###########################################################################################
nodes_of_interest = [2440, 2108, 1590] #for the confined model
search_displacement = "Result Displacements   Isochrones"
extracted_x, extracted_y = extract_xy(lines, search_displacement, nodes_of_interest)

#%%
file_path = 'G:/My Drive/Paper submission 2024/Field test and numerical simulation/Total station and inclinometer.xlsx'################################################
df = pd.read_excel(file_path, engine='openpyxl')
subset = df.iloc[4:7, 1:7]
# Convert to a list
result_list = subset.values.tolist()
    
plt.figure(figsize=(5, 3))
# labels = ['4/29', '5/30', '7/1', '7/30', '9/2']
# times_to_plot = [50, 81, 113, 143, 171]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10.5

x = [row[0] for row in result_list]
y_columns = [[row[i] for row in result_list] for i in range(1, len(result_list[0]))]
for i, y in enumerate(y_columns):
    plt.plot(x, y, color='black', linestyle='-')

#colors = ['#6E558E', '#4F81BD', '#C0504D', '#9BBB59', '#3D97AE']
times_to_plot = [len(extracted_y)/3]
for i, time in enumerate(times_to_plot):
    # Extract data for the current time
    current_time_data = [(node, y*100) for t, node, y in extracted_y if t == time]
    nodes, y_values = zip(*current_time_data)
    y_values = y_values[::-1]
    # if i == 0:
    #     re_y_values = y_values
    # relative_y = tuple(a - b for a, b in zip(y_values, re_y_values))
    # Plot the curve
    plt.plot(x, y_values, linewidth=1.5)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Display the plot
plt.show()
















#eles_of_interest = [3592, 3565, 3542, 3532, 3512]#for the wide model#######################################################################################
eles_of_interest = [2112, 2086, 2072, 2052, 2032]#for the confined model
search_porosity = "Result Porosity        Isochrones"
search_Deg = "Result Liq_Sat_Deg     Isochrones"
extracted_fai= extract_single(lines, search_porosity, eles_of_interest)
extracted_Deg= extract_single(lines, search_Deg, eles_of_interest)

voidratio_dict = {ele: [] for ele in eles_of_interest}  # Initialize empty lists for each element
Deg_dict = {ele: [] for ele in eles_of_interest} 
wc_dict = {ele: [] for ele in eles_of_interest} 
for k, fai in enumerate(extracted_fai):
    for ele in eles_of_interest:
        if fai[1] == ele and extracted_Deg[k][1] == ele:
            e = fai[2] / (1 - fai[2])
            deg = extracted_Deg[k][2]
            wc = e*deg*100/2.70
            voidratio_dict[ele].append(e)  
            Deg_dict[ele].append(deg) 
            wc_dict[ele].append(wc)
#%%
plt.figure(figsize=(10, 3))
start_date = datetime(2014, 3, 11)
labels = ['0.5 m', '1 m', '1.3 m', '1.5 m', '2 m']
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10.5
colors = ['#4A7EBB', '#BE4B48', '#98B954', '#7D60A0', '#46AAC5']
# Iterate over the dictionary and plot each list
for ele, label, color in zip(eles_of_interest, labels, colors):
    wc = wc_dict[ele]  # Extract water content for the element
    date_range = [start_date + timedelta(days=i) for i in range(len(wc))]
    
    # Plot each void ratio list with corresponding datetime as x-axis
    plt.plot(date_range, wc, label=label, color=color)

# Moisture content
file_path = 'G:/My Drive/Paper submission 2024/Field test and numerical simulation/Moisture sensor USE THSI ONE.xlsx'  # Replace with your Excel file path
columns_to_read = list(range(8, 14))  # Columns 8 to 14 (inclusive)
rows_to_read = list(range(10155, 10851))  # Adjust for Python's 0-based indexing
data = pd.read_excel(
    file_path, 
    usecols=columns_to_read, 
    skiprows=10154, 
    nrows=10851 - 10155
)

data.columns = ['Date', '0.5 m', '1 m', '1.3 m', '1.5 m', '2 m']
markers = ['o', 's', '^', 'D', '*']  # Circle, square, triangle, diamond, star
def darken_color(hex_color, factor=0.5):
    rgb = mcolors.hex2color(hex_color)  # Convert hex to RGB (values between 0 and 1)
    darkened_rgb = tuple([max(0, c * factor) for c in rgb])  # Darken by multiplying RGB values
    return mcolors.rgb2hex(darkened_rgb)  # Convert back to hex

# Generate darker colors
darker_colors = [darken_color(color) for color in colors]
# Plot the new data on the same figure
for i, column in enumerate(['0.5 m', '1 m', '1.3 m', '1.5 m', '2 m']):
    plt.plot(data['Date'], data[column], color=darker_colors[i], marker=markers[i], markersize=3, label=column, linestyle='-')

# Add labels and title
plt.xlabel("Date")  # Label for the x-axis (can be adjusted based on your data)
plt.ylabel("Water content (%)")  # Label for the y-axis
plt.title("Moisture Content")

plt.minorticks_on()

# Add both major and minor grids
plt.grid(which='major', axis='both', linestyle='-', linewidth=0.5, color = 'black')  # Major grid lines
plt.grid(which='minor', axis='both', linestyle='--', linewidth=0.5) 
# Show legend to distinguish between different elements
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Display the plot
plt.show()
#%%
file_path = 'G:/My Drive/Paper submission 2024/Field test and numerical simulation/Total station and inclinometer.xlsx'################################################
df = pd.read_excel(file_path, engine='openpyxl')
subset = df.iloc[0:4, 1:7]
# Convert to a list
result_list = subset.values.tolist()
    
plt.figure(figsize=(5, 3))
labels = ['4/29', '5/30', '7/1', '7/30', '9/2']
times_to_plot = [50, 81, 113, 143, 171]
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10.5

x = [row[0] for row in result_list]
y_columns = [[row[i] for row in result_list] for i in range(1, len(result_list[0]))]
for i, y in enumerate(y_columns):
    plt.plot(x, y, color='black', marker=markers[i], markersize=3, label=labels[i], linestyle='-')

colors = ['#6E558E', '#4F81BD', '#C0504D', '#9BBB59', '#3D97AE']
for i, time in enumerate(times_to_plot):
    # Extract data for the current time
    current_time_data = [(node, y*100) for t, node, y in extracted_y if t == time]
    nodes, y_values = zip(*current_time_data)
    y_values = y_values[::-1]
    if i == 0:
        re_y_values = y_values
    relative_y = tuple(a - b for a, b in zip(y_values, re_y_values))
    # Plot the curve
    plt.plot(x, relative_y, marker=markers[i], linestyle='-', color=colors[i],
             label=labels[i], linewidth=1.5, markersize=3)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Display the plot
plt.show()
