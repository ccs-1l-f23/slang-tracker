# slang-tracking

## Goal: Track the growth and decline of slang usage on online forums.
- Rankings of currently popular slang words relative to each other.
- Information regarding recent growth/decline (similar to Billboard Top 100)

- Ex. abbreviations/acronyms like "ikr", "tbh", "lol"
- Ex. sense shift like "bet", "flex", "down", "goat"
- Slang phrases containing multiple tokens are purposefully out of scope

- Feature idea: Predict the future growth/decline of a given word.
- Feature idea: Explain the definition of nonstandard words/phrases
    - [Ni and Wang, 2017](https://aclanthology.org/I17-2070.pdf) describe an approach in this vein

### Subtask 1: Given a piece of text, identify tokens that fit the definition of slang.
- Approach 1: Manual identification/annotation
- Approach 2: Query slang dictionaries ([GDoS](https://greensdictofslang.com/), Urban Dictionary)
- Approach 3: Automatic identification
    - Learning-based approaches that use sentence context (good for sense shift)
        - [Pei et al., 2019](https://aclanthology.org/K19-1082.pdf)
    - TF-IDF against newspaper articles (not great for sense shift)
    - Or simply filter out tokens that are also found in newspapers
        - [Stewart and Eisenstein, 2018](https://aclanthology.org/D18-1467.pdf) mention that words that can be plausibly found in a newspaper could be considered "standard"
            - They reference Dumas and Lighter, 1978

### Subtask 2: Given a set of tokens and a body of text, determine the relative frequency of each.
- If TF-IDF is used in previous step, relative frequency is already found.
- Otherwise, compare normalized frequencies of the given tokens.

### Subtask 3: Given a token and its frequency history, determine if it is in growth or decline.
- This is a two-variable statistical problem: Is there a correlation between frequency and time?
    - This is the meat of the paper from [Stewart and Eisenstein, 2018](https://aclanthology.org/D18-1467.pdf)
        - Spearman Correlation Coefficient (growth)
        - Logistic fit and piecewise (decline)
    - [Tredici and Fernandez, 2018](https://aclanthology.org/C18-1135.pdf) mention a "contagion model"

### Subtask 4: Acquire and normalize data from real-time online forums
- Data should be timestamped sentences or fragments
- Reddit comments and posts (no longer real-time after API update)
    - [Stewart and Eisenstein, 2018](https://aclanthology.org/D18-1467.pdf) do exactly this
    - Public large-scale datasets have been posted online for download
- Other options: Twitter (posts), Instagram (comments, captions), Tiktok (comments, captions), Youtube (comments)
- Perform normalization (tokenization, segmentation, lemmatization(?))

### Subtask 5: Put it all together
- Feed random samples of data to Subtask 1 to identify slang tokens
- For data from various time intervals, feed slang tokens and data to Subtask 2
- Using each token and its frequency history, perform statistics to determine growth/decline