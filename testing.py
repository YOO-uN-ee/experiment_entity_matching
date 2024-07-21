import pickle

file_name = '/home/yaoyi/pyo00005/Entity_Matching/results_archive/matches.pkl'

with open(file_name, 'rb') as handle:
    file = pickle.load(handle)

print(file)