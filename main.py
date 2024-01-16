import os
import plot
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
        Rsd_counts = []
        Rad_counts = []
        cell_names = []
        print('Файл: {}', file_name)
        """Поддерживает только один файл"""
        for cell in file_cells:
            cell_names.append(cell.additional_information.dataset['name'])
            print('Ячейка: ', cell.additional_information.dataset['name'])
            for Rsd_min in cell.Rsd_unique('Li'):
                print('Rsd = ', Rsd_min)
                cell.atom_dataset.filter_Rsd(Rsd_min)
                #можно указать до двух элементов и коэф деформации
                cell.filter_matrix()
                #Названия файла
                name_file = cell.name_db.replace('.dat', '_') + cell.additional_information.dataset['name'].replace(' ', '')
                name_file = ''.join(s for s in name_file if s not in '\/:*?"<>|+') + '_Rsd=' + str(Rsd_min)

                cell.atomic_environment(center='ZA',environment='V', name_file=name_file)
                cell.in_POSCAR(path=path, name_file=name_file)
                cell.statistics(Rsd_min=Rsd_min)
                if Rsd_min == cell.Rsd_unique('Li')[-1]:
                    Rsd_counts.append(cell.additional_information.Rsd_counts)
                    Rad_counts.append(cell.additional_information.Rad_counts)
                wall()
        plot.plot_distribution(Rsd_counts=Rsd_counts, Rad_counts=Rad_counts, cell_name=cell_names)

