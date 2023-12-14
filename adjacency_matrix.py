import pandas as pd
class Adjacency_matrix:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.filter_dataset = pd.DataFrame()

    def filter_Rsd(self, voids):
        #Atom1
        ZA_ = self.dataset[self.dataset['Atom1'].apply(lambda x: x in list(voids))]
        self.filter_dataset = pd.concat([self.dataset.loc[:ZA_.index[0] - 1],
                                         ZA_])
        #Atom2
        names_uniq = self.filter_dataset['Atom1'].unique()
        self.filter_dataset = self.filter_dataset[self.filter_dataset['Atom2'].apply(lambda x: x in names_uniq)]
