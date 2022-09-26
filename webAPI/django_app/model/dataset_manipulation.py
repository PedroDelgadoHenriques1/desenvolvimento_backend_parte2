import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer

from django_app.model.preprocessing import preprocess_text
from sklearn.svm import LinearSVC
from skmultilearn.problem_transform import LabelPowerset


class DatasetManipulation:

    def __init__(self, csv_path):
        self.vectorizer = TfidfVectorizer()
        self.df = pd.read_csv(csv_path)
        self.clean_categories = [sample_categories.split(',') for sample_categories in list(self.df['category'])]
        self.label_binarizer = MultiLabelBinarizer()
        self.transformed_labels = self.label_binarizer.fit_transform(self.clean_categories)
        self.model = LabelPowerset(LinearSVC())

    @property
    def labels_and_numbers(self):
        labels_and_numbers = dict()
        for idx, label in enumerate(self.label_binarizer.classes_):
            labels_and_numbers[label] = idx
        return labels_and_numbers

    @property
    def cleaned_corpus(self):
        return [preprocess_text(sample) for sample in list(self.df['sentence'])]

    @property
    def features(self):
        return self.vectorizer.fit_transform(self.cleaned_corpus)

    def train(self):
        self.model.fit(self.features, self.transformed_labels)

    def predict(self, sentence):
        cleaned_sentence = preprocess_text(sentence)
        features = self.vectorizer.transform([cleaned_sentence])
        predicted_classes = self.model.predict(features).rows[0]
        return_list = []
        for i in range(0, 5):
            if i in predicted_classes:
                return_list.append(1)
            else:
                return_list.append(0)
        return return_list
