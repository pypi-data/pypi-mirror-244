import subprocess
import os
from vkygpt.fngen import flnm
def write_code(code,prompt):
    # Specify the file name and code content
    file_name = flnm(prompt)
    code_content = code
    vscode_path = r'C:/Program Files/Microsoft VS Code/Code.exe'
    # Create or overwrite the Python file with the specified content
    with open(file_name, 'w') as file:
        file.write(code_content)
    try:
        subprocess.run([vscode_path, file_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")