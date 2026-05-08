# Prayer Menu Bar App - Python Project
A MacOS menu bar app that displays Islamic prayer times based on your location (city and country) made entirely with python using the rumps python module. 

## Features
- Shows the next upcoming prayer and a live countdown in the menu bar
- Displays the full daily prayer schedule in the dropdown
- Sends a macOS notification when it's time to pray (still needs some improvement)
- Prompts for your city and country when clicking the 'Set Location' button after hitting the app icon in the menu bar
- Supports changing location at any time

## How it Works
1. After launching the app, press the app icon in your menu bar, then press 'Set Location' to enter your city and country
2. Coordinates are fetched by using the geopy module
3. Prayer times are retrieved from the Ummah API
4. The menu bar title updates every minute with the next prayer and time remaining

## Installation
1. Clone the repo
`git clone https://github.com/ahmedalkinani455/Prayer-Menu-Bar-App.git`
`cd prayer-menu-bar-app`

2. Create a virtual environment and install dependencies
`python3 -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`

3. Bundling as a macOS App
`pip install py2app` - if not already installed
`python setup.py py2app`

## Dependencies 
- rumps -> macOS menu bar framework
- requests -> makes HTTP requests in python
- geopy -> City to coordinate lookup
- timezonefinder -> Timezone detection from coordinates


## Potential Future Updates
- The notification system needs some work
- Error handling if a user inputs an invalid string when entering location
- Would like to convert this python script to a dmg file to make the installation process eaiser

## Notes
- The app requires an internet connection to retrieve the prayer times
- Location is determined by the city and country you enter. GPS is not used
- Compatible with MacOS 10.8+ and with modern macOS such as Monterey, Ventrua, and Tahoe
