import nltk
from nltk.corpus import brown, words, reuters
from nltk.probability import FreqDist
from nltk.tokenize import WhitespaceTokenizer 
import string
import re
import contractions
import glob
import matplotlib.pyplot as plt

nonslang = set()

def fetch_sorted(dir: str) -> list[str]:
    """Fetch and sort filenames from a directory

    Args:
        dir (str): directory to fetch files from

    Returns:
        list[str]: list of sorted filenames
    """
    
    files = glob.glob(dir)
    files.sort()
    return files

def read_file(file: str) -> str:
    """Read and concatenate the text from a file

    Args:
        file (str): the filename to read from

    Returns:
        str: the concatenated text from the file
    """
    text = ""
    with open(file, 'r') as file_text:
        text += file_text.read()
    return text

def read_bucketed(files: list[str], buckets: int = None) -> list[str]:
    """Read timestamped files and bucket them

    Args:
        files (list[str]): list of filenames to read from
        buckets (int): number of buckets to divide the files into
    
    Returns:
        list[str]: list of size `buckets` containing the concatenated text of the files in each bucket
    """
    if buckets is None or buckets > len(files):
        buckets = len(files)

    first = re.findall("/(\d+).txt", files[0])[0]
    last = re.findall("/(\d+).txt", files[-1])[0]

    timerange = int(last) - int(first)
    step = timerange / buckets

    bucketed = [""] * buckets
    for file in files:
        filetime = re.findall("/(\d+).txt", file)[0]
        deltatime = int(filetime) - int(first)

        index = int(deltatime / step)
        index = min(index, buckets - 1)

        bucketed[index] += read_file(file)
    
    return bucketed

def tokenize(text: str) -> list[str]:
    """Normalize, tokenize, and lemmatize the text

    Args:
        text (str): the text to process

    Returns:
        list[str]: list of clean tokens
    """

    # Remove emojis
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove punctuation
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

def slang_frequency(tokens: list[str]) -> FreqDist:
    """Find slang and create a frequency distribution

    Args:
        tokens (list[str]): list of tokens to process

    Returns:
        FreqDist: frequency distribution of the slang
    """
    global nonslang
    if nonslang == set():
        # Prepare SCOWL Corpus
        scowl = read_file('texts/corpora/scowl.txt')
        scowl = scowl.split("\n")

        # Concatenate, lowcase, and set-ify the corpora for faster lookup
        nonslang = set([word.lower() for word in reuters.words() + words.words() + brown.words() + scowl])

    # Filter out non-slang words
    filtered_tokens = [token for token in tokens if token not in nonslang]

    # Create a frequency distribution of the words
    fd = FreqDist(filtered_tokens)

    # Normalize frequency distribution
    for word in fd:
        fd[word] = fd[word] / len(tokens)
    
    return fd

if __name__ == '__main__':
    sources = fetch_sorted("./texts/clockworkorange/*")
    raw = read_bucketed(sources)

    clean = [tokenize(bucket) for bucket in raw]
    frequency_series = [slang_frequency(bucket) for bucket in clean]

    cumulative = FreqDist()
    for bucket in frequency_series:
        cumulative += bucket
    
    for word in cumulative.most_common(5):
        series = []
        for i in range(len(frequency_series)):
            series.append(frequency_series[i][word[0]])
            # print(f"{word[0]}: {frequency_series[i][word[0]]:.4f}", end=" ")
        
        plt.plot(series, label=word[0])
    
    plt.legend(loc='best')
    plt.show()