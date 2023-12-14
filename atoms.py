import pandas as pd
class Atoms:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.filter_dataset = pd.DataFrame()

    #фильтр Rsd
    def filter_Rsd(self, Rsd_min):
        ZA_ = self.dataset[self.dataset['Name'] == 'ZA']
        self.filter_dataset = pd.concat([self.dataset.loc[:ZA_.index[0] - 1], ZA_[ZA_['Rsd'] > Rsd_min]])

    #Статистика