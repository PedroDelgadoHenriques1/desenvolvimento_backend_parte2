import pandas as pd
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer

import webAPI.django_app.model.preprocessing as pp


df = pd.read_csv("model/dataset.csv")

different_one_or_two_categories = list(set(df['category']))
clean_categories = [sample_categories.split(',') for sample_categories in list(df['category'])]

label_binarizer = MultiLabelBinarizer()
transformed_labels = label_binarizer.fit_transform(clean_categories)
print(label_binarizer.classes_)

corpus = list(df['sentence'])
cleaned_corpus = [pp.preprocess_text(sample) for sample in corpus]

vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(cleaned_corpus)

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
