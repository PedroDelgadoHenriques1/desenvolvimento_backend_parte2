import pickle

from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework.decorators import api_view

from django_app.model.dataset_manipulation import DatasetManipulation


def train_model(request):
    dm = DatasetManipulation("django_app/model/dataset.csv")

    dm.train()

    pickle.dump(dm, open("django_app/model/trained_DM.pkl", "wb"))

    return redirect('classify_sentence')


@api_view(['POST'])
def classify_sentence(request):
    if request.method == 'POST':
        sentence = request.data.get('sentence', None)

        trained_DM = pickle.load(open("django_app/model/trained_DM.pkl", "rb"))
        classification_list = trained_DM.predict(sentence)

        response = {
            'financas': int(classification_list[trained_DM.labels_and_numbers['finanças']]),
            'educacao': int(classification_list[trained_DM.labels_and_numbers['educação']]),
            'industrias': int(classification_list[trained_DM.labels_and_numbers['indústrias']]),
            'varejo': int(classification_list[trained_DM.labels_and_numbers['varejo']]),
            'orgao_publico': int(classification_list[trained_DM.labels_and_numbers['orgão público']]),
        }

        return JsonResponse(response)
