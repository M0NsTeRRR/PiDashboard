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
from time import sleep as time_sleep

from yaml import safe_load
from clientMQTT import Client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# config file loaded
CONFIG_FILE = "config.yml"

# prefix topic
PREFIX_TOPIC = "PiDashboard/"

REGEX_IP = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
REGEX_DOMAIN = r"^(((?!-))(xn--|_{1,1})?[a-z0-9-]{0,61}[a-z0-9]{1,1}\.)*(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$"

# read content of config file
with open(CONFIG_FILE) as file:
    config = safe_load(file)

# check if the config file is properly filled
try:
    brokerMQTT = {
        "hostname": config.get("brokerMQTT", None).get("hostname", ""),
        "port": config.get("brokerMQTT", None).get("port", ""),
    }

    if not match(REGEX_IP, brokerMQTT["hostname"]) and not match(REGEX_DOMAIN, brokerMQTT["hostname"]):
        raise Exception("ServerMQTT hostname must be an IPV4 address")

    if not 0 <= brokerMQTT["port"] <= 65535:
        raise Exception("ServerMQTT port must be in range [0;65535]")

except Exception as e:
    logger.error('Configuration file is not filled properly : \n{}'.format(e))
    sys_exit(1)

try:
    clientMQTT = Client(brokerMQTT["hostname"], brokerMQTT["port"], PREFIX_TOPIC)
    clientMQTT.connect()
    while True:
        # replace the value of led_name with the name of the led
        led_name = "salon"
        # get the led state and assign it to the led_state variable
        led_state = "ON"
        clientMQTT.send_message("led/" + led_name, led_state)
        time_sleep(1)

except Exception as e:
    logger.error('Something wrong happened : \n{}'.format(e))
    sys_exit(1)
