import pickle
from evaluation.measure_evalution import *
import matplotlib.pyplot as plt

with open('./groundtruth.pkl', 'rb') as handle:
    list_groundtruth = pickle.load(handle)

print(len(list_groundtruth))
with open('./predictions.pkl', 'rb') as handle:
    list_prediction = pickle.load(handle)

print(return_evalution_scores(list_groundtruth, list_prediction, 'llama'))

# print(len(list_groundtruth))

# with open('./groundtruth_gpt.pkl', 'rb') as handle:
#     list_groundtruth = pickle.load(handle)

# with open('./matches_gpt.pkl', 'rb') as handle:
#     list_prediction = pickle.load(handle)

# print(list(set(list_prediction) - set(list_groundtruth)))

# print(return_evalution_scores(list_groundtruth, list_prediction, 'gpt'))

############################



with open('./combination_dict.pkl', 'rb') as handle:
    dict_combination = pickle.load(handle)

with open('./elapsed_time.pkl', 'rb') as handle:
    list_elapsed_time_llama = pickle.load(handle)

with open('./elapsed_time_gpt.pkl', 'rb') as handle:
    list_elapsed_time_gpt = pickle.load(handle)

dict_time_llama = dict(zip(list_elapsed_time_llama[0], list_elapsed_time_llama[1]))
dict_time_gpt = dict(zip(list_elapsed_time_gpt[0], list_elapsed_time_gpt[1]))

list_time_analysis = [[0], [0], [0]]

for k in list(dict_time_gpt.keys()):
    try:
        row_count = dict_combination[k]
        time_value_llama = dict_time_llama[k]
        time_value_gpt = dict_time_gpt[k]

        list_time_analysis[0].append(row_count)
        list_time_analysis[1].append(time_value_llama)
        list_time_analysis[2].append(time_value_gpt)
    except:
        pass

list_time_analysis[0] = list_time_analysis[0][:135]
list_time_analysis[1] = list_time_analysis[1][:135]
list_time_analysis[2] = list_time_analysis[2][:135]

# with open('./modified_time_gpt_analysis.pkl', 'wb') as handle:
#     pickle.dump(list_time_analysis, handle, protocol=pickle.HIGHEST_PROTOCOL)

plt.plot(list_time_analysis[0], list_time_analysis[1], 'o-r')
plt.plot(list_time_analysis[0], list_time_analysis[2], 'o-b')
plt.savefig('./modified_time_total.png')

print(list_time_analysis[0][73])
print(list_time_analysis[1][73])
print(list_time_analysis[2][73])