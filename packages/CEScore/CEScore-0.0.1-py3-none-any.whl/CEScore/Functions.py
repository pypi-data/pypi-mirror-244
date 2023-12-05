import numpy as np
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from functools import lru_cache
import os
from pathlib import Path
PACKAGE_DIR = Path(__file__).resolve().parent
import re
from string import punctuation

@lru_cache(maxsize=1)
def get_stopwords():
    # TODO: #language_specific
    # Inline lazy import because importing nltk is slow
    import nltk
    try:
        return set(nltk.corpus.stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords')
        return set(nltk.corpus.stopwords.words('english'))


@lru_cache(maxsize=1)
def get_word2fameliralty():
    concrete_words_path = os.path.join(PACKAGE_DIR, 'concrete_words.tsv')
    df = pd.read_csv(concrete_words_path, sep='\t')
    df = df[df['Bigram'] == 0]  # Remove bigrams
    return {row['Word']: row['Percent_known'] for _, row in df.iterrows()}

@lru_cache(maxsize=1)
def get_word2Zipf():
    path = os.path.join(PACKAGE_DIR, 'SUBTLEX_US_frequency_list.csv')
    df = pd.read_csv(path, sep=';')
    #df = df[df['Bigram'] == 0]  # Remove bigrams
    return {row['Word']: row['Zipf-value'] for _, row in df.iterrows()}

def get_known(word):
    return get_word2fameliralty().get(word, 0.75) 

def get_Zipf(word):
    return  get_word2Zipf().get(word, 0)

def count_words(text):
    return len(word_tokenize(text))

# Adapted from the following scripts:
#https://github.com/facebookresearch/text-simplification-evaluation/blob/main/tseval/text.py

specialSyllables_en = """tottered 2
chummed 1
peeped 1
moustaches 2
shamefully 3
messieurs 2
satiated 4
sailmaker 4
sheered 1
disinterred 3
propitiatory 6
bepatched 2
particularized 5
caressed 2
trespassed 2
sepulchre 3
flapped 1
hemispheres 3
pencilled 2
motioned 2
poleman 2
slandered 2
sombre 2
etc 4
sidespring 2
mimes 1
effaces 2
mr 2
mrs 2
ms 1
dr 2
st 1
sr 2
jr 2
truckle 2
foamed 1
fringed 2
clattered 2
capered 2
mangroves 2
suavely 2
reclined 2
brutes 1
effaced 2
quivered 2
h'm 1
veriest 3
sententiously 4
deafened 2
manoeuvred 3
unstained 2
gaped 1
stammered 2
shivered 2
discoloured 3
gravesend 2
60 2
lb 1
unexpressed 3
greyish 2
unostentatious 5
"""

fallback_cache = {}

fallback_subsyl = ["cial", "tia", "cius", "cious", "gui", "ion", "iou",
                   "sia$", ".ely$"]

fallback_addsyl = ["ia", "riet", "dien", "iu", "io", "ii",
                   "[aeiouy]bl$", "mbl$",
                   "[aeiou]{3}",
                   "^mc", "ism$",
                   "(.)(?!\\1)([aeiouy])\\2l$",
                   "[^l]llien",
                   "^coad.", "^coag.", "^coal.", "^coax.",
                   "(.)(?!\\1)[gq]ua(.)(?!\\2)[aeiou]",
                   "dnt$"]


# Compile our regular expressions
for i in range(len(fallback_subsyl)):
    fallback_subsyl[i] = re.compile(fallback_subsyl[i])
for i in range(len(fallback_addsyl)):
    fallback_addsyl[i] = re.compile(fallback_addsyl[i])


def _normalize_word(word):
    return word.strip().lower()


# Read our syllable override file and stash that info in the cache
for line in specialSyllables_en.splitlines():
    line = line.strip()
    if line:
        toks = line.split()
        assert len(toks) == 2
        fallback_cache[_normalize_word(toks[0])] = int(toks[1])

@lru_cache(maxsize=100)
def remove_punctuation_tokens(text):
    return ' '.join([w for w in word_tokenize(text) if w not in punctuation ])



def count_syllables_in_word(text):
    word = text.strip().lower()
    if not word:
        return 0

    # Check for a cached syllable count
    count = fallback_cache.get(word, -1)
    if count > 0:
        return count

    # Remove final silent 'e'
    if word[-1] == "e":
        word = word[:-1]

    # Count vowel groups
    count = 0
    prev_was_vowel = 0
    for c in word:
        is_vowel = c in ("a", "e", "i", "o", "u", "y")
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel

    # Add & subtract syllables
    for r in fallback_addsyl:
        if r.search(word):
            count += 1
    for r in fallback_subsyl:
        if r.search(word):
            count -= 1

    # Cache the syllable count
    fallback_cache[word] = count
    if (len(word)>0 and count==0):
       return 1
    return count




def preprocess_text(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    #words = [word for word in words if word not in stop_words]
    return ' '.join(words)

def to_sentences(text, language='english'):
    # Inline lazy import because importing nltk is slow
    import nltk
    tokenizer = nltk.data.load(f'tokenizers/punkt/{language}.pickle')
    return tokenizer.tokenize(text)
