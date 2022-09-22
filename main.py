import pandas as pd
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer

import preprocessing as pp


# TODO improvement: move to preprocessing module and improve chain of function calls
def preprocess_text(text):
    text = pp.money_conversion(text)
    text = pp.percentage_conversion(text)
    text = pp.lowercase(text)
    text = pp.strip_accents(text)
    tokens = pp.word_tokenizee(text)

    revised_tokens = []
    for token in tokens:
        output_token = ''

        if token == '.' or token == ',':
            continue

        if pp.is_number(token):
            output_token = 'number_value'
        else:
            if '/' in token:
                output_token = 'date_value'
            else:
                if pp.is_portion(token):
                    output_token = 'portion_value'

        if output_token == '':
            output_token = token

        revised_tokens.append(output_token)

    return pp.from_word_list_to_text(revised_tokens)


df = pd.read_csv("dataset.csv")

different_one_or_two_categories = list(set(df['category']))
clean_categories = [sample_categories.split(',') for sample_categories in list(df['category'])]

label_binarizer = MultiLabelBinarizer()
transformed_labels = label_binarizer.fit_transform(clean_categories)
print(label_binarizer.classes_)

corpus = list(df['sentence'])

vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(corpus)

X_train, X_test, y_train, y_test = train_test_split(features, transformed_labels, test_size=0.2, random_state=42)

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
knn_y_pred = knn.predict(X_test)

bagClassifier = OneVsRestClassifier(BaggingClassifier(n_jobs=-1))
bagClassifier.fit(X_train, y_train)
bagg_y_pred = bagClassifier.predict(X_test)

rf = RandomForestClassifier(n_jobs=-1)
rf.fit(X_train, y_train)
rf_y_pred = rf.predict(X_test)

print(f1_score(y_test, knn_y_pred, average='micro'))
print(f1_score(y_test, bagg_y_pred, average='micro'))
print(f1_score(y_test, rf_y_pred, average='micro'))
