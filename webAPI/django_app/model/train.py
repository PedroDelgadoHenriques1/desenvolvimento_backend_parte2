import pickle
from dataset_manipulation import DatasetManipulation


dm = DatasetManipulation("model/dataset.csv")

dm.train()

pickle.dump(dm, open("../trained_DM.pkl", "wb"))
