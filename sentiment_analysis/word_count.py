#!/usr/bin/env python3

from collections import defaultdict
from heapq import nlargest

def statWord(words, fout):
    w = []
    for key, value in words.items():
        w.append((value['sum'], key))
    popular = nlargest(30, w)

    fout.write('====== Most Popular Words:\n')
    for count, word in popular:
        fout.write('%-7s (%-5d times):\n' % (word, count))
        tmp = []
        for label, value in words[word].items():
            if label == 'sum': continue
            tmp.append((value/count*100, label))
        tmp.sort(reverse=True)
        for percent, label in tmp:
            fout.write('    %3s: %6.2f%%\n' % (label, percent))
        fout.write('\n')

def statLabel(labels, fout):
    l = []
    for key, value in labels.items():
        l.append((value['sum'], key))
    l.sort(reverse=True)

    fout.write('====== Most Popular Labels:\n')
    for count, label in l:
        fout.write('%-3s (%-5d times):\n' % (label, count))
        tmp = []
        for word, value in labels[label].items():
            if word == 'sum': continue
            tmp.append((value/count*100, word))
        tmp = nlargest(30, tmp)
        for percent, word in tmp:
            fout.write('    %16s: %6.2f%%\n' % (word, percent))
        fout.write('\n')

def wordCount(input, output, skipColumn=0):
    print(input)

    defaultFactory = lambda: defaultdict(int)
    words = defaultdict(defaultFactory)
    labels = defaultdict(defaultFactory)

    fin = open(input, 'r')
    for line in fin:
        row = []
        for triple in line.rstrip('\n').split(' ')[skipColumn:]:
            splited = triple.split('/')
            if len(splited) != 3:
                continue
            word, proto, label = splited

            words[proto][label] += 1
            labels[label][proto] += 1
            words[proto]['sum'] += 1
            labels[label]['sum'] += 1
    fin.close()

    fout = open(output, 'w')
    statWord(words, fout)
    statLabel(labels, fout)
    fout.close()


wordCount('inputs/blender_sentences.txt', 'outputs/blender_sentences_word_count.txt', skipColumn=1)
wordCount('inputs/drill_POS.txt',         'outputs/drill_POS_word_count.txt')
wordCount('inputs/fridge_ann.txt',        'outputs/fridge_ann_word_count.txt')
wordCount('inputs/movies_ann.txt',        'outputs/movies_ann_word_count.txt')
wordCount('inputs/vacuum_ann.txt',        'outputs/vacuum_ann_word_count.txt')
wordCount('inputs/washer_sentences.txt',  'outputs/washer_sentences_word_count.txt', skipColumn=1)