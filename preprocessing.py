import re
from re import sub
from unicodedata import normalize, category

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import RSLPStemmer

PT_STOPWORDS = (set(stopwords.words('portuguese')) - {'não'}).union({'vc', 'etc'})
PT_NEG_WORDS = {'não', 'nenhum', 'jamais', 'nada', 'nunca', 'nem', 'ninguém', 'n', 'num'}
open_classes = {'NOUN', 'VERB', 'ADJ', 'ADV'}


def money_conversion(text):
    text = re.sub('R\$ ', 'R$', text)
    pattern = re.compile(r"R\$[1-9]\d{0,2}(?:\.\d{3})*,\d{2}")

    return pattern.sub('brl_value', text)


def percentage_conversion(text):
    pattern = re.compile(r"(\d+(\.\d+)?%)")

    return pattern.sub('percentage_value', text)


def is_number(token):
    return_value = True
    for char in token:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.']:
            return_value = False
            break
    return return_value


def is_portion(token):
    return_value = True
    for char in token:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x']:
            return_value = False
            break
    return return_value


def from_text_to_word_list(raw_text):
    return word_tokenize(raw_text, language='portuguese')


def word_tokenizee(raw_text):
    return word_tokenize(raw_text, language='portuguese')


def sentence_tokenize(raw_text):
    return sent_tokenize(raw_text, language='portuguese')


def from_word_list_to_text(word_list):
    return ' '.join(word_list)


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def stem_words(word_list):
    stemmer = RSLPStemmer()
    return [stemmer.stem(word) for word in word_list]


def lowercase(raw_text):
    return raw_text.lower()


def strip_accents(raw_text):
    return ''.join(
        c for c in normalize('NFD', raw_text) if category(c) != 'Mn'
    )


def only_alpha_numeric(raw_text):
    text = sub('\s+', ' ', raw_text).strip()
    return sub('[^a-z0-9áéíóúâêôãõàèìòùç]', ' ', text)


def remove_stopwords(word_list):
    return [w for w in word_list if w not in set(PT_STOPWORDS)]


def remove_symbols(word_list):
    return [w for w in word_list if w.isalpha()]


def preprocess(raw_text, options):
    text = raw_text
    lower = options.get('lower', True)
    only_alphan = options.get('only_alphan', True)

    strip_acc = options.get('strip_acc', True)

    st_or_lmm = options.get('st_or_lmm', 'st')
    stopws = options.get('stopws', False)

    if lower:
        text = lowercase(text)

    if strip_acc:
        text = strip_accents(text)

    if only_alphan:
        text = only_alpha_numeric(text)

    word_list = from_text_to_word_list(text)

    if st_or_lmm == 'st':
        word_list = stem_words(word_list)
    else:
        pass

    if stopws:
        word_list = remove_stopwords(word_list)

    return word_list
