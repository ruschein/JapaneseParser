#!/usr/bin/env python
# -*- coding: utf-8 -*-


def ParseSentence(sentence):
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

if __name__ == "__main__":
    print("Library module. Don't call directly!")
