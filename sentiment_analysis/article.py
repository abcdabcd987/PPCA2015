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


def processArticle(input, output, skipFirst=True):
    print(output)
    fin = open(input, 'r')
    fout = open(output, 'w')
    fout.write("""
<!DOCTYPE html>
<html>
<head>
<title>%s</title>
<meta charset="utf-8">
<link href='http://fonts.useso.com/css?family=Vollkorn' rel='stylesheet' type='text/css'>
<style type="text/css">
p {
    font-family: Vollkorn, serif;
    line-height: 1.25em;
    margin: 0.2em 0;
}

.positive { background-color: #AA3939; color: #FFF; }
.negative { background-color: #2C4770; color: #FFF; }
</style>
</head>
<body>
<h1>%s</h1>""" % (input, input))
    start = 1 if skipFirst else 0
    for line in fin:
        fout.write('<p>')
        for triple in line.rstrip('\n').split(' ')[start:]:
            try:
                word, root, wclass = triple.split('/')
                if root in positiveWords:
                    css = "positive"
                elif root in negativeWords:
                    css = "negative"
                else:
                    css = ""
                fout.write('<span class="%s" title="%s">%s</span> ' % (css, triple, word))
                if wclass not in wordClasses:
                    wordClasses[wclass] = triple
            except:
                print('    skip triple:', triple)
        fout.write('</p>\n')
    fout.write('''
</body>
</html>''')
    fin.close()
    fout.close()

def printWordClasses(output):
    print(output)
    with open(output, 'w') as fout:
        for key, value in wordClasses.items():
            fout.write(value)
            fout.write('\n')

readVocabulary('inputs/positive-words.txt', positiveWords)
readVocabulary('inputs/negative-words.txt', negativeWords)

processArticle('inputs/blender_sentences.txt', 'outputs/blender_sentences.html', False)
processArticle('inputs/drill_POS.txt', 'outputs/drill_POS.html')
processArticle('inputs/fridge_ann.txt', 'outputs/fridge_ann.html')
processArticle('inputs/movies_ann.txt', 'outputs/movies_ann.html')
processArticle('inputs/vacuum_ann.txt', 'outputs/vacuum_ann.html')
processArticle('inputs/washer_sentences.txt', 'outputs/washer_sentences.html', False)

printWordClasses('outputs/word_class.txt')