import pickle


from webAPI.django_app.model.dataset_manipulation import DatasetManipulation

dm = DatasetManipulation("webAPI/django_app/model/dataset.csv")

dm.train()

pickle.dump(dm, open("webAPI/django_app/model/trained_DM.pkl", "wb"))
