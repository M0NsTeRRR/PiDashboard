[EDUCATIONAL PROJECT]
1. Introduction

    The goal of this pedacogical project is to display some I/O (Led status and analog temperature) produce by Raspberry PI module (ref Raspberry PI 3B as least) as client to a website server. 
    The client can be everykind of hardware module (Raspberry pi, Arduino etc...)  

2. Usage

    It's an educationnal experience and it's why **YOU MUST NOT USE IT IN PRODUCTION**. The program has been developed
    in a limited time it's why because some features are non-optimized, unsecure and dirty.
    
    - `source` is the program who must be completed.
    - `objective-X` is the right program corresponding to the stage (X = stage).

3. Ojectives

    1. Send Led state change
    2. Send temperature information every second
    3. Determine 2 attack vectors / security flaws (there's more)
    4. Fix issues found in part 3

You have some informations and advices in Dev section.

# This tool uses :

* [Flask](http://flask.pocoo.org/) - Web microframework
* [Gunicorn](https://gunicorn.org/) - WSGI HTTP Server for UNIX
* [Jinja2](http://jinja.pocoo.org/) - Template engine
* [Bulma](https://bulma.io/) - CSS framework
* [Font Awesome](https://fontawesome.com/) - Icon library
* [Chart.js](https://fontawesome.com/) - Graph library
* [MQTT](http://mqtt.org/) - Connectivity protocol
* [Twilio](https://www.twilio.com/) - Cloud communication platform

# Requirements
* Python >= 3.6 
* pip
* broker MQTT

# Install
### Client
1. Open a terminal in `client` folder
2. Install requirements `pip install -r requirements.txt`
3. Edit `config.yml` with your broker MQQT port and IP

### Server
1. Open a terminal in `server` folder
2. Install requirements `pip install -r requirements.txt`
3. Edit `config.yml` with :
    - your broker MQQT port and IP
    - your twilio account sid, auth_token and phone number
    - your phone number

# Start
### Client
1. Open a terminal in `client` folder
2. Start the program `python main.py` 

### Server
1. Open a terminal in `server` folder
2. Set environment variable Linux `export FLASK_APP=main.py` / Windows : `set FLASK_APP=main.py` 
3. Start the program `flask run --host 0.0.0.0`

# Dev
**Replace `pass` line 86 with your code in `client/main.py`**
1. Send Led state change
    1. You need to read the input of the button when change state occurs (change ON to OFF and OFF to ON)
    2. Send the change state by using clientMQTT object with `send_message(topic, message)` method -> `clientMQTT.send_message("led/led_garage", "ON")`
        1. topic = `led/<led_name>`, replace <led_name> by the name of your choice
        2. message = `ÒN` or `OFF`
2. Send temperature information every second
    1. You need to read the temprature every each second (`time_sleep(1)`)
    2. Send the change state by using clientMQTT object with `send_message(topic, message)` method -> `clientMQTT.send_message("led/led_garage", "ON")`
        1. topic = `led/<led_name>`, replace <led_name> by the name of your choice
        2. message = `ÒN` or `OFF` 
3. Determine 2 attack vectors / security flaws (there's more):
    1. Data privacy (use wireshark)
    2. Data poisonning (see how clientMQTT in `server/clientMQTT.py` handle topic reply)
4. Fix issues found in part 3:
    1. Data poisonning -> User authentification
    2. Data privacy -> Payload encryption
    
# Usage guide
Access the server on http:myIPAdress:5000/ -> replace **myIPAdress by your IP address**

# Licence

The code is under CeCILL license.

You can find all details here: https://cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - ludovic.ortega@adminafk.fr
-Denis Genon-Catalot - denis.genon-catalot@univ-grenoble-alpes.fr
