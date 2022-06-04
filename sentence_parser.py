#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from XMLStreamReader import XMLStreamReader
import sys


class SentenceComponent(Enum):
  JAPANESE_SENTENCE = 1
  ENGLISH_SENTENCE  = 2
  SENTENCE_PARTS    = 3


# @return a tuple with items described by the SentenceComponent enum
#         or None if the end of the XML stream was reached.
def ParseSentences(xml_stream_reader: XMLStreamReader):
  # Skip to next "sentence" opening tag:
  while True:
    xml_stream_reader.next()
    if xml_stream_reader.isStartElement() \
       and xml_stream_reader.getLocalName() == "sentence":
      break
    if xml_stream_reader.isEndElement() \
       and xml_stream_reader.getLocalName() == "sentences":
      return None

  # Extract the original Japanese sentence:
  while True:
    xml_stream_reader.next()
    if xml_stream_reader.isStartElement() \
       and xml_stream_reader.getLocalName() == "original":
      break
  if not xml_stream_reader.isCharacters():
    sys.exit("expected characters after \"original\" opening tag!")
  japanese_sentence = xml_stream_reader.getText()

  # Extract the translated English sentence:
  while True:
    xml_stream_reader.next()
    if xml_stream_reader.isStartElement() \
       and xml_stream_reader.getLocalName() == "english":
      break
  if not xml_stream_reader.isCharacters():
    sys.exit("expected characters after \"english\" opening tag!")
  english_sentence = xml_stream_reader.getText()

  # Extract the expected sentence parts:
  while True:
    xml_stream_reader.next()
    if xml_stream_reader.isStartElement() \
       and xml_stream_reader.getLocalName() == "parts":
      break
  sentence_parts = []
  while True:
    xml_stream_reader.next()
    if xml_stream_reader.isEndElement() \
       and xml_stream_reader.getLocalName() == "parts":
      break
    if xml_stream_reader.isStartElement() \
       and xml_stream_reader.getLocalName() == "part":
      if xml_stream_reader.getAttributeCount() != 1 or xml_stream_reader.getAttributeLocalName() != "type":
        sys.exit("expected the \"part\" tag to have exactly one attribute named \"type\"!")
      part_type = xml_stream_reader.getAttributeValue(0)
      xml_stream_reader.next()
      if not xml_stream_reader.isCharacters():
        sys.exit("expected \"characters\" after the \"part\" opening tag!")
      part_characters = xml_stream_reader.getText()
      sentence_parts.append((part_type, part_characters))
  return (japanese_sentence, english_sentence, sentence_parts)


if __name__ == "__main__":
    sys.exit("Library module. Don't call directly!")
