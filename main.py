import os
from Topos_reading import reading

if __name__ == '__main__':
    # path = input('Введите путь к файлам: ')
    path = 'D:\Py\проекты\ToposPro\check'
    full_cells = reading(path)
    #количество файлов и структур
    print('Прочитано файлов: {}'.format(len(full_cells)))
    print('--------------------------------------------')
    print('Количество структур:')
    number_ = 0
    for file in os.listdir(path):
        print('{}: {}'.format(file, len(full_cells[number_])))
        number_ += 1
    print(full_cells[0][0].atom_dataset.dataset)
    print(full_cells[0][0].adjacency_matrix.dataset)
    print(full_cells[0][0].additional_information.dataset)