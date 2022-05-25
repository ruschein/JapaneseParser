#!/usr/bin/env python
import sys


def ParseSentence(sentence):
    reversed_components = []
    for char in reversed(sentence):
        print(char)
    for component in reversed(reversed_components):
        print(component)

        
def Main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' japanese_sentence')
        exit(1)
    ParseSentence(sys.argv[1])


Main()
