import pandas as pd
import os
from atoms import Atoms
from adjacency_matrix import Adjacency_matrix
from additional_information import Additional_information
import matplotlib.pyplot as plt
#отключить ложное предупреждение
pd.options.mode.chained_assignment = None
class Cell:
    def __init__(self, atom_dataset, adjacency_matrix, additional_information,name_db):
        """
        :param atom_dataset: type - Dataframe, информация об атомах структуры (название, координаты и тд)
        :param adjacency_matrix: type - Dataframe, матрица смежности
        :param additional_information: type - Dataframe, доп параметры, идущие после МС
        :param name_db: type - str, название файла
        """
        self.atom_dataset = atom_dataset
        self.adjacency_matrix = adjacency_matrix
        self.additional_information = additional_information
        self.name_db = name_db
        self.composition = dict(self.atom_dataset.dataset['Name'].value_counts())

    def __str__(self):
        return self.atom_dataset.dataset

    #получить уникальные значения Rsd для выбранного элемента
    def Rsd_unique(self, elem):
        Elem_ = self.atom_dataset.dataset[self.atom_dataset.dataset['Name'] == elem]
        return sorted(Elem_['Rsd'].unique())

    #фильтр матрицы
    def filter_matrix(self, elements=['Li', 'O'], coef_deformation=10):
        radii = {'H': 0.400, 'He': 0.700, 'Li': 1.450, 'O': 0.600, 'Mg': 1.500, 'P': 1.000, 'V': 1.350}
        #Коорд пустот
        ZA_ = self.atom_dataset.filter_dataset[self.atom_dataset.filter_dataset['Name'] == 'ZA']
        #Пустота + ее номер
        ZA_ = ZA_['Name'] + ZA_['Num']
        #удаление лишних пустот
        self.adjacency_matrix.filter_Rsd(ZA_)
        #выбор связи
        bond = 0
        for elem in elements:
            bond += radii[elem]
        bond = bond - bond * coef_deformation / 100
        #Удаление связей между пустотами с малыми радиусами
        self.adjacency_matrix.filter_Rad(bond)
        #Удаление пустот с КЧ < 2:
        self.adjacency_matrix.filter_CN()
        #Удаление пустот с atom_dataset
        self.atom_dataset.drop_elems(list_elem=self.adjacency_matrix.filter_dataset['Atom1'].unique())
        #Обновляем инфу про композит
        self.composition = dict(self.atom_dataset.filter_dataset['Name'].value_counts())

    def statistics(self, Rsd_min):
        #Кол-во пустот для данного Rsd
        ZA_values = self.atom_dataset.filter_dataset['Name'].value_counts()['ZA']
        self.additional_information.distribution_Rsd(Rsd_min=Rsd_min, ZA_values=ZA_values)
        #Кол-во каналов для данного Rsd
        #удаление повторов в МС
        """Возможно удаление дубликатов характеризующих одну и ту же пустоты. 
        Например, удалится вторая строка в следующем массиве:
           Atom1 Atom2   SSeg
            ZA2   ZA4  2.100
            ZA2   ZA4  2.100
        Но в следующем массиве удаление не произойдет:
            Atom1 Atom2   SSeg
            ZA2   ZA4  2.099
            ZA2   ZA4  2.100"""
        channel_ZA_values = self.adjacency_matrix.filter_dataset[['Atom1', 'Atom2', 'SSeg']]
        channel_ZA_values = channel_ZA_values[channel_ZA_values['Atom1'].str.contains('ZA') &
                                              channel_ZA_values['Atom2'].str.contains('ZA')]
        tuple_rows_ = {}
        for index, row in channel_ZA_values.iterrows():
            row_ = tuple(sorted(row[['Atom1', 'Atom2']]))
            if row_ in tuple_rows_ and tuple_rows_[row_] == row['SSeg']:
                channel_ZA_values.drop(index, inplace=True)
            else:
                tuple_rows_[row_] = row['SSeg']
        self.additional_information.channel_ZA_values_filter = channel_ZA_values
        self.additional_information.distribution_Rad(Rsd_min=Rsd_min)

    def in_POSCAR(self, path, Rsd, scaling_factor=1):
        name_file = self.name_db.replace('.dat','_') + self.additional_information.dataset['name'].replace(' ','')
        name_file = ''.join(s for s in name_file if s not in '\/:*?"<>|+') + '_Rsd=' + str(Rsd)
        """Добавить Path"""
        if not os.path.isdir('ready'):
            os.mkdir('ready')
            os.mkdir('ready\\POSCAR')
        with open('ready\\POSCAR\\' + name_file, 'a') as export:
            # имя
            write_line = [self.additional_information.dataset['name'] + '\n']
            # фактор скалирования
            write_line.append(str(scaling_factor) + '\n')
            # вектор ячейки
            for zero, parametr in zip(range(3),self.additional_information.dataset[['A','B','C']]):
                parametr = '{} '.format(0.0) * (zero) + parametr + ' {}'.format(0.0) * (2 - zero) + '\n'
                write_line.append(parametr)
            # Список элементов элементов
            """Для сохранения последовательности элементов используем список"""
            atoms_label = self.atom_dataset.dataset['Name'].unique()
            write_line.append(' '.join(atoms_label) + '\n')
            # Количество элементов
            line_ = ''
            for atom in atoms_label:
                line_ += str(self.composition[atom]) + ' '
            write_line.append(line_ + ' \n')
            # Коорд атомов
            for index in range(self.atom_dataset.filter_dataset.shape[0]):
                line_ = ''
                for value in self.atom_dataset.filter_dataset[['X','Y','Z']].iloc[index]:
                    line_ += str(value) + ' '
                write_line.append(line_ + '\n')
            write_line.append('\n')
            export.writelines(write_line)








