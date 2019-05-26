[EDUCATIONAL PROJECT]
1. Introduction

    The goal of this project is to display the state of Leds and the temperature send by the client on the server (website). 
    The client can be everything (Raspberry pi, Arduino etc...) 

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
###Client
1. Open `client` folder
2. Install requirements `pip install -r requirements.txt`
3. Fill `config.yml` with your broker MQQT port and IP

###Server
1. Open `server` folder
2. Install requirements `pip install -r requirements.txt`
3. Fill `config.yml` with :
    - your broker MQQT port and IP
    - your twilio account sid, auth_token and phone number
    - your phone number
    #####LINUX ONLY (install gunicorn)
4. `pip install gunicorn`
# Start
###Client
1. Open `client` folder
2. Start the program `python main.py` 

###Server
Open `server` folder

**It's recommended to use the server on linux because windows will use the development server**

#####Windows
1. Set environment variable `set FLASK_APP_main.py`
2. Start the program `flask run`

#####Linux
1. Start the program `gunicorn main:app --bind 0.0.0.0:80`

#Dev
**Replace `pass` line 85 with your code**
1. Send Led state change
    1. You need to read the input of the button when change state occurs (change ON to OFF and OFF to ON)
    2. Send the change state by using clientMQTT object with `send_message(topic, message)` method -> `clientMQTT.send_message("led/led_garage", "ON")`
        1. topic = `led/<led_name>`, replace <led_name> by the name of your choice
        2. message = `ÒN` or `OFF`
2. Send temperature information every second
    1. You need to read the temprature every each second (`time.sleep(1)`)
    2. Send the change state by using clientMQTT object with `send_message(topic, message)` method -> `clientMQTT.send_message("led/led_garage", "ON")`
        1. topic = `led/<led_name>`, replace <led_name> by the name of your choice
        2. message = `ÒN` or `OFF` 
3. Determine 2 attack vectors / security flaws (there's more):
    1. Data privacy (use wireshark)
    2. Data poisonning (see how clientMQTT in `server/clientMQTT.py` handle topic reply)
4. Fix issues found in part 3:
    1. Data poisonning -> User authentification
    2. Privacy security -> Payload encryption
    
# Usage guide
Access the server on http:myIPAdress:80/ -> replace **myIPAdress by your IP address**

# Licence

The code is under CeCILL license.

You can find all details here: http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - mastership@hotmail.fr
-Denis Genon-Catalot - Denis.Genon-Catalot@iut-valence.fr