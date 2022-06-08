# -*- coding: utf-8 -*-
import JapaneseParser as jp
import wkData as wk

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
        if (particle == '。'):
            verb = ''
            for ch in text:
                verb += ch
                if ch in verbEndings:
                    break
            # Assume we got a verb in dictionary form.
            wkEntries.append([particle, "(%s)" % verb])
        else:
            # Just hunt for kanji.
            kanji = "("
            kana = ""
            adjective = "("
            verb = "("
            kanjiMode = False
            for ch in text:
                if jp.IsKanji(ch):
                    #print("kanji="+ch)
                    kanji += ch
                    kanjiMode = True
                else:
                    if kanjiMode:
                        kanji += ")" # For only being kanjis.
                        kanjiMode = False
                    kana += ch
                    adjective += ch
                    verb += ch
            if (kanji != "("):
                if kanjiMode: kanji += ")"
                wkEntry = kanji + kana
            else:
                wkEntry = kana
            wkEntries.append([particle, wkEntry])
    return wkEntries

### Start Convert to JS.
# https://extendsclass.com/python-to-javascript.html


vocabs = { # -*- coding: utf-8 -*-
    '日本': ['にほん', 'Japan'],
    '食べる': ['たべる', 'To Eat'],
    '人': ['ひと', 'Person'],
    }

def isKanji(ch):
    return u'\u4E00' <= ch <= u'\u9FAF'

def matchVocab(text):
    """[日,本,人] = matchVocab("さくらは日本人です。")
        """
    #match = [ch for ch in text if isKanji(ch)]
    match = []
    vocab = "" 
    for ch in text:
        if isKanji(ch):
            if vocab+ch in vocabs:
                vocab = vocab+ch
            else:
                match.append(vocab)
                vocab = ch
        else: # Kana
            if vocab != "":
                match.append(vocab)
                vocab = ""
    return match

def splitVocab(text, matches):
    """ [さくらは,",",です] = splitVocab("さくらは日本人です。", [日,本,人])
        """
    split = []
    pos = 0
    for vocab in matches:
        pos = text.find(vocab)
        split.append(text[:pos])
        text = text[pos+len(vocab):]
    # Get tail.
    split.append(text)
    return split

### End JS

def WkDump(wkEntries):
    """ Dump logical parser taking kanji and recognise verbs
        in dictionary form. """
    wkDump0 = [ l[1]+l[0] for l in wkEntries]
    return "".join(wkDump0)

def RawList(list):
    """ Raw japanese string."""
    for entry in list:
        print(entry[0])
        vocabs = matchVocab(entry[0])
        print("vocabs=%s" % vocabs)
        if (vocabs != []):
            splits = splitVocab(entry[0], vocabs)
            print("splits=%s" %splits)
    return [entry[0] for entry in list]

if __name__ == "__main__":
    print("Library module. Don't call directly!")
