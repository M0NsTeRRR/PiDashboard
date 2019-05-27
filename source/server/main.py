# ----------------------------------------------------------------------------
# Copyright © Ludovic Ortega, 2019
#
# Contributeur(s):
#     * Ortega Ludovic - mastership@hotmail.fr
#     * Denis Genon-Catalot - denis.genon-catalot@univ-grenoble-alpes.fr
#
# Ce logiciel, PiDashboard, est un programme informatique à but éducatif.
# Il a été developpé spécialement pour des travaux pratiques sur l'IoT et
# des RaspberryPi.
#
# Ce logiciel est régi par la licence CeCILL soumise au droit français et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
# sur le site "http://www.cecill.info".
#
# En contrepartie de l'accessibilité au code source et des droits de copie,
# de modification et de redistribution accordés par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
# seule une responsabilité restreinte pèse sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les concédants successifs.
#
# A cet égard  l'attention de l'utilisateur est attirée sur les risques
# associés au chargement,  à l'utilisation,  à la modification et/ou au
# développement et à la reproduction du logiciel par l'utilisateur étant
# donné sa spécificité de logiciel libre, qui peut le rendre complexe à
# manipuler et qui le réserve donc à des développeurs et des professionnels
# avertis possédant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
# logiciel à leurs besoins dans des conditions permettant d'assurer la
# sécurité de leurs systèmes et ou de leurs données et, plus généralement,
# à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
#
# Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
# pris connaissance de la licence CeCILL, et que vous en avez accepté les
# termes.
# ----------------------------------------------------------------------------

import logging
from sys import exit as sys_exit
from re import match

from flask import Flask, redirect, url_for, render_template, jsonify, request
from yaml import safe_load

from clientMQTT import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_FILE = "config.yml"

PREFIX_TOPIC = "PiDashboard/"

REGEX_TOPIC = r"^[a-z0-9_]{3,10}$"
REGEX_IP = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
REGEX_DOMAIN = r"^(((?!-))(xn--|_{1,1})?[a-z0-9-]{0,61}[a-z0-9]{1,1}\.)*(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$"
REGEX_PHONE = r"^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$"


with open(CONFIG_FILE) as file:
    config = safe_load(file)

try:
    brokerMQTT = {
        "hostname": config.get("brokerMQTT", None).get("hostname", ""),
        "port": config.get("brokerMQTT", None).get("port", ""),
    }

    REFRESH = 1
    LED = {}
    TEMPERATURE = {"datetime": [], "value": []}
    PHONE_ALERT = {
        "user": {
            "phone_number": config.get("user", None).get("phone_number", ""),
        },
        "twilio": {
            "phone_number": config.get("twilio", None).get("phone_number", ""),
            "account_sid": config.get("twilio", None).get("account_sid", ""),
            "auth_token": config.get("twilio", None).get("auth_token", ""),
        },
        "treshold": 20,
    }

    if not match(REGEX_IP, brokerMQTT["hostname"]) and not match(REGEX_DOMAIN, brokerMQTT["hostname"]):
        raise Exception("brokerMQTT hostname must be an IPV4 address")

    if not 0 <= brokerMQTT["port"] <= 65535:
        raise Exception("brokerMQTT port must be in range [0;65535]")

    if not match(REGEX_PHONE, PHONE_ALERT["twilio"]["phone_number"]):
        raise Exception("Twilio phone_number is incorrect")

    if not PHONE_ALERT["twilio"]["account_sid"]:
        raise Exception("Twilio account_sid is incorrect")

    if not PHONE_ALERT["twilio"]["auth_token"]:
        raise Exception("Twilio auth_token is incorrect")

    if not match(REGEX_PHONE, PHONE_ALERT["user"]["phone_number"]):
        raise Exception("User phone number is incorrect")

except Exception as e:
    logger.error('Configuration file is not filled properly : \n{}'.format(e))
    sys_exit(1)

try:
    clientMQTT = Client(brokerMQTT["hostname"], brokerMQTT["port"], PREFIX_TOPIC, LED, TEMPERATURE, PHONE_ALERT)
    clientMQTT.connect()
except Exception as e:
    logger.error('Something wrong happened : \n{}'.format(e))
    sys_exit(1)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        active={'index': 'is-active'},
        health="UP" if clientMQTT.is_alive() else "DOWN",
        uptime=clientMQTT.getUptime(),
        refresh=REFRESH,
        leds=LED,
        temperatures=TEMPERATURE,
        phone_alert=PHONE_ALERT
    )


@app.route('/get/information')
def get_information():
    """
    Endpoint to get value of INFORMATION
    :return: JSON with value of health, uptime and refresh
    """
    return jsonify(health="UP" if clientMQTT.is_alive() else "DOWN", uptime=clientMQTT.getUptime(), refresh=REFRESH, phone_number=PHONE_ALERT["user"]["phone_number"])


@app.route('/get/data/led')
def get_data_led():
    """
    Endpoint to get data about LED topics
    :return: JSON with informations about led topics
    """
    return jsonify(LED)


@app.route('/get/data/temperature')
def get_data_temperature():
    """
    Endpoint to get data about TEMPERATURE topic
    :return: JSON with information about temperature topic
    """
    return jsonify(TEMPERATURE)


@app.route('/post/temperature/treshold', methods=["POST"])
def post_temperature_treshold():
    """
    Endpoint to post the treshold of temperature
    """
    temperature_treshold = request.form["temperature_treshold"]
    try:
        if temperature_treshold and -20 <= int(temperature_treshold) <= 50:
            PHONE_ALERT["treshold"] = temperature_treshold
    except:
        pass
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
