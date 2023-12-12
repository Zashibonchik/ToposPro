import pandas as pd
class Adjacency_matrix:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.filter_dataset = pd.DataFrame()
