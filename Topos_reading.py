import os
from cell import Cell
#чтение топос файла
def reading(path):
    path_cells = []
    for file in os.listdir(path):
        file_cells = []
        with open(path + '\\' + file, "r") as Topos_dataset:
            while Topos_dataset.tell() != os.path.getsize(path + '\\' + file): #итерация пока не закончится файл
                atom_dataset = reading_until(word_until='matrix', file=Topos_dataset) #данные об атомах
                MC_dataset = reading_until(word_until='Composition', file=Topos_dataset) #MC
                add_info_dataset = reading_until(word_until='--------------------------------------------',
                                                  file=Topos_dataset) #доп параметры
                topos_cell = Cell(atom_dataset=atom_dataset,
                                  adjacency_matrix=MC_dataset,
                                  additional_information=add_info_dataset,
                                  name_db=path)
                file_cells.append(topos_cell)
        path_cells.append(file_cells)
    return path_cells

#ф-ия для чтения фрагментов файла.
def reading_until(word_until, file):
    dataset = []
    line = 1
    while line:
        line = file.readline()
        if line.find(word_until) + 1: # find() возвращает -1, если нет подстроки
            return dataset
        line = (''.join(line.split('\n')).replace('\t','')) #удалить \n и \t
        dataset.append(line)
    return dataset
