#!/usr/bin/env python3

import os
import random
import platform

vocabulary = set()
row = list()

def readVocabulary(input):
    print(input)
    with open(input) as fin:
        for line in fin:
            word = line.rstrip()
            if not word or word[0] == ';': continue
            vocabulary.add(word)

def readArticle(input):
    print(input)
    with open(input, 'r') as fin:
        for line in fin:
            cur = []
            for triple in line.rstrip('\n').split(' '):
                splited = tuple(triple.split('/'))
                if len(splited) == 3:
                    cur.append(splited)
                else:
                    cur.append((triple, '', ''))
            row.append(cur)

def answer():
    rowNumber = random.randrange(len(row))
    line = row[rowNumber]

    wordList = []
    for idx, triple in enumerate(line):
        w, p, l = triple
        if p in vocabulary:
            wordList.append(idx)
    if not wordList:
        return True
    wordNumber = random.choice(wordList)
    word = line[wordNumber][0]

    firstLine = ''
    secondLine = ''
    for i, triple in enumerate(line):
        w, p, l = triple
        width = len(w)+1
        firstLine += '%*d' % (width, i)
        secondLine += '%*s' % (width, w)

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    print(firstLine)
    print(secondLine)
    print()
    res = input('What do you think of word **%s** (at index %d)? [-1 / 0 / 1]: ' % (word, wordNumber)).strip()
    if res in ['-1', '0', '1']:
        with open('outputs/train.txt', 'a') as fout:
            fout.write('%d %d %s\n' % (rowNumber, wordNumber, res))
        return True
    
    return False


readVocabulary('inputs/positive-words.txt')
readVocabulary('inputs/negative-words.txt')

readArticle('inputs/blender_sentences.txt')
readArticle('inputs/drill_POS.txt')
readArticle('inputs/fridge_ann.txt')
readArticle('inputs/movies_ann.txt')
readArticle('inputs/vacuum_ann.txt')
readArticle('inputs/washer_sentences.txt')

while True:
    if not answer():
        break
        