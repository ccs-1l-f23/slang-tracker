# Adapted from https://github.com/jadessechan/Text-Prediction/blob/master/main.py

import unicodedata
import string
import re
import nltk
from nltk.probability import *
import random
nltk.download('punkt')
nltk.download('wordnet')

def filter_text(text):
    # Unicode text normalization according to the NFKD standard
    # url: https://en.wikipedia.org/wiki/Unicode_equivalence
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # Remove all punctuation
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    print("Remove punctuation: \n%s\n" % text)

    # Only alphabet
    text = re.sub('[^a-zA-Z]', ' ', text)
    print("No numerals: \n%s\n" % text)

    # Lowercase
    text = text.lower()
    print("Lowercase: \n%s\n" % text)

    # add line markers
    # text = text.replace('\n', '<\s>\n<s>')
    # print("Add line markers: \n%s\n" % text)

    # Split and rejoin
    text = ' '.join(text.split())
    print("Split and rejoin: \n%s\n" % text)

    return text

def tokenize_lemmatize(text):
    # tokenize using Penn Treebank Tokenizer
    # tokenization is the process of segmenting words
    # challenging because have to deal with punctuation, contractions, etc.
    # Penn Treebank separates punctuation, contractions, etc. into separate tokens
    # in this case, tokenization isn't doing much because punctuation already removed
    tokens = nltk.word_tokenize(text)
    print("Tokenized: \n%s\n" % tokens)

    # lemmatize the tokens using WordNet, a database of semantic relations
    # lemmatization is the process of reducing words to their base or root form
    # hopefully lower number of unique tokens
    wnl = nltk.stem.WordNetLemmatizer()
    output = []
    for word in tokens:
        output.append(wnl.lemmatize(word))
    print("Lemmatized: \n%s\n" % output)

    return output

# Build trigram model
def create_model(trigrams):
    cfdist = ConditionalFreqDist()
    for w1, w2, w3 in trigrams:
        cfdist[(w1, w2)][w3] += 1

    # transform frequencies to probabilities
    for w1_w2 in cfdist:
        total_count = float(sum(cfdist[w1_w2].values()))
        for w3 in cfdist[w1_w2]:
            cfdist[w1_w2][w3] /= total_count

    return cfdist

def predict(model, user_input):
    user_input = user_input.split()

    w1 = len(user_input) - 2
    w2 = len(user_input)
    prev_words = user_input[w1:w2]

    # display prediction from highest to lowest maximum likelihood
    prediction = sorted(dict(model[prev_words[0], prev_words[1]]), key=lambda x: dict(model[prev_words[0], prev_words[1]])[x], reverse=True)
    # print("Trigram model predictions: ", prediction)

    word = []
    weight = []
    for key, prob in dict(model[prev_words[0], prev_words[1]]).items():
        word.append(key)
        weight.append(prob)
    
    # pick from a weighted random probability of predictions
    next_word = random.choices(word, weights=weight, k=1)
    
    # add predicted word to user input
    user_input.append(next_word[0])
    print(' '.join(user_input))

    # ask = input("Do you want to generate another word? (type 'y' for yes or 'n' for no): ")
    ask = input()
    predict(model, ' '.join(user_input))

# Read the text from the files
# files = ['texts/reddit/berkeley.txt', 'texts/reddit/UCDavis.txt', 'texts/reddit/UCI.txt', 'texts/reddit/ucla.txt', 'texts/reddit/UCSD.txt', 'texts/reddit/UCSantaBarbara.txt', 'texts/reddit/UCSC.txt', 'texts/reddit/UCMerced.txt', 'texts/reddit/UCR.txt']
files = ['texts/shakespeare/hamlet.txt', 'texts/shakespeare/romeoandjuliet.txt', 'texts/shakespeare/macbeth.txt']
# files = ['texts/inaugural_addresses/adams.txt', 'texts/inaugural_addresses/biden.txt', 'texts/inaugural_addresses/washington.txt']
# files = ['texts/shakespeare/hamlet.txt']
text = ""
for file in files:
    file = open(file, 'r')
    while True:
        line = file.readline()
        text += line
        if not line:
            break
    file.close()

# Take a couple lines [104:116] seem to be good
text = '\n'.join(text.split('\n'))
# text = '\n'.join(text.split('\n')[104:116])

print("Raw: \n%s\n" % text)
text = filter_text(text)
words = tokenize_lemmatize(text)

bigrams = list(nltk.ngrams(words, 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))
trigrams = list(nltk.ngrams(words, 3, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))
# print(trigrams)

# N-gram Statistics
# get freq dist of trigrams
freq_tri = nltk.FreqDist(trigrams)
freq_bi = nltk.FreqDist(bigrams)
# freq_tri.plot(30, cumulative=False)
print("Most common trigrams: \n%s\n" % freq_tri.most_common(5))
print("Most common bigrams: \n%s\n" % freq_bi.most_common(5))

model = create_model(trigrams)
predict(model, input())