import pickle

sentence = 'na sala de aula os professores ensinam o conteúdo'

trained_DM = pickle.load(open("webAPI/django_app/model/trained_DM.pkl", "rb"))
prediction = trained_DM.predict(sentence)
print(prediction)
