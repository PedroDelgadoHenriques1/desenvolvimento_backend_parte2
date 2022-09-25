import re
from re import sub
from unicodedata import normalize, category

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import RSLPStemmer

PT_STOPWORDS = (set(stopwords.words('portuguese')) - {'não'}).union({'vc', 'etc'})
PT_NEG_WORDS = {'não', 'nenhum', 'jamais', 'nada', 'nunca', 'nem', 'ninguém', 'n', 'num'}
open_classes = {'NOUN', 'VERB', 'ADJ', 'ADV'}


# TODO improvement: improve chain of function calls (how to make it more pythonic?)
def preprocess_text(text):
    text = money_conversion(text)
    text = percentage_conversion(text)
    text = lowercase(text)
    text = strip_accents(text)
    tokens = word_tokenizee(text)

    revised_tokens = []
    for token in tokens:
        output_token = ''

        if token == '.' or token == ',':
            continue

        if is_number(token):
            output_token = 'number_value'
        else:
            if '/' in token:
                output_token = 'date_value'
            else:
                if is_portion(token):
                    output_token = 'portion_value'

        if output_token == '':
            output_token = token

        revised_tokens.append(output_token)

    return from_word_list_to_text(revised_tokens)


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

