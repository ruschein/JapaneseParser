#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


# Strips "possible_suffix" from "reversed_sentence", if "reversed_sentence" ends
# with "possible_suffix".
# @return ("reversed_sentence","possible_suffix") if "reversed_sentence" ends w/ "possible_suffix" o/w ("reversed_sentence",False).
def StripIfEndsWith(reversed_sentence, possible_suffix):
    if len(reversed_sentence) >= len(possible_suffix) \
       and reversed_sentence[:len(possible_suffix)] == possible_suffix:
        reversed_sentence = reversed_sentence[len(possible_suffix):]
        return reversed_sentence, possible_suffix
    return reversed_sentence, False


def StripSentenceEnders(reversed_sentence, reversed_components):
    sentence_ender_particles = ['か', 'ね', 'よ', 'な', 'の']
    while True:
        matched_at_least_one = False
        for sentence_ender_particle in sentence_ender_particles:
            reversed_sentence, stripped_ender = StripIfEndsWith(reversed_sentence, sentence_ender_particle[::-1])
            if stripped_ender:
                reversed_components.append(stripped_ender)
                matched_at_least_one = True
        if not matched_at_least_one:
            break

        
def ParseSentence(sentence):
    reversed_components = []
    reversed_sentence = sentence[::-1]
    StripSentenceEnders(reversed_sentence, reversed_components)
    for component in reversed(reversed_components):
        print(component)

def ParseSentenceEs(sentence):
    """ Parse from start to end and capture components before
        particles. Ignore の for now."""
    particles = ['が', 'ね', 'よ', 'な', 'を', 'に','は'] #'の', 
    pos = 0
    start = 0
    components = []
    for ch in sentence:
        if ch in particles:
            components.append([ch, sentence[start:pos]])
            start = pos+1
        pos += 1
    components.append(['。', sentence[start:-2]]) # Drop 。 and newline.
    return components
        
def Main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' japanese_sentence')
        exit(1)
    ParseSentence(sys.argv[1])

if __name__ == "__main__":
    Main()
