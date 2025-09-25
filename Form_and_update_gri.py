import os

def modify_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process the third line
    for ii, line in enumerate(lines):
        if ii == 0:
           lines[ii] = '           0           0\n' 
        if ii >= 1 and ii <= 1491:
            line = lines[ii].strip().split()
            line[0] = f"{line[0]}".rjust(12)  # Change first number, align to 12 spaces
            line[1] = f"{line[1]}".rjust(25)
            line[2] = f"{line[2]}".rjust(25) 
            line[3] = f"{line[3]}".rjust(12)
            line[4] = f"{line[4]}".rjust(11)
            lines[ii] = " ".join(line) + "\n"
        if ii >= 1492 and ii <= 2892:
            line = lines[ii].strip().split()
            line[0] = f"{line[0]}".rjust(12)
            line = [f"{num}".rjust(11) if i > 0 else num for i, num in enumerate(line)]  # Format each element      
            lines[ii] = " ".join(line) + "\n"     
        if ii >= 2892 and ii <= 7182:
            line = lines[ii].strip().split()
            line[0] = f"{line[0]}".rjust(12)
            line = [f"{num}".rjust(24) if i > 0 else num for i, num in enumerate(line)]  # Format each element      
            lines[ii] = " ".join(line) + "\n"   
        if ii >= 7183 and ii <= 7188:
            line = lines[ii].strip().split()
            print(line)
            line[0] = f"{line[0]}".rjust(12)
            if len(line) > 0:
               line = [f"{num}".rjust(11) if i > 0 else num for i, num in enumerate(line)]  # Format each element      
            lines[ii] = " ".join(line) + "\n" 


    # Save to output file
    with open(output_file, 'w') as file:
        file.writelines(lines)

# Example usage
input_file = 'F:/Dam Simulation_Mac/07212020/ET/8_13_2021/Comprehensive simualation after water inflow investigation/DS 3 months/no loading/half vet simplified - Copy/good result backup/Cut_gri.dat'
output_file = 'F:/Paper writing/Second paper draft/Simulation/Hydraulic/Hydraulic_gri.dat'
modify_file(input_file, output_file)
