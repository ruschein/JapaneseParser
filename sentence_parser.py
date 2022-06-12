#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from XMLStreamReader import XMLStreamReader
import sys


class SentenceComponent(Enum):
  JAPANESE_SENTENCE = 1
  ENGLISH_SENTENCE  = 2
  SENTENCE_PARTS    = 3


# @return True if we managed to find "TAG_NAME" before reaching the end
#         of the document, else False.
def _SkipToOpeningTag(xml_stream_reader: XMLStreamReader, TAG_NAME: str) -> bool:
  while not xml_stream_reader.isEndDocument():
    xml_stream_reader.next()
    if xml_stream_reader.isStartElement() \
       and xml_stream_reader.getLocalName() == TAG_NAME:
      return True
  return False

  
# @return a tuple with items described by the SentenceComponent enum
#         or None if the end of the XML stream was reached.
def ParseSentences(xml_stream_reader: XMLStreamReader):
  if not _SkipToOpeningTag(xml_stream_reader, "sentence"):
    return None
  
  # Extract the original Japanese sentence:
  if not _SkipToOpeningTag(xml_stream_reader, "original"):
    sys.exit("unexpected end of document while looking for \"original\" opening tag!")
  xml_stream_reader.next()
  if not xml_stream_reader.isCharacters():
    sys.exit("expected characters after \"original\" opening tag!")
  japanese_sentence = xml_stream_reader.getText()

  # Extract the translated English sentence:
  if not _SkipToOpeningTag(xml_stream_reader, "english"):
    sys.exit("unexpected end of document while looking for \"english\" opening tag!")
  xml_stream_reader.next()
  if not xml_stream_reader.isCharacters():
    sys.exit("expected characters after \"english\" opening tag!")
  english_sentence = xml_stream_reader.getText()

  # Extract the expected sentence parts:
  if not _SkipToOpeningTag(xml_stream_reader, "parts"):
    sys.exit("unexpected end of document while looking for \"parts\" opening tag!")
  sentence_parts = []
  while True:
    xml_stream_reader.next()
    if xml_stream_reader.isEndDocument():
      sys.exit("unexpected end of document while processing sentence parts!")       
    if xml_stream_reader.isEndElement() \
       and xml_stream_reader.getLocalName() == "parts":
      break
    if xml_stream_reader.isStartElement() \
       and xml_stream_reader.getLocalName() == "part":
      if xml_stream_reader.getAttributeCount() != 1 or xml_stream_reader.getAttributeLocalName(0) != "type":
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
