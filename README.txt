Advanced NBA Analytics for Fantasy Basketball 

This file contains summary and instructions on how to set up your environment to work with Advanced NBA Analytics for Fantasy NBA source code.


DESCRIPTION
=======================================
This readme serves as a guide for setting up and running Advanced Data Analytics for Fantasy Basketball.
This package has 3 main steps.

In the first step, "Start.ipynb" is executed to collect NBA stats data from third-party Python package, nba-api. 
Due to limits placed by nba-api, "sleep" function must be used to call the api to not return an error.
This will get all NBA players stats from NBA seasons 2010 to 2020.

In the second step, "Processing.ipynb" is executed to create the final outpat data that is will be used for visualization.
Python package SciKits is used to process nba stats data with 2 models, linear regression model and ridge regression model.
More details about what each cell does is provided in "Processing.ipynb"

In the final step, "app.py" is ran to host localserver "http://127.0.0.1:8050/" to show the dashboard.


CONFIGURING YOUR WORKSPACE
=======================================

Installation:
    1. Download and install Python from https://www.python.org/downloads/release/python-378/
        1a. Scroll down to "Files"
        1b. Choose any version depending on your Operating System. We used "Windows x86-64 executable installer"
        1c. Follow the recommended installation settings.
        1d. Verify that Python has been installed by opening "Command Prompt" and enter <python --version> without <> brackets.
        1e. It should display "Python 3.7.8"
    2. Download and install pip
        2a. Open "Command Prompt"
        2b. Enter <curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py> without <> brackets.
        2c. Enter <python get-pip.py> without <> brackets.
        2d. Verify that pip has been installed by entering <pip --version> without <> brackets.
        2e. It should display "pip xx.x.x" where x is the version of the pip installed
    3. Install pandas
        3a. Open "Command Prompt" (if not already open)
        3b. Enter <pip install pandas>
    4. Install numpy
        4a. Open "Command Prompt" (if not already open)
        4b. Enter  <pip install numpy>
    5. Install nba-api
        5a. Open "Command Prompt" (if not already open)
        5b. Enter <pip install nba-api>
    6. Install Plotly
        6a. Open "Command Prompt" (if not already open)
        6b. Enter <pip install plotly==4.12.0>
    7. Install SciKits
        7a. Open "Command Prompt" (if not already open)
        7b. Enter <pip install scikit-learn>
  
Running package:
    1. Run "Start.ipynb"
        1a. We used Visual Studio Code to run .ipynb file types. When using Visual Studio Code, a message will popup asking if you would like to install
            necessary extensions to run .ipynb file types. You may need to restart your Visual Studio Code to get the extension working after installation.
    2. When running all the cells, please note that it will take hours to finish to collect the same amount of data that we used for ours.
        2a. Due to limited rates, nba-api will error out if you call the api without sleep in between calls
    3. Run "Processing.ipynb"
        3a. This will export a csv file that includes output data used for fantasy points calculation. 
            It also includes players predictions for NBA season 2020-2021 by using 2 regression models.
    4. If you have Python along with all the correct packages installed, double click on "app.py" to start the dashboard.
        4a. You should see a message saying "Dash is running on http://127.0.0.1:8050/"
    5. On your browser of choice (we used Google Chrome), enter "127.0.0.1:8050" in the address bar.
    6. Done! You should see a dashboard that was created from data extracted and processed in "Start.ipynb" and "Processing.ipynb"

 