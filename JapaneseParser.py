#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


def StripSentenceEnders(reversed_sentence, reversed_components):
    sentence_ender_particles = ['か', 'ね', 'よ', 'な', 'の']
    while reversed_sentence and reversed_sentence[0] in sentence_ender_particles:
        reversed_components.append(reversed_sentence[0])
        reversed_sentence = reversed_sentence[1:]

        
def ParseSentence(sentence):
    reversed_components = []
    reversed_sentence = sentence[::-1]
    StripSentenceEnders(reversed_sentence, reversed_components)
    for component in reversed(reversed_components):
        print(component)

        
def Main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' japanese_sentence')
        exit(1)
    ParseSentence(sys.argv[1])


Main()
