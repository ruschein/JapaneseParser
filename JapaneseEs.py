# -*- coding: utf-8 -*-
import JapaneseParser as jp


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
    if sentence[-1] =='。':
        components.append(['。', sentence[start:-1]]) # Drop 。 .
    elif sentence[-2] =='。':
        components.append(['。', sentence[start:-2]]) # Drop 。 and newline.
    else: # Just take the rest.
        components.append(['。', sentence]) # Drop 。 and newline.
    return components

def ParseParticles(sentence):
    """ Parse from start to end and capture components before particles.
        Handle logical particles and は.
        To do: 'よ', 'と', 'の'? """
    # cd#8b: Cure Dolly's detectives + は
    particles = ['が', 'を', 'に', 'へ', 'で', 'は'] 
    pos = 0
    start = 0
    components = []
    for ch in sentence:
        if ch in particles:
            components.append([ch, sentence[start:pos]])
            start = pos+1
        pos += 1
    if sentence[-1] =='。':
        components.append(['。', sentence[start:-1]]) # Drop 。 .
    elif sentence[-2] =='。':
        components.append(['。', sentence[start:-2]]) # Drop 。 and newline.
    else: # Just take the rest.
        components.append(['。', sentence]) # Drop 。 and newline.
    return components

# cd#5 Japanese verb groups and the te.form.
TeForms = {"って": "うつる",
           "んて": "ぬぶむ", 
           "いて": "く",
           "いで": "ぐ", 
           "して": "す"}

def ParseLogicals(logicals):
    """ Dump logical parser taking kanji and recognise verbs
        in dictionary form. """
    # cd#5 Japanese verb groups and the te.form.
    verbEndings = ['う','つ','る','ぬ','ぶ','む','く','ぐ','す']
    wkEntries = []
    for (particle, text) in logicals:
        if (particle == '。') and (text[-1] in verbEndings):
            # Assume we got a verb in dictionary form.
            wkEntries.append([particle, "(%s)" % text])
        else:
            # Just hunt for kanji.
            wkEntry = ""
            for ch in text:
                if jp.IsKanji(ch):
                    wkEntry += "(%s)" % ch
                else:
                    wkEntry += ch
            wkEntries.append([particle, wkEntry])
    return wkEntries

def WkDump(wkEntries):
    """ Dump logical parser taking kanji and recognise verbs
        in dictionary form. """
    wkDump0 = [ l[1]+l[0] for l in wkEntries]
    return "".join(wkDump0)

def RawList(list):
    """ Raw japanese string."""
    return [entry[0] for entry in list]

if __name__ == "__main__":
    print("Library module. Don't call directly!")
