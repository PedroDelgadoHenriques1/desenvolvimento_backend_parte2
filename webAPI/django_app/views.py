import pickle

from django.http import JsonResponse

from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def classify_sentence(request):
    if request.method == 'POST':
        sentence = request.data.get('sentence', None)
        print(sentence)

        # trained_DM = pickle.load(open("django_app/trained_DM.pkl", "rb"))
        # prediction = trained_DM.predict(sentence)
        # print(prediction)


    classification_list = [1, 0, 1, 0, 1]
    response = {
        'financas': classification_list[0],
        'educacao': classification_list[1],
        'industrias': classification_list[2],
        'varejo': classification_list[3],
        'orgao_publico': classification_list[4],
    }

    return JsonResponse(response)
