import xlwings as xw
import os

# Load the Excel workbook and specify the sheet
file_path = "F:/Paper writing/Second paper draft/ETnew.xlsx"  # Replace with your file path
wb = xw.Book(file_path)
sheet = wb.sheets[0] 
ET_list = []
P_list = []

# Loop through rows AC328 to AC502, 3/11 to 8./31
for row in range(328, 502):    
    cell_value = sheet.range(f'AC{row}').value
    p_value = sheet.range(f'AJ{row}').value
    ET_list.append(cell_value)
    P_list.append(p_value)
wb.close()

# Print the list of values
print(P_list)
ET_list = [-x for x in ET_list]

BC_2list = [x if x is not None else y for x, y in zip(P_list, ET_list)]
BC_3list = [x if x is not None else y for x, y in zip(P_list, ET_list)]
BC_4list = [x if x is not None else y for x, y in zip(P_list, ET_list)]
# BC_3list = [x/3 if x is not None else y for x, y in zip(P_list, ET_list)]
# BC_4list = [x/1000 if x is not None else y/1000 for x, y in zip(P_list, ET_list)]

def format_list(list):
    formatted_list= []
    for line in list:
        if line < 0:
            formatted_value = f"{line:.15E}"  # Negative values need 17 spaces
        else:
            formatted_value = f"{line:.16E}"  # Positive values need 16 
        formatted_list.append(formatted_value)
    return formatted_list

BC_2list =  format_list(BC_2list)
BC_3list =  format_list(BC_3list)
BC_4list =  format_list(BC_4list)

# Open the file and read its content into a list of lines
file_path = 'F:/Paper writing/Second paper draft/Simulation/Cut_no_flux_DONT_TOUCH.dat'  
directory = os.path.dirname(file_path)
output_file = os.path.join(directory, "Cut_CB_2013_gen.dat")

with open(file_path, 'r') as file:
    lines0 = file.readlines()
            
# Process the lines
replacement_index = 0
j = 0
for i, line in enumerate(lines0):  # Assuming lines0 is the list of lines
    if i >= 660:  # Start processing only after line 700
        if '-j_l(Kg-s)            0.0000000000000000E+00' in line:
            # Check 9 lines before for specific conditions
            if i >= 9:
                preceding_value = lines0[i - 9].strip()
                if preceding_value == '2':
                    replacement_value = BC_2list[j]
                elif preceding_value == '3':
                    replacement_value = BC_3list[j]
                elif preceding_value == '4':
                    replacement_value = BC_4list[j]
                    j = j + 1
                else:
                    continue  # Skip if none of the conditions are met

                # Replace only the first occurrence of the target value in the line
                parts = line.split("0.0000000000000000E+00", 1)
                lines0[i] = parts[0] + replacement_value + parts[1]


# Write the modified lines back to the file
with open(output_file, 'w') as output_file:
    output_file.writelines(lines0)
print("Replacement completed.")

input_file = 'F:/Paper writing/Second paper draft/Simulation/Cut_CB_2013_gen.dat'  # Replace with your .dat file path
output_file = 'F:/Paper writing/Second paper draft/Simulation/delete4.dat'  # Replace with your desired output file path

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    lines = infile.readlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("    4"):
            i += 21  # Skip the next 21 lines
        else:
            outfile.write(lines[i])
            i += 1

print(f"Filtered data saved to {output_file}")

