import sgt
from sgt import SGT
import numpy as np


def embedding(data):
    '''
    Do the embedding every day and send to the server
    '''
    alphabets = range(-1, 157)
    sgt = SGT(alphabets=alphabets, flatten=True)
    vector = sgt.fit(data)
    return vector


patient_data = np.load('./test_data/patient.npy')
patient_embedding = []
for each_day in patient_data:
    patient_embedding.append(embedding(each_day))
np.save('./test_data/converted.npy', patient_embedding)
