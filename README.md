# pwned-checker
';--have i been pwned?




## Project Folder

your_project/
│
├── venv/               # Virtual environment folder
├── your_script.py      # Your Selenium script
├── start.sh            # Startup script for macOS/Linux
├── start.bat           # Startup script for Windows
└── requirements.txt    # (Optional) List of dependencies




# virtual env
1. Create and Activate a Virtual Environment
In your project directory, use the following commands to set up and activate a virtual environment:

For Windows:


'''
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
'''

For macOS/Linux:


'''
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
'''

## 2. Install the Required Packages
Once the virtual environment is activated, install the necessary dependencies (selenium):

'''
pip install selenium
'''
3. Create a Startup Script (start.sh or start.bat)
You can create a script to activate the virtual environment and run the Python script automatically. Here’s how:

For macOS/Linux (Bash Script):
Create a start.sh file:

'''
#!/bin/bash
# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python your_script.py

# Deactivate the virtual environment after script finishes
deactivate
'''