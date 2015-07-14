#!/usr/bin/env python3

wordClasses = {}

def processArticle(input, output, skipFirst=True):
    print(output)
    fin = open(input, 'r')
    fout = open(output, 'w')
    start = 1 if skipFirst else 0
    for line in fin:
        for triple in line.rstrip('\n').split(' ')[start:]:
            try:
                word, root, wclass = triple.split('/')
                fout.write(word)
                fout.write(' ')
                if wclass not in wordClasses:
                    wordClasses[wclass] = triple
            except:
                print('    skip triple:', triple)
        fout.write('\n')
    fin.close()
    fout.close()

def printWordClasses(output):
    print(output)
    with open(output, 'w') as fout:
        for key, value in wordClasses.items():
            fout.write(value)
            fout.write('\n')

processArticle('inputs/blender_sentences.txt', 'outputs/blender_sentences.txt', False)
processArticle('inputs/drill_POS.txt', 'outputs/drill_POS.txt')
processArticle('inputs/fridge_ann.txt', 'outputs/fridge_ann.txt')
processArticle('inputs/movies_ann.txt', 'outputs/movies_ann.txt')
processArticle('inputs/vacuum_ann.txt', 'outputs/vacuum_ann.txt')
processArticle('inputs/washer_sentences.txt', 'outputs/washer_sentences.txt', False)

printWordClasses('outputs/word_class.txt')