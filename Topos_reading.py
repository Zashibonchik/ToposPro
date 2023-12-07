import os
from cell import Cell
from atoms import Atoms
from adjacency_matrix import Adjacency_matrix
from additional_information import Additional_information
#чтение топос файла, возвращает список списков ячеек (списки внутри представляют собой ячейки из одного файла)
def reading(path) -> list:
    path_cells = [] #список списков ячеек
    for file in os.listdir(path):
        file_cells = [] #ячейки из одного файла
        with open(path + '\\' + file, "r") as Topos_dataset:
            while Topos_dataset.tell() != os.path.getsize(path + '\\' + file): #итерация пока не закончится файл
                atom_dataset = reading_until(word_until='matrix', file=Topos_dataset) #данные об атомах
                MC_dataset = reading_until(word_until='Composition', file=Topos_dataset) #MC
                add_info_dataset = reading_until(word_until='--------------------------------------------',
                                                  file=Topos_dataset) #доп параметры
                topos_cell = Cell(atom_dataset=Atoms(atom_dataset),
                                  adjacency_matrix=Adjacency_matrix(MC_dataset),
                                  additional_information=Additional_information(add_info_dataset),
                                  name_db=path)
                file_cells.append(topos_cell)
                """В конце файлов .dat создаются две пустые строки,
                которые ошибочно воспринимаются за ячейку.
                Поэтому удаляем псевдоячейку, если в ее МС 1 элемент"""
                if len(topos_cell.adjacency_matrix.dataset) == 1:
                    file_cells.remove(topos_cell)
        path_cells.append(file_cells)
    return path_cells

#ф-ия для чтения фрагментов файла, возвращает список строк
def reading_until(word_until, file) -> list:
    dataset = []
    line = 1
    while line:
        line = file.readline()
        if line.find(word_until) + 1:
            """find() возвращает -1, если нет подстроки"""
            return dataset
        line = (''.join(line.split('\n')).replace('\t','')) #удалить \n и \t
        dataset.append(line)
    return dataset

