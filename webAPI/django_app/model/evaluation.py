import pandas as pd
from sklearn.ensemble import BaggingClassifier, GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from skmultilearn.problem_transform import LabelPowerset

import webAPI.django_app.model.preprocessing as pp


approaches = {
    # Problem Adaption
    'knn': KNeighborsClassifier(),
    'random_forest': RandomForestClassifier(n_jobs=-1),
    # Problem Transformation: Binary Relevance
    'bagging': OneVsRestClassifier(BaggingClassifier(n_jobs=-1)),
    'gradient_boosting': OneVsRestClassifier(GradientBoostingClassifier()),
    'naive_bayes': OneVsRestClassifier(MultinomialNB()),
    'linear_SVM': OneVsRestClassifier(LinearSVC(), n_jobs=-1),
    # Problem Transformation: Label PowerSet
    'LP_bagging': LabelPowerset(BaggingClassifier(n_jobs=-1)),
    'LP_gradient_boosting': LabelPowerset(GradientBoostingClassifier()),
    'LP_naive_bayes': LabelPowerset(MultinomialNB()),
    'LP_linear_SVM': LabelPowerset(LinearSVC())
}


df = pd.read_csv("webAPI/django_app/model/dataset.csv")

different_one_or_two_categories = list(set(df['category']))
cleaned_categories = [sample_categories.split(',') for sample_categories in list(df['category'])]

corpus = list(df['sentence'])
cleaned_corpus = [pp.preprocess_text(sample) for sample in corpus]

X_train, X_test, y_train, y_test = train_test_split(cleaned_corpus, cleaned_categories, test_size=0.2, random_state=42)

label_binarizer = MultiLabelBinarizer()
y_train = label_binarizer.fit_transform(y_train)
y_test = label_binarizer.transform(y_test)

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

for approach_name, approach in approaches.items():
    approach.fit(X_train, y_train)
    predictions = approach.predict(X_test)
    score = f1_score(y_test, predictions, average='micro')
    print(f"Approach {approach_name} with f1-score of {score:.3f}")
