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

    #перевод данных в датафрейм
    def transfer_in_df(self):
        #информация об атомах
        self.atom_dataset = [line.split() for line in self.atom_dataset ]
        columns_ = self.atom_dataset[5]
        """Топос для многих атомов не может самостоятельно определить степень окисления,
        что может привести к проблемам при дальнейшей обработке.
        Степень окисления будет равна нулю для атомов, которых она не определна."""
        for index_line in range(5,len(self.atom_dataset)):
            if len(self.atom_dataset[index_line]) < len(columns_):
                self.atom_dataset[index_line].insert(2,0)
        self.atom_dataset = pd.DataFrame(self.atom_dataset[6:], columns=columns_)


