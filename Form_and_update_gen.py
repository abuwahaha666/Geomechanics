import os
from datetime import datetime, timedelta

input_file = 'F:/Paper writing/Second paper draft/Simulation/Cut_short_DONT_TOUCH.dat'
# Example: Reading a text-based .dat file
n = 172
directory = os.path.dirname(input_file)
output_file = os.path.join(directory, "Cut_DS.dat")
with open(input_file, 'r') as file:
    lines = file.readlines()

# Extract lines 678 to 744 (zero-based index: 734 to 800)
target_lines = lines[733:800]

# Prepare duplicated lines
duplicated_lines = []
for i in range(1, n + 1):
    for line in target_lines:
        if line == target_lines[0]:
            # Split the line into the main part and the comment part
            main_part, comment = line.split('!', 1)
            components = main_part.split()
            components[0] = f"{86400 * (i+1):.16E}".rjust(25)  # Update the first number and pad to 25 spaces
            components[4] = f"{86400 * (i+2):.16E}".rjust(25)  # Update the 5th number and pad to 25 spaces
            formatted_main_part = ''.join(component.rjust(25) for component in components)

            parts = comment.strip().split()
            current_date = datetime.strptime(parts[1], "%m/%d/%Y")
            new_date = current_date + timedelta(days=i)
            parts[1] = new_date.strftime("%m/%d/%Y")
            updated_comment = ' '.join(parts)

            formatted_line = formatted_main_part + ' !' + updated_comment + '\n'
            duplicated_lines.append(formatted_line)
        else:
            duplicated_lines.append(line)  # Keep lines that don't match the format unchanged

# Insert the duplicated lines after the original block
updated_lines = lines[:800] + duplicated_lines + lines[800:]


# Write the updated content to the output file
with open(output_file, 'w') as output_file:
    output_file.writelines(updated_lines)

print(f"File processed successfully. Modified file saved to {output_file}")

# F:\Dam Simulation_Mac\07212020\ET\8_13_2021\Comprehensive simualation after water inflow investigation\DS 3 months\no loading\half vet simplified - Copy\good result backup