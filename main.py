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
    print('По умолчанию рассматривается связь Li — O\n'
          'С коэффициентом деформации 10%')
    wall()
    for file_cells, file_name in zip(full_cells, os.listdir(path)):
        print('Файл: {}', file_name)
        for cell in file_cells:
            for Rsd_min in cell.Rsd_unique('Li'):
                print('Rsd = ', Rsd_min)
                cell.atom_dataset.filter_Rsd(Rsd_min)
                cell.filter_matrix()
                cell.in_POSCAR(path)
                wall()


