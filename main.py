import os
from Topos_reading import reading
from cell import Cell
import pandas as pd
"""Не определяется G3!!!"""


pd.set_option('display.max_rows', None)
def wall():
    print('--------------------------------------------')
if __name__ == '__main__':
    # path = input('Введите путь к файлам: ')
    path = 'D:\Py\проекты\ToposPro\check'
    full_cells = reading(path)
    #количество файлов и структур
    print('Прочитано файлов: {}'.format(len(full_cells)))
    wall()
    print('Название файла: кол-во структур')
    number_ = 0
    for file in os.listdir(path):
        print('{}: {}'.format(file, len(full_cells[number_])))
        number_ += 1
    wall()
    # Фильтрация Rsd
    #(full_cells[1][0].atom_dataset.filter_Rsd(float(input('Введите минимальное Rsd = '))))
    full_cells[1][0].atom_dataset.filter_Rsd(1.3507)
    # Фильтрация матрицы смежности по Rsd
    print('Список элементов: {}\n'
          'По умолчанию рассматривается связь Li — O\n'
          'С коэффициентом деформации 10%'.format(' '.join(full_cells[0][0].composition.keys())))
    full_cells[1][0].filter_matrix()
    print(full_cells[1][0].adjacency_matrix.filter_dataset)

