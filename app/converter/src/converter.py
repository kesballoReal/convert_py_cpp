import os
import re

def open_file(file):
    if not os.path.isfile(file):
        raise FileNotFoundError(f"File not found: {file}")
    
    with open(file, 'r') as f:
        return f.read()

def convert(file, cppfile):
    pythoncode = open_file(file)
    try:
        conversion(pythoncode, cppfile)
    except Exception as e:
        print(f"Error during conversion: {e}")

def conversion(code, cppfile):
    lines = code.splitlines()
    
    includes_written = set()
    
    with open(cppfile, 'w') as cppf:
        standard_includes = ['<iostream>', '<string>', '<vector>']
        for include in standard_includes:
            cppf.write(f'#include {include}\n')
        
        cppf.write('\n')
        cppf.write("int main() {\n")
        
        cppf.write('\n')
        
        for line in lines:
            print(f"Processing line: {line}")
            
            if line.startswith('print("') and line.endswith('")'):
                print_content = convert_prints(line)
                cppf.write(f'    std::cout << "{print_content}" << std::endl;\n')
                print(f"\nConverted print statement: {print_content}")
            elif line.startswith('print(') and line.endswith(')'):
                print_content = convert_prints_variables(line)
                cppf.write(f'    std::cout << {print_content} << std::endl;\n')
            elif '=' in line:
                if 'input(' in line:
                    cpp_input = convert_input(line)
                    cppf.write(f'{cpp_input}\n')
                    print(f"\nConverted input statement: {cpp_input}")
                else:
                    cpp_assignment = convert_assignment(line)
                    cppf.write(f'    {cpp_assignment}\n')
                    print(f"\nConverted assignment: {cpp_assignment}")
            elif not line.startswith('import') and not line.startswith('print('):
                cppf.write(f'    // {line}\n')
        
        cppf.write("    return 0;\n")
        cppf.write("}\n")

def convert_prints(current_line):
    print(f"\nDebug convert_prints input: {current_line}")
    start_idx = current_line.index('"') + 1
    end_idx = current_line.rindex('"')
    
    if start_idx < end_idx:
        print_content = current_line[start_idx:end_idx]
        print(f"\nDebug convert_prints output: {print_content}")
        return print_content
    else:
        raise ValueError(f"Invalid print format: {current_line}")

def convert_prints_variables(current_line):
    print(f"\nDebug convert_prints input: {current_line}")
    start_idx = current_line.index('(') + 1
    end_idx = current_line.rindex(')')
    
    if start_idx < end_idx:
        print_content = current_line[start_idx:end_idx]
        print(f"\nDebug convert_prints output: {print_content}")
        return print_content
    else:
        raise ValueError(f"Invalid print format: {current_line}")

def convert_assignment(line):
    print(f"\nDebug convert_assignment input: {line}")
    var_name, var_value = line.split('=', 1)
    var_name = var_name.strip()
    var_value = var_value.strip()
    
    if '"' in var_value:
        cpp_type = "std::string"
        cpp_value = f'"{var_value.strip("\"")}"'
    elif re.match(r'^\d+\.\d+$', var_value):
        cpp_type = "float"
        cpp_value = var_value
    elif var_value.lower() in ['true', 'false']:
        cpp_type = "bool"
        cpp_value = 'true' if var_value.lower() == 'true' else 'false'
    elif re.match(r'^\d+$', var_value):
        cpp_type = "int"
        cpp_value = var_value
    elif var_value.startswith('[') and var_value.endswith(']'):
        cpp_type, cpp_value = convert_list(var_value)
    else:
        raise ValueError(f"Unsupported variable type or value: {var_value}")
    
    cpp_assignment = f'{cpp_type} {var_name} = {cpp_value};'
    print(f"\nDebug convert_assignment output: {cpp_assignment}")
    return cpp_assignment

def convert_list(var_value):
    print(f"\nDebug convert_list input: {var_value}")
    elements = var_value.strip('[]').split(',')
    elements = [element.strip().strip('"') for element in elements]
    
    if all(re.match(r'^\d+$', element) for element in elements):
        cpp_type = "std::vector<int>"
        cpp_elements = ", ".join(elements)
    elif all(re.match(r'^\d+\.\d+$', element) for element in elements):
        cpp_type = "std::vector<float>"
        cpp_elements = ", ".join(elements)
    elif all(element.lower() in ['true', 'false'] for element in elements):
        cpp_type = "std::vector<bool>"
        cpp_elements = ", ".join('true' if element.lower() == 'true' else 'false' for element in elements)
    else:
        cpp_type = "std::vector<std::string>"
        cpp_elements = ', '.join(f'"{element}"' for element in elements)
    
    cpp_list = f'{cpp_type}{{{cpp_elements}}}'
    print(f"\nDebug convert_list output: {cpp_list}")
    return cpp_type, cpp_list

def convert_input(line):
    print(f"\nDebug convert_input input: {line}")
    prompt_start = line.index('(') + 1
    prompt_end = line.rindex(')')
    prompt = line[prompt_start:prompt_end].strip().strip('"')
    
    var_name = line.split('=')[0].strip()
    
    cpp_code = f'    std::string {var_name};\n'
    cpp_code += f'    std::cout << "{prompt}";\n'
    cpp_code += f'    std::getline(std::cin, {var_name});\n'
    
    print(f"\nDebug convert_input output: {cpp_code}")
    return cpp_code
