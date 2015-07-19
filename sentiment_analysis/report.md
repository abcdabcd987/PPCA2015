## A Naïve Try

### Naïve Model

We defined the sentiment value \\(sw_{j}\\) of a word \\(j\\) as a real number in \\([-1, 1]\\). The closer to \\(1\\) \\(se_w\\) is, the more positive the word is, and similarily, \\(-1\\) for the most negative and \\(0\\) for the neutral. Since we are given two vocabularies of positive words and negative words in standard context, we initially set the sentiment values to \\(1\\) for positive ones and \\(-1\\) for negative ones.

We treated a sentence as a sequence of words, hence we defined the sentiment value \\(ss_{i}\\) of a sentence \\(i\\) as

\\[
ss_i = \frac{1}{cnt_i}\sum_{j} sw'_{j}
\\]

where \\(cnt_i\\) is the number of words which are in the vocabulary and \\(j\\) is a word of the sentence which is in the vocabulary.

We took negations into account. Whenever a *not* appears, sentiment values of the words after it will be opposite, while double *not*s cancel this effect. Hence, the \\(sw'_{j}\\) means the sentiment value of word \\(j\\) with negations considered.

After we got the sentiment value of each sentence, we used it to update the sentiment value of each word. The new sentiment value \\(sw''_{j}\\) for word \\(j\\) is

\\[
sw''_j = \frac{1}{appear_j}\sum_{i} ss_{i}
\\]

where \\(appear_j\\) is the number of sentences which include word \\(j\\) and \\(i\\) is a sentence which has word \\(j\\) included.

We repeated the operations above, iterating for several times.

### Result and Analysis

We first noticed that as the number of iteration times increase, the sentiment value of each word converges at \\(0\\). This is easy to explain, for it always holds that

\\[
\left| ss_i \right| \leq \max_j{\left| sw_j \right|}
\\]

Therefore, iteration is meaningless here.

Besides that, the result of this naïve model is also quite disappointing. One of the most hugely sentiment-changed words is *plight* which is in the nagative vocabulary and is regared as a positive one in this model. However, the only sentence that includes *plight* is *LG does not care about the customer or their plight.* in which *plight* does have negative sentiment.