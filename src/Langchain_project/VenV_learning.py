# here is guide what Virtual environment is and how to create and use it
# A virtual environment in Python is an isolated workspace that allows you to manage dependencies for your projects separately. This means that each project can have its own set of libraries and packages, independent of other projects and the system-wide Python installation. This is particularly useful when working on multiple projects that may require different versions of the same package or when you want to avoid conflicts between dependencies.
# To create and use a virtual environment in Python, you can follow these steps:
# 1. Install Python: Make sure you have Python installed on your system. You can download it from the official Python website (https://www.python.org/).
# 2. Open a terminal or command prompt: Navigate to the directory where you want to create your project.
# 3. Create a virtual environment: You can create a virtual environment using the built-in venv module. Run the following command:
#    ```bash	

# in terminal run python -m venv env
#    ```
# 4. Activate the virtual environment: To use the virtual environment, you need to activate it. Run the following command:
#    ```bash
#    source env/bin/activate  # On macOS/Linux
#    .\env\Scripts\activate   # On Windows
#    ```
# 5. Install packages: Once the virtual environment is activated, you can install packages using pip. For example:
#    ```bash
#    pip install numpy
#    ```
# 6. Deactivate the virtual environment: When you're done working in the virtual environment, you can deactivate it by running:
#    ```bash
#    deactivate
#    ```
# 7. Reactivate the virtual environment: Whenever you want to work on your project again, navigate to the project directory and activate the virtual environment using the command from step 4.
# By using virtual environments, you can keep your project dependencies organized and avoid potential conflicts between different projects.

#Now further if we do not want to include our file in github then we can use virtual environment and for that we need to create a .gitignore file in our project directory and inside that we can add the name of the virtual environment folder like env/ or venv/ based on what name you gave while creating the virtual environment. This will ensure that the virtual environment folder is not tracked by git and will not be included in your github repository when you push your code.

#We define the requirements.txt file to keep track of all the packages and their versions that our project depends on. This file is essential for ensuring that anyone who wants to run our project can easily install the exact same dependencies, leading to a consistent development environment across different machines.
#To create a requirements.txt file, we can use the pip freeze command, which lists all the installed packages in the current environment along with their versions. We can redirect this output to a file named requirements.txt using the following command:
#pip freeze > requirements.txt
#This command will create a requirements.txt file in the current directory, containing a list of all the packages and their versions.
#To install the packages listed in the requirements.txt file on another machine or environment, we can use the pip install command with the -r option, specifying the requirements.txt file:
#pip install -r requirements.txt # this will install all the packages listed in requirements.txt
# .gitignore should be entered in the project directory to avoid pushing the virtual environment folder to github IN THE VIRTUAL ENVIRONMENT FOLDER NAME list .venv/ or env/ based on what name you gave while creating the virtual environment.

#This command will read the requirements.txt file and install all the packages listed in it, ensuring that the environment is set up with the same dependencies as the original project.
#Using a requirements.txt file is a best practice in Python development, as it helps maintain consistency and makes it easier to share projects with others.
 # now you can create a python file for exampe wheather.py and inside that you can write code to fetch the weather data from an API like openweathermap.org and then you can create a requirements.txt file using pip freeze > requirements.txt command and then you can share the requirements.txt file with others so that they can install the same packages using pip install -r requirements.txt command in their virtual environment.
# no create one more file .env and in this file you can store your API keys and other sensitive information like this
# API_KEY=your_api_key_here
# Now in your weather.py file you can use the python-dotenv package to load the environment variables from the .env file like this
# from dotenv import load_dotenv

# now back to python file where you will add the api url and fetch the data using requests package
# import os
# import requests
# from dotenv import load_dotenv
#add now load_dotenv() at the top of your python file after imports
# load_dotenv()
# api_key = os.getenv("API_KEY")	
# you can write a function as well

# def get_current_weather():
#.    print()'\nFetching current weather data...\n')
# city = input("Enter city name: ")
# request_url = https://api.openweathermap.org/data/2.5/weather?q=London&appid=your_api_key_here os.getenv("API_KEY")&q={city}&units= imperial
# response = requests.get(request_url)
# data = response.json()
# print(data)

Here’s a concise, working sequence for macOS in this folder (/Users/sunilkumar/Downloads/Python_revision):

Create venv (use python3 to avoid “command not found”):
cd /Users/sunilkumar/Downloads/Python_revision
python3 -m venv env
Activate:
source env/bin/activate
Install packages:
pip install requests python-dotenv
Freeze dependencies:
pip freeze > requirements.txt
.gitignore (to avoid committing the venv and secrets):
Add lines:
env/
venv/
.env
Deactivate when done:
deactivate
Reactivate later:
cd /Users/sunilkumar/Downloads/Python_revision && source env/bin/activate
# Now you can run your weather.py file in this virtual environment and it will have access to the requests and python-dotenv packages that you installed in this virtual environment.
#code-----HERE------
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_current_weather():
    city = input("Enter city name: ").strip()
    if not API_KEY:
        print("Missing API_KEY in .env")
        return
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_URL, params=params, timeout=10)
    data = resp.json()
    print(data)

if __name__ == "__main__":
    get_current_weather()

	API_KEY=your_api_key_here #DO NOT CMMIT THIS - GITIGNORE THIS
# .env file content should be like this API_KEY=your_api_key_here
python weather.py # to run the weather.py file in the virtual environment