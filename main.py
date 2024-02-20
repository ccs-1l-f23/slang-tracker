import nltk
from nltk.corpus import brown
from nltk.corpus import words
from nltk.corpus import reuters
from nltk.probability import FreqDist
from nltk.tokenize import WhitespaceTokenizer 
import string
import re
import contractions
import glob

# Download the necessary resources
nltk.download('brown')
nltk.download('words')
nltk.download('reuters')

def readFromFiles(files):
    text = ""
    for file in files:
        with open(file, 'r') as file_text:
            text += file_text.read()
    return text

def cleanText(text):
    # Remove emojis
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove punctuation except apostrophe
    # text = text.translate(str.maketrans('', '', string.punctuation.replace("'", "")))
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

    # Normalize the text using Whitespace Tokenization (not Penn Treebank b/c contractions)
    tk = WhitespaceTokenizer()
    tokens = tk.tokenize(text.lower())

    # Expand contractions
    # This might be problematic, removes "gonna", "yall", "kinda" - these are words that could be slang
    output = []
    for token in tokens:
        token = contractions.fix(token)
        output += token.split(" ")
    tokens = output

    # Remove contractions for now
    # tokens = [word for word in tokens if "'" not in word]

    # lemmatize the tokens using WordNet, a database of semantic relations
    wnl = nltk.stem.WordNetLemmatizer()
    output = []
    for word in tokens:
        output.append(wnl.lemmatize(word))
    tokens = output

    return tokens

# Prepare SCOWL Corpus
files = ['texts/corpora/scowl.txt']
scowl = readFromFiles(files)
scowl = scowl.split("\n")

# Concatenate, lowcase, and set-ify the corpora for faster lookup
vocab = set([word.lower() for word in reuters.words() + words.words() + brown.words() + scowl])

def frequencyOfSlang(files):
    # Read the text from the files
    text = readFromFiles(files)

    # Clean the text
    tokens = cleanText(text)

    # Remove English words
    filtered_tokens = [token for token in tokens if token not in vocab]

    # Create a frequency distribution of the words
    fd = FreqDist(filtered_tokens)

    # Normalize frequency distribution
    for word in fd:
        fd[word] = fd[word] / len(tokens)
    
    return fd

# if __name__ == "__main__":
    # Read the text from the files
    # files = ['texts/reddit/berkeley.txt', 'texts/reddit/UCDavis.txt', 'texts/reddit/UCI.txt', 'texts/reddit/ucla.txt', 'texts/reddit/UCSD.txt', 'texts/reddit/UCSantaBarbara.txt', 'texts/reddit/UCSC.txt', 'texts/reddit/UCMerced.txt', 'texts/reddit/UCR.txt']
    # files = ['texts/shakespeare/hamlet.txt', 'texts/shakespeare/romeoandjuliet.txt', 'texts/shakespeare/macbeth.txt']
    # files = ['texts/books/clockworkorange.txt', 'texts/books/cuckoosnest.txt', 'texts/books/maninhighcastle.txt', 'texts/books/wrinkleintime.txt']
    # files = ['texts/clockworkorange/chapter1.txt']
    # fd = frequencyOfSlang(files)
    
    # print(fd.tabulate(5))

if __name__ == '__main__':
    files = glob.glob("./texts/clockworkorange/*")

    # sort by name
    files.sort()

    timeSeries = {}
    for i in range(len(files)):
        fd = frequencyOfSlang([files[i]])

        for word in fd:
            if word in timeSeries:
                timeSeries[word].append(fd[word])
            else:
                timeSeries[word] = [0] * i + [fd[word]]
        
        for word in timeSeries:
            if word not in fd:
                timeSeries[word].append(0)

    fd = frequencyOfSlang(files)
    for common in fd.most_common(10):
        print(common[0], timeSeries[common[0]])