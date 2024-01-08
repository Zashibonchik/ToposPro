import os

import matplotlib.pyplot as plt

from Topos_reading import reading
from cell import Cell
import pandas as pd
import numpy as np
"""Не определяется G3!!!"""


pd.set_option('display.max_rows', None)
def wall():
    print('--------------------------------------------')

#Рассчитать кол-во столбцов и строк на рисунке
def number_multipliers(number):
    factor1 = 0
    factor2 = number
    while factor1 + 1 <= factor2:
        factor1 += 1
        if number % factor1 == 0:
            factor2 = number // factor1
    return factor1, factor2
def plot_Rsd_counts(Rsd_counts: list, cell_name: str):
    if len(Rsd_counts) in (3, 5):
        if len(Rsd_counts) == 3:
            rows = 2
            columns = 2
        else:
            rows = 2
            columns = 3
    else:
        columns, rows = number_multipliers(len(Rsd_counts))
    fig, axs = plt.subplots(rows, columns, figsize=(10, 6),
                            layout='constrained',
                            sharex=True, sharey=True)
    fig.suptitle('Количество пустот в зависимости от Rsd', fontsize=16)
    for ax, elem in zip(np.array(axs).flat, range(len(Rsd_counts))):
        if elem >= len(np.array(axs).flat)//2:
            ax.set_xlabel('Rsd')
        if elem == 0 or elem == len(np.array(axs).flat)//2:
            ax.set_ylabel('Кол-во пустот')
        ax.set_axisbelow(True) #Нарисовать сетку поздаи всех элементов графика
        ax.grid(True)
        ax.set_title(cell_name[elem])
        ax.scatter(x=list(Rsd_counts[elem].keys()), y=list(Rsd_counts[elem].values()),
                   color='darkorange',
                   edgecolors='black',
                   s=50
                   )
        ax.tick_params(axis='both', direction='in')
    (np.array(axs).flat)[-1].set_xlabel('Rsd')
    fig.savefig(fname='Количество пустот в зависимости от Rsd.jpg')
    plt.show()
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
        cell_names = []
        print('Файл: {}', file_name)
        for cell in file_cells:
            cell_names.append(cell.additional_information.dataset['name'])
            print('Ячейка: ', cell.additional_information.dataset['name'])
            for Rsd_min in cell.Rsd_unique('Li'):
                print('Rsd = ', Rsd_min)
                cell.atom_dataset.filter_Rsd(Rsd_min)
                cell.filter_matrix()
                #cell.in_POSCAR(path=path, Rsd=Rsd_min)
                cell.statistics(Rsd_min=Rsd_min)
                if Rsd_min == cell.Rsd_unique('Li')[-1]:
                    Rsd_counts.append(cell.additional_information.Rsd_counts)
                wall()
        plot_Rsd_counts(Rsd_counts, cell_name=cell_names)

