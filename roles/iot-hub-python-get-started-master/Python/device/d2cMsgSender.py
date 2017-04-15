"""
Module Name:  d2cMsgSender.py
Project:      IoTHubRestSample
Copyright (c) Microsoft Corporation.

Using [Send device-to-cloud message](https://msdn.microsoft.com/en-US/library/azure/mt590784.aspx) API to send device-to-cloud message from the simulated device application to IoT Hub.

This source is subject to the Microsoft Public License.
See http://www.microsoft.com/en-us/openness/licenses.aspx#MPL
All other rights reserved.

THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
"""

import base64
import hmac
import hashlib
import time
import requests
import urllib
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class D2CMsgSender:

    API_VERSION = '2016-02-03'
    TOKEN_VALID_SECS = 10
    TOKEN_FORMAT = 'SharedAccessSignature sig=%s&se=%s&skn=%s&sr=%s'

    def __init__(self, connectionString=None):
        if connectionString != None:
            iotHost, keyName, keyValue = [sub[sub.index('=') + 1:] for sub in connectionString.split(";")]
            self.iotHost = iotHost
            self.keyName = keyName
            self.keyValue = keyValue

    def _buildExpiryOn(self):
        return '%d' % (time.time() + self.TOKEN_VALID_SECS)

    def _buildIoTHubSasToken(self, deviceId):
        resourceUri = '%s/devices/%s' % (self.iotHost, deviceId)
        targetUri = resourceUri.lower()
        expiryTime = self._buildExpiryOn()
        toSign = '%s\n%s' % (targetUri, expiryTime)
        key = base64.b64decode(self.keyValue.encode('utf-8'))
        signature = urllib.quote(
            base64.b64encode(
                hmac.HMAC(key, toSign.encode('utf-8'), hashlib.sha256).digest()
            )
        ).replace('/', '%2F')
        return self.TOKEN_FORMAT % (signature, expiryTime, self.keyName, targetUri)

    def sendD2CMsg(self, deviceId, message):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s/messages/events?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.post(url, headers={'Authorization': sasToken}, data=message)
        return r.text, r.status_code

if __name__ == '__main__':
    connectionString = 'HostName=imanraspi02.azure-devices.net;SharedAccessKeyName=device;SharedAccessKey=bVZ8R6wfEESZLRbgeBarVqg6pRyrS6soQ/wgwcNqvfk='
    d2cMsgSender = D2CMsgSender(connectionString)
    deviceId = 'iotdevice1'
    sensor = Adafruit_DHT.DHT11
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    print(temperature)
    print(humidity)

    # read photoresistor
    # Hardware SPI configuration:  -> need to enable the SPI
    SPI_PORT   = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    light = mcp.read_adc(0)
# message = 'Hello, IoT Hub'
    message = 'temperature  : '+str(temperature)+', humidity : '+str(humidity)+' ligh : '+str(light)
    print(d2cMsgSender.sendD2CMsg(deviceId, message))

    response = urllib.urlopen("https://dweet.io/dweet/for/mypizero?temperature="+str(temperature)+"&humidity="+str(humidity)+"&light="+str(light))
    print 'RESPONSE:', response
    print 'URL     :', response.geturl()

    headers = response.info()
    print 'DATE    :', headers['date']
    print 'HEADERS :'
    print '---------'
    print headers

    data = response.read()
    print 'LENGTH  :', len(data)
    print 'DATA    :'
    print '---------'
    print data
