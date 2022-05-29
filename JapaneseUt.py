#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Test setup for 
  parsing a 日本 sentence with JapaneseParser.
Usage:
  JapaneseUt.py <Test sentences file>
"""
import sys
import JapaneseEs

sentences = (
    ("その後私はそこを出るんだけど鞄を忘れてきたことに気付くんだ。",
     [['は', 'その後私'], ['を', 'そこ'], ['を', '出るんだけど鞄'], ['に', '忘れてきたこと'], ['。', '気付くんだ']]
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
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    else:
        print("Input file: %s" % sys.argv[1])
        ParseFile(open(sys.argv[1], 'r', encoding='UTF-8'))
        #ParseSentences(sentences)
