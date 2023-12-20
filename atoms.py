import pandas as pd
class Atoms:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.filter_dataset = pd.DataFrame(columns=dataset.columns)

    #фильтр Rsd
    def filter_Rsd(self, Rsd_min):
        ZA_ = self.dataset[self.dataset['Name'] == 'ZA']
        self.filter_dataset = pd.concat([self.dataset.loc[:ZA_.index[0] - 1], ZA_[ZA_['Rsd'] > Rsd_min]])

    #удаление элементов
    def drop_elems(self, list_elem):
        for name, num in zip(self.filter_dataset['Name'], self.filter_dataset['Num']):
            if name + num not in list_elem:
                drop_ = self.filter_dataset[self.filter_dataset['Name'] == name]
                drop_ = drop_[drop_['Num'] == num]
                self.filter_dataset.drop(drop_.index, axis=0, inplace=True)


    #Статистика
    def statistics_Rsd(self):
        ZA_ = self.filter_dataset[self.filter_dataset['Name']== 'ZA']
        min_Rsd, max_Rsd = ZA_['Rsd'].min()
