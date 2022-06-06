#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys


LOGICAL_PARTICLES = ['が', 'を', 'へ', 'に', 'で']
NONLOGICAL_PARTICLES = ['は', 'の']
POSSIBLE_ADJECTIVE_ENDINGS = ['い']
VERB_INFINITIVE_ENDINGS = ['う', 'く', 'す', 'つ', 'ぬ', 'ぶ', 'む', 'る']
TE_ENDINGS = ['って', 'んで', 'いて', 'いで', 'して']


def IsHiragana(CHAR) -> bool:
    return u'\u3040' <= CHAR <= u'\u309F'


def IsKatakana(CHAR) -> bool:
    return u'\u30A0' <= CHAR <= u'\u30FF'


def IsKanji(CHAR) -> bool:
    return u'\u4E00' <= CHAR <= u'\u9FAF'


# @return True if "reversed_word" is probably an adjective, else False.
def IsProbablyAnAdjective(reversed_word: str) -> bool:
    if not IsHiragana(reversed_word[0])::
        return False

    # Adjectives can *never* end in えい;
    if len(reversed_word) > 1 and reversed_word[0:2] == 'いえ':
        return False

    # Past tense of adverbial adjective?
    if len(reversed_word) > 3 and reversed_word[0:3] == 'たっか':
        return True

    # Negative adverb?
    if len(reversed_word) > 3 and reversed_word[0:3] == 'いなく':
        return True

    # Negative past tense adverb?
    if len(reversed_word) > 4 and reversed_word[0:4] == 'たかなく':
        return True

    return reversed_word[0] in POSSIBLE_ADJECTIVE_ENDINGS


# @return the type of verb ending if it was one of the recognized endings, else None.
def ClassifyVerbEnding(reversed_word: strd) -> str:
    if len(reversed_word) > 1 and reversed_word[0:2] == 'すま':
        return 'ます'
    if len(reversed_word) > 2 and reversed_word[0:3] == 'んせま':
        return 'ません'
    return None
    
    
# Attempts to extract a verb, adjective or noun from the reversed_sentence.
# If successful, we return the shortened reversed_sentence and whatever we extracted
# o/w we return the original reversed_sentence and False.
def ExtracVerbAdjectiveOrNoun(reversed_sentence):
    if not reversed_sentence:
        return reversed_sentence, False
    if IsKatakana(reversed_sentence[0]):
        # Assume we have a word written w/ Katakana only!
        katakana_word = ''
        while reversed_sentence and IsKatakana(reversed_sentence[0]):
            katakana_word += reversed_sentence[0]
            reversed_sentence = reversed_sentence[1:]
        return reversed_sentence, katakana_word[::-1]
    if not IsHiragana(reversed_sentence[0]) and not IsKanji(reversed_sentence[0]):
        sys.exit("Non-Japanese character in input: " + reversed_sentence[0] + "!")
    verb_or_noun = ''
    while reversed_sentence and IsHiragana(reversed_sentence[0]):
        verb_or_noun += reversed_sentence[0]
        reversed_sentence = reversed_sentence[1:]
    while reversed_sentence and IsKanji(reversed_sentence[0]):
        verb_or_noun += reversed_sentence[0]
        reversed_sentence = reversed_sentence[1:]
    return reversed_sentence, verb_or_noun[::-1]


# Strips "POSSIBLE_SUFFIX" from "reversed_sentence", if "reversed_sentence" ends
# with "POSSIBLE_SUFFIX".
# @return ("reversed_sentence","POSSIBLE_SUFFIX") if "reversed_sentence" ends w/ "POSSIBLE_SUFFIX" o/w ("reversed_sentence",False).
def StripIfEndsWith(reversed_sentence, POSSIBLE_SUFFIX):
    reversed_possible_suffix = POSSIBLE_SUFFIX[::-1]
    if len(reversed_sentence) >= len(POSSIBLE_SUFFIX) \
       and reversed_sentence[:len(POSSIBLE_SUFFIX)] == reversed_possible_suffix:
        return reversed_sentence[len(POSSIBLE_SUFFIX):], POSSIBLE_SUFFIX
    return reversed_sentence, False


# This should handle one or two particles and what Cure Dolly calls a "car".
# @return (reversed_sentence, car, particles)
def ParseSentenceComponent(reversed_sentence):
    if not reversed_sentence:
        sys.exit("ParseSentenceComponent requires non-empty reversed_sentences!");
    
    # 1. Expect and strip particles:
    particles = ''
    if reversed_sentence and reversed_sentence[0] == 'と': # We're dealing w/ a quotation!
        particles += 'と'
        reversed_sentence = reversed_sentence[1:]
    elif reversed_sentence[0] in LOGICAL_PARTICLES:
        particles += reversed_sentence[0]
        reversed_sentence = reversed_sentence[1:]
        if reversed_sentence and reversed_sentence[0] in NONLOGICAL_PARTICLES:
            particles += reversed_sentence[0]
            reversed_sentence = reversed_sentence[1:]
    elif reversed_sentence[0] in NONLOGICAL_PARTICLES:
        particles += reversed_sentence[0]
        reversed_sentence = reversed_sentence[1:]

    reversed_sentence, car = ExtracVerbAdjectiveOrNoun(reversed_sentence)
    if not car:
        sys.exit('Failed to parse a "car"!')

    return reversed_sentence, car, particles

        
# @Return (the shortened reversed_sentence, the stripped copula or False if there wasn't one)
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
    reversed_sentence, verb_adjective_or_noun = ExtracVerbAdjectiveOrNoun(reversed_sentence)
    if verb_adjective_or_noun:
        reversed_components.append(verb_adjective_or_noun)

    while reversed_sentence:
        reversed_sentence, car, particles = ParseSentenceComponent(reversed_sentence)
        if particles:
            reversed_components.append(particles)
        if car:
            reversed_components.append(car)
            
    return reversed_components

        
def Main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' japanese_sentence')
        sys.exit(1)

    ORIGINAL_SENTENCE = sys.argv[1]
    reversed_componenst = ParseSentence(ORIGINAL_SENTENCE)
    DisplayResult(ORIGINAL_SENTENCE, reversed_componenst)


if __name__ == "__main__":
    Main()
