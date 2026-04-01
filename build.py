import os

# Define the name of the script to build
script_name = 'your_script.py'

# Command to build the executable
command = f'pyinstaller --onefile {script_name}'

# Run the build command
os.system(command)

# Optional: Clean up the build files
os.remove(f'{script_name}.spec')
 os.system('rm -rf build dist')