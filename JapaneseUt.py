#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Test setup for 
  parsing a 日本 sentence with JapaneseParser.
Usage:
  JapaneseUt.py <Test sentences file>
"""
import sys
import JapaneseEs

mode = None


dolly = ( # cd = Cure Dolly
    ("私がケーキを食べる。",
    "I eat cake",
    "cd#3 WA particle",
    "(私)がケーキを(食べる)。"
    ),
    # https://www.wanikani.com/vocabulary/食べる
    ("犬が食べる。",
     "The dog will eat",
    "cd#3 WA particle",
    "(犬)が(食べる)。"
    ),(
    "さくらが歩く。",
    "Sakura will walk",
    "cd#3 WA particle",
    "さくらが(歩く)。"
    ),(
    "犬が食べている",
    "The dog is eating.",
    "cd#4 te.",
    "(犬)が(食べる)ている",
    ),(
    "明日ケーキを食べる。",
    "Tomorrow I will eat cake",
    "ch#4 relative time.",
    "(明日)ケーキを(食べる)。"
    ),( # Tae Kim
       "友達は親切。",
       "Friend is kind.",
       "tk Adjectives and particles.",
       ""
    ),( # Tae Kim
       "友達は親切な人だ。",
       "Friend is kind person.",
       "tk Adjectives and particles.",
       ""
    ),( # Tae Kim: Bob and fish.
       "ボブは魚が好きだ。",
       "Bob likes fish.",
       "Pesent.",
       ""
    ),( # Tae Kim: Bob and fish.
       "ボブは魚が好きじゃない。",
       "Bob does not like fish.",
       "Present,negative.",
       ""
    ),( # Tae Kim: Bob and fish.
       "ボブは魚が好きだった。",
       "Bob liked fish.",
       "Past.",
       ""
    ),( # Tae Kim: Bob and fish.
       "ボブは魚が好きじゃなかった。",
       "Bob did not like fish.",
       "Past,negative",
       ""
    ),( # Tae Kim: Person,fish.
       "魚が好きな人。",
       "Person that likes fish.",
       "",
       ""
    ),( # Tae Kim: Person,fish.
       "魚が好きじゃない人。",
       "Person that does not like fish.",
       "",
       ""
    ),( # Tae Kim: Person,fish.
       "魚が好きだった人。",
       "Person that liked fish.",
       "",
       ""
    ),( # Tae Kim: Person,fish.
       "魚が好きじゃなかった人。",
       "Person that did not like fish.",
       "",
       ""
    ),( # Tae Kim: People, fish.
       "人は魚が好きだ",
       "People like fish.",
       "",
       ""
    ),( # Tae Kim: Descriptive noun clause == single noun.
       "魚が好きじゃない人は、肉が好きだ。",
       "Person who does not like fish like meat.",
       "",
       ""
    ),( # Tae Kim: Descriptive noun clause == single noun.
       "魚が好きな人は、野菜も好きだ。",
       "Person who likes fish also likes vegetables.",
       "",
       ""
    ),( # Tae Kim
       "",
       "",
       "",
       ""
    ))

sentences = ( # https://www.wanikani.com/vocabulary/後私
    ("その後私はそこを出るんだけど鞄を忘れてきたことに気付くんだ。",
     "After that I leave there but realize that I have forgotten my bag",
     [['は', 'その後私'], ['を', 'そこ'], ['を', '出るんだけど鞄'], ['に', '忘れてきたこと'], ['。', '気付くんだ']],
     [['は', 'その後私'], ['を', 'そこ'], ['を', 'wk/出る けど鞄'], ['に', '忘れてきたこと'], ['。', 'wk/気付く']]
    ),
    ("若い男女が人里離れた洋館で恐怖の一夜を過ごすという、ホラーの定番スタイルだ。",
     [['が', '若い男女'], ['を', '人里離れた洋館で恐怖の一夜'], ['。', '過ごすという、ホラーの定番スタイルだ']]
    ),
    ("この土地とこの家は私の物ですよ",
     [['は', 'この土地とこの家'], ['よ', '私の物です'], ['。', '']]
    ),
    ("アンタ本当にi器用ねっ。",
     [['に', 'アンタ本当'], ['ね', 'i器用'], ['。', 'っ']]
    ),
    ("主夫とか向いてるんじゃない？",
     [['な', '主夫とか向いてるんじゃ'], ['。', 'い']]
    ),
    ("でも、ジェンの家のベランダにいたヴィンスは上半身裸。",
     [['に', 'でも、ジェンの家のベランダ'], ['は', 'いたヴィンス'], ['。', '上半身裸']]
    ),
    ("いやー、もしかしたらすっぽんぽんだったかもッ！",
     [['。', 'いやー、もしかしたらすっぽんぽんだったかもッ']]
    ))

if 0:
    W  = '\033[0m'  # white (normal)
    R  = '\033[31m' # red
    G  = '\033[32m' # green
    O  = '\033[33m' # orange
    B  = '\033[34m' # blue
    P  = '\033[35m' # purple
else:
    W  = ''
    R  = ''
    G  = ''
    O  = ''
    B  = ''
    P  = ''

def ParseList(list):
    """ Split sentence by particles in 'logicals'.
        Then find Wanikani items to highlight. """
    for raw in JapaneseEs.RawList(list):
        if (raw != ""):
            print(raw)
    print()
    for sentence in list:
        if (sentence[0] != ""):
            print("%s" % (sentence[0]))
            logicals = JapaneseEs.ParseSentence(sentence[0])
            print(logicals)
            wanikanis = JapaneseEs.ParseLogicals(logicals)
            #print (wanikanis)
            wkdump = JapaneseEs.WkDump(wanikanis)
            if (sentence[3] == ""):
                print("= %s%s%s" % (G, wkdump, W))
            elif (sentence[3] == wkdump):
                print("+ %s%s%s" % (G, wkdump, W))
            else:
                print("- %s%s%s" % (B, wkdump, W))
                print("+ %s%s%s" % (G, sentence[3], W))
        print()
        

def ParseFile(input):
    for line in input.readlines():
        print("%s" % (line[:-1]))
        components = JapaneseEs.ParseSentence(line)
        print(components)
        print()

def ParseSentences(input):
    for (line, salami) in input:
        print("%s" % (line))
        components = JapaneseEs.ParseSentence(line)
        print(components)
        print("-")

if __name__ == "__main__":
    mode = "dolly"
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    elif (mode =="dolly"):
        ParseList(dolly)
    else:
        print("Input file: %s" % sys.argv[1])
        #ParseFile(open(sys.argv[1], 'r', encoding='UTF-8'))
        #ParseSentences(sentences)
        state = 0
        vocabText = open("../../wkdata/vocab.txt", 'r', encoding='UTF-8')
        vocabPy = open("wkData.py", 'w', encoding='UTF-8')
        vocabPy.write("# -*- coding: utf-8 -*-\n")
        vocabPy.write("vocabs = { # -*- coding: utf-8 -*-\n")
        #vocabs = {}
        for line in vocabText.readlines():
            if (state == 0) and (line.find('<span class="character" lang="ja">') > -1):
                state += 1
            elif (state == 1):
                vocab = line.strip()
                state += 1
            elif (state == 2) and (line.find('<li lang="ja">') > -1):
                state +=1
            elif (state == 3):
                reading = line.strip()
                state += 1
            elif (state == 4) and (line.find('<li>') > -1):
                splits = line.split('li')
                #vocabs[vocab] = [reading, splits[1][1:-2]]
                vocabPy.write("    '%s': %s,\n" % (vocab, str([reading, splits[1][1:-2]])))
                state = 0
            # for val in vocabs.items(): print(val)
        vocabPy.write("}\n")
        vocabPy.close()
                