# EEGWorkbench
Online web app for processing of eeg data for BCI purposes

# Dependencies 
Tested on Ubuntu 18.04

1. python3.7
2. Django2.2.6
3. pytz2019.3
4. sqlparse0.3.0

To install all dependencies use
"pip3.7 install -r requirements.txt"

# Installation
1. Install python3.7 
2. Clone this repository 
3. Create a virtual environement
   "python3.7 -m venv <name>"
4. Active the virtual environment
	 "source venv/bin/activate"
5. Install dependencies
	 -cd path/to/EEGWorkbench
	 -pip3.7 install -r requirements.txt
6. Run the server
	 -cd path/to/EEGWorkbench
	 -python3.7 ./manage.py runserver
