#!/usr/bin/env python3

import doctest
import http.client
import urllib
import requests
import time
import random
from bs4 import BeautifulSoup

# pylint: disable=C0103


productList = [
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-248876-0-0-0-33-5-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '250'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-276693-0-0-0-2-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '110'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-276698-0-0-0-2-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '200'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-276695-0-0-0-49-5-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '100'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-0-210744-003007-0-0-0-0-0-0-grp-de-p-0/ein_produkt.html', 'wantedPrice': '95'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-224382-0-0-0-2-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '110'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-215586-0-0-0-2-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '110'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-215842-0-0-0-35-10-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '120'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-215838-0-0-0-2-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '200'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/PIKO/15-4-004001-215836-0-0-0-6-10-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '120'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/ESU/29-4-004001-260119-0-0-0-49-10-3-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '390'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/ESU/29-4-004001-260120-0-0-0-2-4-3-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '390'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/ESU/29-4-004001-260121-0-0-0-49-5-3-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '390'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-265715-0-0-0-2-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '185'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-223324-0-0-0-8-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '215'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-249008-0-0-0-8-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '250'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-249004-0-0-0-40-10-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '220'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-262786-0-0-0-33-4-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '250'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-262788-0-0-0-33-5-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '247'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-265337-0-0-0-40-11-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '150'},
    #{'url': '', 'wantedPrice': ''},
    #ludmilla:
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-213482-0-0-0-49-5-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '165'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-265713-0-0-0-49-10-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '185'},
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-263238-0-0-0-49-5-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '185'},
    #russian:
    {'url': 'http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-222912-0-0-0-48-3-2-0-gatt-de-p-0/ein_produkt.html', 'wantedPrice': '240'},
]


class Notification:
    'Optional Class documentation which iam too lazy for'

    def __init__(self):
        self.notificationMessage = None
        self.linkToProduct = None

class PushoverNotification(Notification):
    'Send an message via Pushover API'

    def send(notificationMessage, linkToProduct):
        """Send an message via Pushover API"""
        try:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                         urllib.parse.urlencode({
                             "token": "URTOKENFORPUSHPOVER",
                             "user": "URUSER",
                             "url": linkToProduct,
                             "message": notificationMessage}),
                             { "Content-type": "application/x-www-form-urlencoded" })
            conn.close()
            print("Pushover notification was sent")
        except:
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
    for loco in productList:
        locoToProcess = MobaProductShopLippe(loco['url'], int(loco['wantedPrice']))
        try:
            locoToProcess.parse()
            #loco.setTargetPrice(loco.['wantedPrice'])
            locoToProcess.comparePrice()
            locoToProcess.printData()
            #dont drop requests too fast, webserver will be mad with us
        except:
            print("failed: " + loco['url'])
            pass
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    main()
