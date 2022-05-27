#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Test setup for 
  parsing a 日本 sentence with JapaneseParser.
Usage:
  JapaneseParserUt.py <Test sentences file>
"""
import sys
import JapaneseParser


### Added to JapanesParser.py        
def ParseSentenceEs(sentence):
    particles = ['が', 'ね', 'よ', 'な', 'を', 'に','は'] # 'の', 
    pos = 0
    start = 0
    components = []
    for ch in sentence:
        if ch in particles:
            components.append([ch, sentence[start:pos]])
            start = pos+1
        pos += 1
    components.append(['。', sentence[start:-2]])
    return components


def ParseFile(input):
    for line in input.readlines():
        print("%s" % (line[:-1]))
        components = JapaneseParser.ParseSentenceEs(line)
        print(components)
        JapaneseParser.ParseSentence(line)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    else:
        print("Input file: %s" % sys.argv[1])
        ParseFile(open(sys.argv[1], 'r', encoding='UTF-8'))
