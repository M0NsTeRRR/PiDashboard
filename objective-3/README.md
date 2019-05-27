# Data privacy
At the moment we don't encrypt our data it's why if someone does an man-in-the-middle attack for example he can read and access to our
informations. It's why we need to implement a cipher algorithm.

To see packets on wireshark put `mqtt` in filter if there is a lot of traffic you can add the source IP of the client
In wireshark folder you have 3 screenshots :
1. list.PNG show you when the client try to connecto to the MQTT broker and send 2 messages, one on led
topic and the second one on temperature topic.
2. led.PNG show you the content of a MQTT led message
    - message="ON" (led state)
    - datetime="2019-05-27 15:34:32" (datetime)
3. temperature.PNG show you the content of a MQTT temperature message
    - message="40" (temperature value)
    - datetime="2019-05-27 15:29:59" (datetime)
    
# Data poisonning
At the moment we don't use any authentification as you can see we connect to the broker and we subscribe to the
topic. That is weird because if someone connect to the same broker and send informations, our server will listen
it and will execute some codes. It's why we need to implement authentification.

In `server/clientMQTT.py` on line 82
```python
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
```
