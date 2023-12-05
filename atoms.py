import pandas as pd
class Atoms:
    def __init__(self, dataset: list):
        self.dataset = dataset

    #перевод данных в датафрейм
    def transfer_in_df(self):
        #информация об атомах
        self.dataset = [line.split() for line in self.dataset]
        columns_ = self.dataset[5]
        """Топос для многих атомов не может самостоятельно определить степень окисления,
        что может привести к проблемам при дальнейшей обработке.
        Степень окисления будет равна нулю для атомов, которых она не определена."""
        for index_line in range(5, len(self.dataset)):
            if len(self.dataset[index_line]) < len(columns_):
                self.dataset[index_line].insert(2, 0)
        self.dataset = pd.DataFrame(self.dataset[6:], columns=columns_)