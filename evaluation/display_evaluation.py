import pickle
import configparser

from tabulate import tabulate
from evaluation.measure_evalution import *

config = configparser.ConfigParser()

def display_evalution_result(pl_prediction, method_name:str):
    pl_ground_truth = pl.read_csv('/home/yaoyi/pyo00005/Entity_Matching/data')

    table = []
    with open('/home/yaoyi/pyo00005/Entity_Matching/results/result.pkl', 'rb') as handle:
        table.append(pickle.load(handle))

    table.append(return_evalution_scores(pl_ground_truth, pl_prediction, method_name))

    headers = ['Method', 'F1-Score', 'Precision', 'Recall']
    
    print(tabulate(table, headers, tablefmt='grid'))