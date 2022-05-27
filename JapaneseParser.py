#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


LOGICAL_PARTICLES = ['が', 'を', 'へ', 'に', 'で']
NONLOGICAL_PARTICLES = ['は', 'の']


# Strips "possible_suffix" from "reversed_sentence", if "reversed_sentence" ends
# with "possible_suffix".
# @return ("reversed_sentence","possible_suffix") if "reversed_sentence" ends w/ "possible_suffix" o/w ("reversed_sentence",False).
def StripIfEndsWith(reversed_sentence, possible_suffix):
    reversed_possible_suffix = possible_suffix[::-1]
    if len(reversed_sentence) >= len(possible_suffix) \
       and reversed_sentence[:len(possible_suffix)] == reversed_possible_suffix:
        reversed_sentence = reversed_sentence[len(possible_suffix):]
        return reversed_sentence, possible_suffix
    return reversed_sentence, False


# @return (the shortened reversed_sentence, the stripped copula or False if there wasn't one)
def StripTrailingCopula(reversed_sentence):
    COPULA_FORMS = ['だ', 'だった', 'です', 'でした', 'である', 'であります', 'でござる', 'でございます']
    for copula_form in COPULA_FORMS:
        reversed_sentence, found_copula_form = StripIfEndsWith(reversed_sentence, copula_form)
        if found_copula_form:
            return reversed_sentence, found_copula_form
    return reversed_sentence, False


# @return (reversed_sentence, reversed_components)
def StripSentenceEnders(reversed_sentence, reversed_components):
    SENTENCE_ENDER_PARTICLES = ['か', 'ね', 'よ', 'な', 'の']
    while True:
        matched_at_least_one = False
        for sentence_ender_particle in SENTENCE_ENDER_PARTICLES:
            reversed_sentence, stripped_ender = StripIfEndsWith(reversed_sentence, sentence_ender_particle)
            if stripped_ender:
                reversed_components.append(stripped_ender)
                matched_at_least_one = True
        if not matched_at_least_one:
            break
    return reversed_sentence, reversed_components


# @return (the shortened reversed_sentence, the stripped punctuation mark or False if there wasn't one)
def StripPunctuationMark(reversed_sentence):
    PUNCTUATION_MARKS = ['。', '？', '！']
    for punctuation_mark in PUNCTUATION_MARKS:
        reversed_sentence, found_punctuation_mark = StripIfEndsWith(reversed_sentence, punctuation_mark)
        if found_punctuation_mark:
            return reversed_sentence, found_punctuation_mark
    return reversed_sentence, False


def DisplayResult(ORIGINAL_SENTENCE, reversed_components):
    print(ORIGINAL_SENTENCE)
    for component in reversed(reversed_components):
        print("\t" + component)

        
def ParseSentence(SENTENCE):
    reversed_components = []
    reversed_sentence = SENTENCE[::-1]
    reversed_sentence, punctuation_mark = StripPunctuationMark(reversed_sentence)
    if punctuation_mark:
        reversed_components.append(punctuation_mark)
    reversed_sentence, reversed_components = StripSentenceEnders(reversed_sentence, reversed_components)
    reversed_sentence, copula_form = StripTrailingCopula(reversed_sentence)
    if copula_form:
        reversed_components.append(copula_form)
    return reversed_components

        
def Main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' japanese_sentence')
        exit(1)

    ORIGINAL_SENTENCE = sys.argv[1]
    reversed_componenst = ParseSentence(ORIGINAL_SENTENCE)
    DisplayResult(ORIGINAL_SENTENCE, reversed_componenst)


Main()
