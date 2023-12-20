import pandas as pd
class Adjacency_matrix:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.filter_dataset = pd.DataFrame(columns=dataset.columns)

    def filter_Rsd(self, voids):
        #Atom1
        try:
            index_ = self.dataset[self.dataset['Atom1'] == 'ZA1'].index[0] - 1
        except:
            raise AttributeError("В матрице смежности отсутствуют пустоты") from None
        if not voids.empty:
            #если существуют пустоты
            ZA_ = self.dataset[self.dataset['Atom1'].apply(lambda x: x in list(voids))]
            self.filter_dataset = pd.concat([self.dataset.loc[:index_],
                                            ZA_])
        else:
            self.filter_dataset = self.dataset.loc[:index_]
        #Atom2
        names_uniq = self.filter_dataset['Atom1'].unique()
        self.filter_dataset = self.filter_dataset[self.filter_dataset['Atom2'].apply(lambda x: x in names_uniq)]

    def filter_Rad(self, bond):
        ZA_ = self.filter_dataset[self.filter_dataset['Atom1'].apply(lambda x: 'ZA' in x)]
        if not ZA_.empty:
            """Если пустой DF булево индексировать, то он удаляет столбцы"""
            ZA_ = ZA_[ZA_['Atom2'].apply(lambda x: 'ZA' in x)]
        self.filter_dataset.drop(ZA_[ZA_['SSeg'] < str(bond)].index, axis=0, inplace=True)

    def filter_CN(self):
        ZA_ = self.filter_dataset[self.filter_dataset['Atom1'].apply(lambda x: 'ZA' in x)]
        for elem in ZA_['Atom1'].unique():
            ZA_solo_ = self.filter_dataset[self.filter_dataset['Atom1'] == elem]
            ZA_solo_with_ZA_ = ZA_solo_[ZA_solo_['Atom2'].apply(lambda x: 'ZA' in x)]
            ZA_solo_with_ZA_ = ZA_solo_with_ZA_['Type'] != ''
            if ZA_solo_with_ZA_.sum() < 2:
                self.filter_dataset.drop(ZA_solo_.index, inplace=True)



