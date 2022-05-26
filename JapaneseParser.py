#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


# Strips "possible_suffix" from "reversed_sentence", if "reversed_sentence" ends
# with "possible_suffix".
# @return "possible_suffix" if "reversed_sentence" ends w/ "possible_suffix" o/w False.
def StripIfEndsWith(reversed_sentence, possible_suffix):
    if len(reversed_sentence) >= len(possible_suffix) \
       and reversed_sentence[:len(possible_suffix)] == possible_suffix:
        reversed_sentence = reversed_sentence[len(possible_suffix):]
        print("possible_suffix = " + possible_suffix + ", reversed_sentence = "+reversed_sentence)
        return possible_suffix
    return False


def StripSentenceEnders(reversed_sentence, reversed_components):
    sentence_ender_particles = ['か', 'ね', 'よ', 'な', 'の']
    while True:
        matched_at_least_one = False
        for sentence_ender_particle in sentence_ender_particles:
            stripped_ender = StripIfEndsWith(reversed_sentence, sentence_ender_particle[::-1])
            print(str(stripped_ender) + ", " + reversed_sentence)
            if stripped_ender:
                reversed_components.append(stripped_ender)
                matched_at_least_one = True
        sys.exit(0)
        if not matched_at_least_one:
            break

        
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
