#!/usr/bin/env python3

wordClasses = {}
positiveWords = set()
negativeWords = set()

def readVocabulary(input, s):
    with open(input) as fin:
        for line in fin:
            word = line.rstrip('\n')
            if not word or word[0] == ';': continue
            s.add(word)


def processArticle(input, html, txt, skipFirst=True):
    print(html)
    fin = open(input, 'r')
    fhtml = open(html, 'w')
    ftxt = open(txt, 'w')
    fhtml.write("""
<!DOCTYPE html>
<html>
<head>
<title>%s</title>
<meta charset="utf-8">
<style type="text/css">
p {
    font-family: Palatino, serif;
    line-height: 1.25em;
    margin: 0.3em 0;
}

.positive { background-color: #AA3939; color: #FFF; }
.negative { background-color: #2C4770; color: #FFF; }
</style>
</head>
<body>
<h1>%s</h1>""" % (input, input))
    start = 1 if skipFirst else 0
    for line in fin:
        fhtml.write('<p>')
        for triple in line.rstrip('\n').split(' ')[start:]:
            try:
                word, root, wclass = triple.split('/')
                if root in positiveWords:
                    css = "positive"
                elif root in negativeWords:
                    css = "negative"
                else:
                    css = ""
                fhtml.write('<span class="%s" title="%s">%s</span> ' % (css, triple, word))
                ftxt.write('%s ' % word)
                if wclass not in wordClasses:
                    wordClasses[wclass] = triple
            except:
                print('    skip triple:', triple)
        fhtml.write('</p>\n')
        ftxt.write('\n')
    fhtml.write('''
</body>
</html>''')
    fin.close()
    fhtml.close()
    ftxt.close()

def printWordClasses(output):
    print(output)
    with open(output, 'w') as fout:
        for key, value in wordClasses.items():
            fout.write(value)
            fout.write('\n')

readVocabulary('inputs/positive-words.txt', positiveWords)
readVocabulary('inputs/negative-words.txt', negativeWords)

processArticle('inputs/blender_sentences.txt', 'outputs/blender_sentences.html', 'outputs/blender_sentences.txt', False)
processArticle('inputs/drill_POS.txt',         'outputs/drill_POS.html',         'outputs/drill_POS.txt')
processArticle('inputs/fridge_ann.txt',        'outputs/fridge_ann.html',        'outputs/fridge_ann.txt')
processArticle('inputs/movies_ann.txt',        'outputs/movies_ann.html',        'outputs/movies_ann.txt')
processArticle('inputs/vacuum_ann.txt',        'outputs/vacuum_ann.html',        'outputs/vacuum_ann.txt')
processArticle('inputs/washer_sentences.txt',  'outputs/washer_sentences.html',  'outputs/washer_sentences.txt', False)

printWordClasses('outputs/word_class.txt')