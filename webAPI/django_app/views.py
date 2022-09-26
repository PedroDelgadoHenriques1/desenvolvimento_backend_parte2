import os
import pickle

from django.http import JsonResponse

from rest_framework.decorators import api_view

from django_app.model.dataset_manipulation import DatasetManipulation


def train_model(request):
    dm = DatasetManipulation("django_app/model/dataset.csv")

    dm.train()

    pickle.dump(dm, open("django_app/model/trained_DM.pkl", "wb"))
    print("train completed")


@api_view(['GET', 'POST'])
def classify_sentence(request):
    if request.method == 'POST':
        sentence = request.data.get('sentence', None)
        print(sentence)

        # print(os.path.abspath(os.getcwd()))
        # import sys
        # sys.path.append(os.path.abspath(os.getcwd()) + 'django_app/model/')
        trained_DM = pickle.load(open("django_app/model/trained_DM.pkl", "rb"))
        prediction = trained_DM.predict(sentence)
        classification_list = prediction[0]

        print(classification_list)
        # classification_list = [1, 0, 1, 0, 1]

        response = {
            'financas': int(classification_list[trained_DM.labels_and_numbers['finanças']]),
            'educacao': int(classification_list[trained_DM.labels_and_numbers['educação']]),
            'industrias': int(classification_list[trained_DM.labels_and_numbers['indústrias']]),
            'varejo': int(classification_list[trained_DM.labels_and_numbers['varejo']]),
            'orgao_publico': int(classification_list[trained_DM.labels_and_numbers['orgão público']]),
        }

        return JsonResponse(response)
