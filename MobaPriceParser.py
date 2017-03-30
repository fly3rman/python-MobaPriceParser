#!/usr/bin/env python3

import doctest
import http.client
import urllib
import requests
import time
import random
import json
from bs4 import BeautifulSoup

# pylint: disable=C0103

def readSettingsFile(filename):
    'Reads the settings and article list from file'

    with open(filename) as data_file:
        data = json.load(data_file)
        return data

class Notification:
    'Optional Class documentation which iam too lazy for'

    def __init__(self):
        self.notificationMessage = None
        self.linkToProduct = None

class PushoverNotification(Notification):
    'Send an message via Pushover API'

    def send(self, notificationMessage, linkToProduct):
        """Send an message via Pushover API"""
        try:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                         urllib.parse.urlencode({
                             "token": settingsData["pushover"]["apiToken"],
                             "user": settingsData["pushover"]["receiverUser"],
                             "url": linkToProduct,
                             "message": notificationMessage}),
                             { "Content-type": "application/x-www-form-urlencoded" })
            conn.close()
            print("Pushover notification was sent")
        except Exception:
            print("Pushover notification could not be sent")


class MobaProduct:
    'Optional Class documentation which iam too lazy for'

    def __init__(self, productUrl, targetPrice=None):
        self.name = None
        self.model = None
        self.price = None
        self.productUrl = productUrl
        self.messageToSend = None
        if targetPrice is None:
            self.targetPrice = 0
        else:
            self.targetPrice = targetPrice


    def printData(self):
        """print the Data of this Object"""
        print(self.productUrl)
        print(self.name)
        print(self.model)
        print(self.price)
        print("        ")

    def notificate(self):
        """Build the message and call the list of real notification functions here"""
        self.messageToSend = (self.name + " von " +
                             self.model + " ist für " +
                             str(self.price) + " statt " +
                             str(self.targetPrice) + " Euro zu haben")
        PushoverNotification.send(self.messageToSend, self.productUrl)

    def setTargetPrice(self, targetPrice):
        """save the price as treshold for comparePrice"""
        self.targetPrice = targetPrice

    def comparePrice(self):
        """compares the price and act based on the decision"""
        if self.targetPrice != 0:
            if self.price <= self.targetPrice:
                self.notificate()


class MobaProductShopLippe(MobaProduct):
    'Provides a parser function for modellbahnshop-lippe. Using bs4'

    def parse(self):
        """ search for the html tags and content on modellbahnshop-lippe website """

        r = requests.get(self.productUrl)
        soup = BeautifulSoup(r.content, "lxml")
        self.price = int(float(soup.find(itemprop="price")["content"]))
        self.model = soup.find(itemprop="name").get_text()
        self.name = soup.find(
            "span", class_="eh3 col6").get_text()

def main():
    """Main function, put all the logic inside here"""
    settingsData = readSettingsFile("data.json")
    productList = settingsData["productList"]
    failed = 0
    for loco in productList:
        locoToProcess = MobaProductShopLippe(loco['url'], int(loco['wantedPrice']))
        try:
            locoToProcess.parse()
            #loco.setTargetPrice(loco.['wantedPrice'])
            locoToProcess.comparePrice()
            locoToProcess.printData()
            #dont drop requests too fast, webserver will be mad with us
        except Exception:
            print("failed: " + loco['url'])
            failed = failed + 1
            pass
        time.sleep(random.uniform(0.2, 1.0))
    if failed > 0:
        print("Could not process " + str(failed) + " url(s)")

if __name__ == "__main__":
    main()
