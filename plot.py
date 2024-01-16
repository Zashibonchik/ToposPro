import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#Рассчитать кол-во столбцов и строк на рисунке
def number_multipliers(number):
    factor1 = 0
    factor2 = number
    while factor1 + 1 <= factor2:
        factor1 += 1
        if number % factor1 == 0:
            factor2 = number // factor1
    return factor1, factor2
def plot_distribution(Rsd_counts: list, Rad_counts: list, cell_name: str):
    #const
    fontsize_title = 20
    fontsize_axes = 12
    size_marker = 50
    figsize = 10,6

    if len(Rsd_counts) in (3, 5):
        if len(Rsd_counts) == 3:
            rows = 2
            columns = 2
        else:
            rows = 2
            columns = 3
    else:
        columns, rows = number_multipliers(len(Rsd_counts))
    if not os.path.isdir(os.path.join('ready', 'Graphics')):
        try:
            os.mkdir('ready')
            os.mkdir(os.path.join('ready', 'Graphics'))
        except:
            os.mkdir(os.path.join('ready', 'Graphics'))
    plot_Rsd_counts(Rsd_counts=Rsd_counts,
                    cell_name=cell_name,
                    rows=rows, columns=columns,
                    fontsize_title=fontsize_title,
                    fontsize_axes=fontsize_axes,
                    size_marker=size_marker,
                    figsize=figsize)
    plot_Rad_counts(Rad_counts=Rad_counts,
                    cell_name=cell_name,
                    rows=rows, columns=columns,
                    fontsize_title=fontsize_title,
                    fontsize_axes=fontsize_axes,
                    size_marker=size_marker,
                    figsize=figsize)

def plot_Rsd_counts(Rsd_counts: list, cell_name: str, rows: int, columns: int, fontsize_title, fontsize_axes, size_marker, figsize):
    fig, axs = plt.subplots(rows, columns, figsize=figsize,
                            layout='constrained',
                            sharex=True, sharey=True)
    fig.suptitle('Количество пустот в зависимости от Rsd', fontsize=fontsize_title)
    for ax, elem in zip(np.array(axs).flat, range(len(Rsd_counts))):
        if elem >= len(np.array(axs).flat) // 2:
            ax.set_xlabel('Rsd', fontsize=fontsize_axes)
        if elem == 0 or elem == len(np.array(axs).flat) // 2:
            ax.set_ylabel('Кол-во пустот', fontsize=fontsize_axes)
        ax.set_axisbelow(True)  # Нарисовать сетку поздаи всех элементов графика
        ax.grid(True)
        ax.set_title(cell_name[elem])
        ax.scatter(x=list(Rsd_counts[elem].keys()), y=list(Rsd_counts[elem].values()),
                   color='darkorange',
                   edgecolors='black',
                   s=size_marker
                   )
        ax.tick_params(axis='both', direction='in')
    # добавить подпись на последний подграфик
    (np.array(axs).flat)[-1].set_xlabel('Rsd', fontsize=fontsize_axes)
    fig.savefig(fname='ready/Graphics/Количество пустот в зависимости от Rsd.jpg')
def plot_Rad_counts(Rad_counts: list, cell_name: str, rows: int, columns: int, fontsize_title, fontsize_axes, size_marker,figsize):
    fig, axs = plt.subplots(rows, columns, figsize=figsize,
                            layout='constrained',
                            sharex=True, sharey=True)
    cell_names = cell_name.copy()
    names_parametrs = ['mean', 'std', 'min','25%', '50%', '75%', 'max']
    names_graphics = {'mean':'Среднее значения радиуса канала', 'std':'Дисперсия радиуса канала',
                      'min':'Минимальное значение радиуса канала','25%':'Первый квантиль значения радиуса канала',
                      '50%':"Второй квантиль значения радиуса канала", '75%':"Третий квантиль значения радиуса канала",
                      'max':"Максимальное значение радиуса канала"}
    while len(names_parametrs):
        fig.suptitle(names_graphics[names_parametrs[0]], fontsize=fontsize_title)
        parametr_statistics_plot(key=names_parametrs[0], axs=axs, Rad_counts=Rad_counts, cell_names=cell_names,
                                 fontsize_axes=fontsize_axes, size_marker=size_marker)
        fig.savefig(fname='ready/Graphics/{}.jpg'.format(names_parametrs[0]))
        #очистить графики
        for ax in np.array(axs).flat:
            ax.cla()
        del names_parametrs[0]
def parametr_statistics_plot(key: str, axs, Rad_counts, cell_names, fontsize_axes, size_marker):
    for ax, elem in zip(np.array(axs).flat, range(len(Rad_counts))):
        x_values = list(Rad_counts[elem].keys())
        y_values = []
        for df in Rad_counts[elem].values():
            y_values.append(df[key])
        ax.scatter(x=x_values, y=y_values,
                   color='darkorange',
                   edgecolors='black',
                   s=size_marker)
        ax.set_axisbelow(True)  # Нарисовать сетку поздаи всех элементов графика
        ax.grid(True)
        ax.set_title(cell_names[elem])
        ax.tick_params(axis='both', direction='in')
        if elem >= len(np.array(axs).flat) // 2:
            ax.set_xlabel('Rsd', fontsize=fontsize_axes)
        if (elem == 0 or elem == len(np.array(axs).flat) // 2) and key!='std':
            ax.set_ylabel('Радиус канала', fontsize=fontsize_axes)
        elif (elem == 0 or elem == len(np.array(axs).flat) // 2) and key=='std':
            ax.set_ylabel('Дисперсия радиуса канала', fontsize=fontsize_axes)
    #добавить подпись на последний подграфик
    (np.array(axs).flat)[-1].set_xlabel('Rsd', fontsize=fontsize_axes)

