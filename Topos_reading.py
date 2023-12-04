import pandas as pd
import os
path = '2Li-Mg#.dat'
def reading(path):
    with open(path, "r") as Topos_dataset:
        # cell_datacet = []
        # for line in Topos_dataset: #данные об атомах
        #     cell_datacet.append(''.join(line.split('\n')))
        #     if line.find('matrix')+1: #поиск строки, где начинается МС
        #         pass
        #     if line.find('Composition')+1: #информация после МС
        #         pass

        while Topos_dataset.tell() != os.path.getsize(path):
            print(1)
            atom_dataset = reading_until(word_until='matrix', file=Topos_dataset)
            MC_dataset = reading_until(word_until='Composition', file=Topos_dataset)
            parametrs_dataset = reading_until(word_until='--------------------------------------------',
                                              file=Topos_dataset)
            print(parametrs_dataset)
        #print(atom_dataset)
        #print(MC_dataset)
        print(parametrs_dataset)
def reading_until(word_until, file):
    dataset = []
    line = 1
    while line:
        line = file.readline()
        if line.find(word_until) + 1: # find() возвращает -1, если нет подстроки
            return dataset
        dataset.append(''.join(line.split('\n')))
    return dataset
reading('2Li-Mg#.dat')