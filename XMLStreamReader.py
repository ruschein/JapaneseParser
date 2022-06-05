#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xml.dom import pulldom
import sys


class XMLStreamReader():
    def __init__(self, file):
        self.events     = pulldom.parse(file)
        self.event      = None
        self.node       = None
        self.look_ahead = None

    # get next token 
    def next(self):
        if self.look_ahead == None:
            event = self.events.getEvent()
            if event is None:
                (self.event, self.node) = (pulldom.END_DOCUMENT, None)
            else:
                (self.event, self.node) = event
        else:
            (self.event, self.node) = self.look_ahead
            self.look_ahead = None
        # concatenate consecutive character nodes 
        while self.event == pulldom.CHARACTERS:
            self.look_ahead = self.events.__next__()
            while self.look_ahead[0] == pulldom.CHARACTERS:
                self.look_ahead = self.events.getEvent()
            break

    def isEndDocument(self):
        return self.event == pulldom.END_DOCUMENT

    def isWhiteSpace(self):
        return (self.event == pulldom.CHARACTERS and 
                len(self.node.data.strip()) == 0)

    def isStartElement(self):
        return self.event == pulldom.START_ELEMENT

    def isEndElement(self):
        return self.event == pulldom.END_ELEMENT

    def isCharacters(self):
        return self.event == pulldom.CHARACTERS

    def checkStartElement(self, method):
        if not self.isStartElement():
            sys.exit("%s called for an event of type: %s" % (method, self.event))
    
    def getLocalName(self):
        if not self.isStartElement() and not self.isEndElement():
            sys.exit("getLocalName called for an event of type: %s" % self.event)
        return self.node.localName

    def getAttributeCount(self):
        self.checkStartElement("getAttributeCount")
        return self.node.attributes.length

    def getAttributeLocalName(self, index):
        self.checkStartElement("getAttributeLocalName")
        return self.node.attributes.item(index).localName

    def getAttributeValue(self, index):
        self.checkStartElement("getAttributeValue")
        return self.node.attributes.item(index).value

    def getText(self):
        if not self.isCharacters():
            sys.exit("getText called for an event of type %s" % self.event)
        return self.node.data


if __name__ == "__main__":
    sys.exit("Library module. Don't call directly!")
