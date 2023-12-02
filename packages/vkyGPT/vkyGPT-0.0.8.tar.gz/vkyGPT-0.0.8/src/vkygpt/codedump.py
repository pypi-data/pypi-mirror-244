import subprocess
import os
from vkygpt.fngen import flnm
def write_code(code,prompt):
    # Specify the file name and code content
    file_name = flnm(prompt)
    code_content = code

    # Create or overwrite the Python file with the specified content
    if os.path.exists(file_name):
        with open(file_name, 'a') as file:
            file.write(code_content)
    else:
        with open(file_name, 'w') as file:
            file.write(code_content)

    # Get the full path to the Visual Studio Code executable
    vs_code_path = r'C:/Users/vijay/AppData/Local/Programs/Microsoft VS Code/Code.exe'  # Update this path

    # Open Visual Studio Code with the newly created file
    try:
        subprocess.run([vs_code_path, file_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")