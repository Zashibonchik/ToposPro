import pandas as pd
class Cell:
    def __init__(self, atom_dataset, adjacency_matrix, additional_information, name_db):
        """
        :param atom_dataset: type - , информация об атомах структуры (название, координаты и тд)
        :param adjacency_matrix: type - , матрица смежности (МС)
        :param additional_information: type - , доп параметры, идущие после МС
        :param name_db: type - str, название базы данных
        """
        self.atom_dataset = atom_dataset
        self.adjacency_matrix = adjacency_matrix
        self.additional_information = additional_information

    def transfer_in_df(self):
        #ПРИДЕТСЯ УДАЛЯТЬ СТЕПЕНЬ ОКИСЛЕНИЯ, ТАК КАК ОНА НЕ ВЕЗДЕ ЕСТЬ
        self.atom_dataset = [line.split() for line in self.atom_dataset]
