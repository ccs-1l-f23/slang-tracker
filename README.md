# slang-tracking

## Goal: Track the growth and decline of slang usage on online forums.
- Rankings of currently popular slang words relative to each other.
- Information regarding recent growth/decline (similar to Billboard Top 100)

- Read more [here](https://docs.google.com/document/d/1kXFS8nniL8kICFqFjQzA3XOBMj9tsrYLD_1oXKTfyFc/edit?usp=sharing)

### Corpora
#### [NLTK Data](https://www.nltk.org/nltk_data/)
- (65) Word Lists (id: words) is the UNIX words list
- (74) Stopwords Corpus (id: stopwords) are a good list of stopwords
- (93) The Reuters-21578 benchmark corpus (id: reuters) which is good for newspaper
- (102) Brown Corpus (id: brown)

#### [SCOWL](http://wordlist.aspell.net/)
- en_US defaults

#### [Word frequency data](https://www.wordfrequency.info/)
- Could be useful for filtering out common words
- But I think you have to pay for anything more than samples

#### [English-Corpora.org](https://www.english-corpora.org/)
- This is the holy grail but requires payment :(

#### [Google Books N-grams](https://storage.googleapis.com/books/ngrams/books/datasetsv2.html)
- Haven't looked into using this but could be great

#### In total
- reuters + brown + words + scowl seems to catch most words that I want to remove

### Directories
- slp/
    - My exploration of some NLP techniques from Speech and Language Processing (Jurafsky and Martin)
- texts/
    - Various resources that are useful for slp/ and main.py