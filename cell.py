import pandas as pd
from atoms import Atoms
from adjacency_matrix import Adjacency_matrix
from additional_information import Additional_information
class Cell:
    def __init__(self, atom_dataset, adjacency_matrix, additional_information, name_db):
        """
        :param atom_dataset: type - , информация об атомах структуры (название, координаты и тд)
        :param adjacency_matrix: type - , матрица смежности
        :param additional_information: type - , доп параметры, идущие после МС
        :param name_db: type - str, название файла
        """
        self.atom_dataset = atom_dataset
        self.adjacency_matrix = adjacency_matrix
        self.additional_information = additional_information
        self.name_db = self.additional_information.dataset['name']
        self.composition = dict(self.atom_dataset.dataset['Name'].value_counts())

    def __str__(self):
        return self.atom_dataset.dataset

    #фильтр матрицы
    def filter_matrix(self, coef_deformation=10):
        try:
            #Коорд пустот
            ZA_ = self.atom_dataset.filter_dataset[self.atom_dataset.filter_dataset['Name'] == 'ZA']
            #Пустота + ее номер
            ZA_ = ZA_['Name'] + ZA_['Num']
        except:
            raise AttributeError('Не проведена фильтрация радиусов пустот (Rsd)') from None
        #удаление лишних пустот
        self.adjacency_matrix.filter_Rsd(ZA_)





    def in_POSCAR(self, scaling_factor=1):
        """ВЕКТОР ЯЧЕЙКИ"""
        with open('POSCAR_test', 'a') as export:
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
            for index in range(self.atom_dataset.dataset.shape[0]):
                line_ = ''
                for value in self.atom_dataset.dataset[['X','Y','Z']].iloc[index]:
                    line_ += str(value) + ' '
                write_line.append(line_ + '\n')
            export.writelines(write_line)








