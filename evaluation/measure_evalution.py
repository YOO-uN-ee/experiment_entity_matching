import polars as pl
from sklearn.metrics import f1_score, precision_score, recall_score

# Metrics commonly used to measure entity matching accuracy: F1, precision, recall
# The pairs in the sample as "matched" / "no-matched"
def calculate_f1_score(ground_truth:list, prediction:list) -> float:
    return f1_score(ground_truth, prediction, average='weighted')

def calculate_precision_score(ground_truth:list, prediction:list) -> float:
    return precision_score(ground_truth, prediction, average='weighted')

def calculate_recall_score(ground_truth:list, prediction:list) -> float:
    return recall_score(ground_truth, prediction, average='weighted')

def return_evalution_scores(ground_truth, prediction, method_name:str) -> list:
    if not isinstance(ground_truth, list):
        ground_truth = ground_truth['label'].to_list()
    if not isinstance(prediction, list):
        prediction = prediction['label'].to_list()

    f1_score = calculate_f1_score(ground_truth, prediction)
    precision = calculate_precision_score(ground_truth, prediction)
    recall = calculate_recall_score(ground_truth, prediction)

    return [method_name, f1_score, precision, recall]