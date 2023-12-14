import os
from cell import Cell
from atoms import Atoms
from adjacency_matrix import Adjacency_matrix
from additional_information import Additional_information
import pandas as pd
#чтение топос файла, возвращает список списков ячеек (списки внутри представляют собой ячейки из одного файла)
def reading(path) -> list:
    # список списков ячеек
    path_cells = []
    for file in os.listdir(path):
        # ячейки из одного файла
        file_cells = []
        with open(path + '\\' + file, "r") as Topos_dataset:
            # итерация пока не закончится файл
            while Topos_dataset.tell() != os.path.getsize(path + '\\' + file):
                # данные об атомах
                atom_dataset = reading_until(word_until='matrix', file=Topos_dataset)
                """В конце файлов .dat создаются две пустые строки,
                которые ошибочно воспринимаются за ячейку.
                Поэтому удаляем псевдоячейку, если в ее МС 1 элемент"""
                if len(atom_dataset) > 1:
                    atom_dataset = atoms_transfer_in_df(atom_dataset)
                    # MC
                    MC_dataset = reading_until(word_until='Composition', file=Topos_dataset)
                    MC_dataset = adjacency_matrix_transfer_in_df(MC_dataset)
                    # доп параметры
                    add_info_dataset = reading_until(word_until='--------------------------------------------',
                                                      file=Topos_dataset)
                    add_info_dataset = additional_information_transfer_in_df(add_info_dataset)
                    topos_cell = Cell(atom_dataset=Atoms(atom_dataset),
                                      adjacency_matrix=Adjacency_matrix(MC_dataset),
                                      additional_information=Additional_information(add_info_dataset))
                    file_cells.append(topos_cell)
        path_cells.append(file_cells)
    return path_cells

#ф-ия для чтения фрагментов файла, возвращает список строк
def reading_until(word_until, file) -> list:
    dataset = []
    line = 1
    while line:
        #построчно читаем файл и проверяем строку
        line = file.readline()
        if line.find(word_until) + 1:
            """find() возвращает -1, если нет подстроки"""
            return dataset
        """при достижении строки с \n, while не работает. 
        Возможно, неверное предположение"""
        # Проверка на пустую строку и удаление \n
        if line != '\n':
            line = line.replace('\n', '')
            dataset.append(line)
        else:
            line = 1
    return dataset

"""Ф-ции для перевода в датафрейм"""
def atoms_transfer_in_df(atom_dataset) -> pd.DataFrame:
    columns_ = atom_dataset[5].split()[:7] + [atom_dataset[5].split()[-1]]
    atom_dataset = [atoms_beautiful_line(line) for line in atom_dataset if atom_dataset.index(line) > 5]
    atom_dataset = pd.DataFrame(atom_dataset, columns=columns_)
    #изменяем типы данных
    atom_dataset = atom_dataset.astype({name:'float16' for name in columns_ if name in columns_[-4:]})
    return atom_dataset

"""Ф-ия для устранения ошибки, связанной с пустыми значениями
в столбце со степенью окисления в .dat"""
"""Топос для многих атомов не может самостоятельно определить степень окисления,
что может привести к проблемам при дальнейшей обработке.
Степень окисления будет равна нулю для атомов, которых она не определена."""
def atoms_beautiful_line(line) -> list:
    line = line.split()
    try:
        # проверка на пустоту в столбце со степенью окисления
        int(line[2])
        return line[:7] + [line[-1]]
    except:
        line.insert(2, 0)
        return line[:7] + [line[-1]]

def adjacency_matrix_transfer_in_df(adjacency_matrix) -> pd.DataFrame:
    columns_ = adjacency_matrix[0].split('\t')
    adjacency_matrix = [line.split('\t')[:-1] for line in adjacency_matrix[1:] if line !='---------------------------------------------------------']
    adjacency_matrix = pd.DataFrame(adjacency_matrix, columns=columns_)
    return adjacency_matrix

def additional_information_transfer_in_df(additional_information) -> pd.Series:
    """Возможно несоотвествие индексов и требуемых значений"""
    parameters_dict = {}
    Z = additional_information[3]
    name_cell = additional_information[-1]
    cell_parameters = additional_information[-4:-2]
    volume = additional_information[-2]
    #кристал. заселенность
    parameters_dict['Z'] = after_equals(Z)
    #объем
    parameters_dict['Volume'] = after_equals(volume[:volume.find(';')])
    #параметры ячейки
    for parameters in cell_parameters:
        for name, value in zip(parameters.split()[::2], parameters.split()[1::2]):
            parameters_dict[name[:-1]] = value
    #название
    parameters_dict['name'] = name_cell
    return pd.Series(parameters_dict)

def after_equals(line):
    index_eq = line.find('=')
    return line[index_eq + 1:]