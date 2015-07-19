#!/usr/bin/env python

import random

vocabulary = dict()
originalVocabulary = dict()
articles = list()

def readVocabulary(input, default):
    print(input)
    with open(input) as fin:
        for line in fin:
            word = line.rstrip('\n')
            if not word or word[0] == ';': continue
            vocabulary[word] = default

def readArticle(input, skipColumn=0):
    print(input)
    article = []
    with open(input, 'r') as fin:
        for line in fin:
            row = []
            for triple in line.rstrip('\n').split(' ')[skipColumn:]:
                splited = triple.split('/')
                if len(splited) == 3:
                    row.append(splited)
            article.append(row)
    articles.append(article)

def getLineSentiment(line):
    acum = 0
    sign = 1
    count = 0
    for triple in line:
        word, proto, label = triple
        if word in ['.', ',', '!', '?']:
            sign = 1
        if word in ['not']:
            sign *= -1
        if proto not in vocabulary:
            continue
        acum += vocabulary[proto] * sign
        count += 1
    return acum / count if count else .0

def processArticle(article, diff):
    for line in article:
        ls = getLineSentiment(line)
        for triple in line:
            word, proto, label = triple
            if proto not in vocabulary:
                continue
            if proto not in diff:
                diff[proto] = { 'sum': 0, 'cnt': 0 }
            diff[proto]['sum'] += ls
            diff[proto]['cnt'] += 1

def iterate():
    for times in range(1):
        print('iterate %d' % times)
        diff = dict()
        for article in articles:
            processArticle(article, diff)
        for key in diff:
            if not diff[key]['cnt']:
                continue
            #vocabulary[key] *= diff[key]['sum'] / diff[key]['cnt']
            vocabulary[key] = diff[key]['sum'] / diff[key]['cnt']

def collectLines(article, diffWord):
    print('collectLines')
    for line in article:
        for triple in line:
            word, proto, label = triple
            if proto in diffWord:
                diffWord[proto]['lines'].append(line)

def printDiffWord(w, l):
    fout = open('outputs/brute_iterate_changed.html', 'w')
    fout.write("""
<!DOCTYPE html>
<html>
<head>
<title>Sentiment-Changed Words</title>
<meta charset="utf-8">
<style type="text/css">
p {
    font-family: Palatino, serif;
    line-height: 1.25em;
    margin: 0.3em 0;
}

.changed { background-color: #7159C7; color: #FFF; }
.vocabulary { background-color: #F76237; color: #FFF; }
</style>
</head>
<body>
<h1>Sentiment-Changed Words</h1>""")
    for d in l:
        key = d[0]
        value = w[key]
        fout.write("<h2>%s (%.6f -> %.6f)</h2>\n" % (key, value['old'], value['new']))
        random.shuffle(value['lines'])
        cnt = 0
        for line in value['lines']:
            fout.write('<p>')
            for word, root, wclass in line:
                triple = '%s/%s/%s' % (word, root, wclass)
                if root in w:
                    css = "changed"
                    title = "%.6f -> %.6f" % (w[root]['old'], w[root]['new'])
                    fout.write('<span class="%s" title="%s">%s</span> ' % (css, title, word))
                elif root in originalVocabulary:
                    css = "vocabulary"
                    title = "%.3f" % originalVocabulary[root]
                    fout.write('<span class="%s" title="%s">%s</span> ' % (css, title, word))
                else:
                    fout.write('%s ' % word)
            fout.write('</p>\n')
            cnt += 1
            if cnt == 5:
                break

    fout.write('''
</body>
</html>''')
    fout.close()

def diff():
    print('diff')
    diffList = []
    diffWord = dict()
    for key in vocabulary:
        old = originalVocabulary[key]
        new = vocabulary[key]
        d = new-old
        if d:
            diffList.append((key, old, new, d))
    diffList.sort(key=lambda item: abs(item[3]), reverse=True)
    with open('outputs/brute_iterate.txt', 'w') as fout:
        fout.write('key\told\tnew\tdiff\n')
        for d in diffList:
            fout.write('%s\t%.6f\t%.6f\t%.6f\n' % d)
            key, old, new, diff = d
            diffWord[key] = { 'old': old, 'new': new, 'lines' : [] }

    for article in articles:
        collectLines(article, diffWord)

    printDiffWord(diffWord, diffList)


readVocabulary('inputs/positive-words.txt', +1.0)
readVocabulary('inputs/negative-words.txt', -1.0)
originalVocabulary = vocabulary.copy()

readArticle('inputs/blender_sentences.txt', skipColumn=1)
readArticle('inputs/drill_POS.txt')
readArticle('inputs/fridge_ann.txt')
readArticle('inputs/movies_ann.txt')
readArticle('inputs/vacuum_ann.txt')
readArticle('inputs/washer_sentences.txt', skipColumn=1)
#readArticle('inputs/interesting.txt')

iterate()
diff()