# To run the webpage run this command in the terminal: flask --app main run --debug



# 1. To make a flask project create a folder that your project will exist in.
# 2. Then populate that folder with a python file named main.py, the name really doesn't matter.
# 3. In the terminal run this command: py -3 -m venv .venv   This will create a virtual enviorment that your flask install will exist in.
# 4. You now need to activate the virtual environment. To do this follow the instructions bellow in order.

# "Bypass Security Windows script security then the set back to default for your safety."
# To activate the virtual environment run these commands in this order in the terminal.
# Commands:
#   get-ExecutionPolicy ; Set-ExecutionPolicy Unrestricted -Scope Process ; get-ExecutionPolicy ; .venv\Scripts\activate ; Set-ExecutionPolicy Default -Scope Process ; get-ExecutionPolicy
#

#   Set-ExecutionPolicy Unrestricted -Scope Process
#   .venv\Scripts\activate
#   Set-ExecutionPolicy Default -Scope Process
#   get-ExecutionPolicy

#5. Now install flask with the command: pip install Flask.   !make sure your terminal has (.venv) at the start of the command line.
