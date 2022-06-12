#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from XMLStreamReader import XMLStreamReader
import sentence_parser
import sys


xml_stream_reader = XMLStreamReader(sys.stdin)
while True:
  sentence = sentence_parser.ParseSentences(xml_stream_reader)
  if not sentence:
    exit(0)
  print(str(sentence))
