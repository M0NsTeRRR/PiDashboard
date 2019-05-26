# ----------------------------------------------------------------------------
# Copyright © Ludovic Ortega, 2019
#
# Contributeur(s):
#     * Ortega Ludovic - mastership@hotmail.fr
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
from threading import Thread
from datetime import datetime, timedelta
from time import sleep as time_sleep
from json import loads as json_loads, dumps as json_dumps

import paho.mqtt.client as mqtt


from twilio.rest import Client as twilio
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


class Client(Thread):
    def __init__(self, broker_hostname, broker_port, prefix_topic, led, temperature, phone_alert):
        """
        Create a client to send message to a broker
        :param broker_hostname: Broker hostname to connect
        :param broker_port: Broker port to connect
        :param prefix_topic: MQTT prefix topic used
        :param led: dictionnary where are saved leds informations
        :param temperature: list where are saved temperature informations
        :param phone_alert: dictionnary where are saved phone alert informations
        """
        Thread.__init__(self)
        self.broker_hostname = broker_hostname
        self.broker_port = broker_port
        self.prefix_topic = prefix_topic
        self.echo_hello = "echo_hello"
        self.reply_hello = "reply_hello"
        self.led_topic = "led/#"
        self.temperature_topic = "temperature"
        self.led = led
        self.temperature = temperature
        self.phone_alert = phone_alert
        self.first_hello = datetime.now().replace(microsecond=0)
        self.last_hello = datetime.now().replace(microsecond=0) - timedelta(seconds=30)
        self.client = mqtt.Client()
        self.clientSMS = twilio(self.phone_alert["twilio"]["account_sid"], self.phone_alert["twilio"]["auth_token"])

    def connect(self):
        """
        Connect to a broker
        """
        self.client.connect(self.broker_hostname, self.broker_port)
        logger.info("Connected to broker {}:{}".format(self.broker_hostname, self.broker_port))
        self.subscribe_to_one_topic(self.reply_hello, self.__on_reply_hello_message)
        self.subscribe_to_one_topic(self.led_topic, self.__on_led_message)
        self.subscribe_to_one_topic(self.temperature_topic, self.__on_temperature_message)
        self.client.loop_start()
        time_sleep(4)
        self.start()

    def send_message(self, topic, message):
        """
        Send a message to the broker
        :param message: the message to send
        """
        try:
            message_send = json_dumps({"message": message, "datetime": str(datetime.now().replace(microsecond=0))})
            self.client.publish(self.prefix_topic + topic, message_send)
            logger.info("Datetime: {}\nMessage sent on topic : {}".format(datetime.now().replace(microsecond=0), topic))
            logger.debug("Message: {}".format(json_loads(message_send)))
        except Exception as e:
            logger.error("Something wrent wrong when it try to send the message")
            logger.debug("{}".format(e))

    def run(self):
        while True:
            self.send_message(self.echo_hello, "echo hello")
            time_sleep(5)

    def __on_reply_hello_message(self, client, userdata, message):
        """
        Handle message of self.reply_hello
        :param client:client instance of the callback
        :param userdata:private user data
        :param message:an instance of MQTTMessage
        :return:
        """
        try:
            message = self.__read_message(message)
            if not self.is_alive():
                self.first_hello = datetime.now().replace(microsecond=0)
            self.last_hello = datetime.now().replace(microsecond=0)
        except Exception as e:
            logger.error("Something wrent wrong when it try to read the message")
            logger.debug("{}".format(e))

    def __on_led_message(self, client, userdata, message):
        """
        Handle message of self.reply_topic
        :param client:client instance of the callback
        :param userdata:private user data
        :param message:an instance of MQTTMessage
        :return:
        """
        try:
            message = self.__read_message(message)
            if message["message"] == "ON" or message["message"] == "OFF":
                self.led[message["topic"].replace(self.prefix_topic + self.led_topic[:self.led_topic.rfind("/")+1], "")] = message["message"]
            else:
                logger.error("Invalid value received".format(message["message"]))
        except Exception as e:
            logger.error("Something wrent wrong when it try to read the message")
            logger.debug("{}".format(e))

    def __on_temperature_message(self, client, userdata, message):
        """
        Handle message of self.reply_topic
        :param client:client instance of the callback
        :param userdata:private user data
        :param message:an instance of MQTTMessage
        :return:
        """
        try:
            message = self.__read_message(message)
            if -20 <= float(message["message"]) <= 50:
                self.temperature["datetime"].append(message["datetime"])
                self.temperature["value"].append(message["message"])
                if float(message["message"]) > float(self.phone_alert["treshold"]):
                    self.send_sms('PiDashboard WARNING : Threshold has been crossed with {}°C ({})'.format(message["message"], message["datetime"]))
            else:
                logger.error("Invalid value received".format(message["message"]))
        except TwilioRestException as e:
            logger.error("Error when it try to send sms")
            logger.debug("{}".format(e))
        except Exception as e:
            logger.error("Something wrent wrong when it try to read the message")
            logger.debug("{}".format(e))

    @staticmethod
    def __read_message(message):
        """
        Read MQTT JSON message
        :param message:An instance of MQTT message
        :return: Dictionnarie with message, message datetime emission, topic, qos and flag
        """
        message_received = json_loads(message.payload)
        topic = message.topic
        qos = message.qos
        flag = message.retain
        logger.info("Datetime: {}\nMessage received on topic: {}".format(datetime.now().replace(microsecond=0), topic))
        logger.debug(
            "message : {}\nqos: {}\nflag: {}\n".format(message_received, qos, flag))
        return {"message": message_received["message"], "topic": topic, "datetime": message_received["datetime"], "qos": qos, "flag": flag}

    def subscribe_to_one_topic(self, topic, callback):
        """
        Subscribe to one topic
        :param topic: topic to subscribe
        :param callback: function who handle the topic
        """
        self.client.subscribe(self.prefix_topic + topic)
        self.client.message_callback_add(self.prefix_topic + topic, callback)
        logger.info("Subscribed to topic: {}".format(self.prefix_topic + topic))

    def is_alive(self):
        """
        :return: client is alive
        """
        return self.last_hello + timedelta(seconds=10) >= datetime.now().replace(microsecond=0)

    def getUptime(self):
        """
        :return: client uptime
        """
        if self.is_alive():
            return str(datetime.now().replace(microsecond=0) - self.first_hello.replace(microsecond=0))
        else:
            return "UNKNOW"

    def send_sms(self, body):
        sms = self.clientSMS.messages.create(
            body=body,
            from_=self.phone_alert["twilio"]["phone_number"],
            to=self.phone_alert["user"]["phone_number"]
        )

    def stop(self):
        """
        Stop and close the connection
        """
        self.client.loop_stop()
