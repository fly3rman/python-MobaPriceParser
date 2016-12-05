#!/usr/bin/env python3
import requests
import doctest

from bs4 import BeautifulSoup
# pylint: disable-msg=C0103


class MobaProduct:
    'Optional Class documentation which iam too lazy for'
    productData = {}

    def __init__(self, productUrl):
        self.productData['url'] = productUrl

    def print(self):
        """print the Data of this Object"""
        print(self.productData['name'])
        print(self.productData['model'])
        print(self.productData['price'])

    def comparePrice(self):
        return


class MobaProductShopLippe(mobaProduct):
    'Provides a parser function for modellbahnshop-lippe. Using bs4'

    def parse(self):
        """ search for the html tags and content on modellbahnshop-lippe website """

        r = requests.get(self.productData['url'])
        soup = BeautifulSoup(r.content, "lxml")
        self.productData['price'] = soup.find(itemprop="price")["content"]
        self.productData['model'] = soup.find(itemprop="name").get_text()
        self.productData['name'] = soup.find(
            "span", class_="eh3 col6").get_text()
        return self.productData


def main():
    firstLoco = mobaProductShopLippe(
        "http://www.modellbahnshop-lippe.com/produkt/Roco/1-4-004001-248876-0-0-0-33-5-2-0-gatt-de-p-0/ein_produkt.html")
    firstLoco.parse()
    firstLoco.print()

if __name__ == "__main__":
    main()
