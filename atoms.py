import pandas as pd
"""Ф-ия для устранения ошибки, связанной с пустыми значениями
 в столбке со степенью окисления в .dat"""
"""Топос для многих атомов не может самостоятельно определить степень окисления,
что может привести к проблемам при дальнейшей обработке.
Степень окисления будет равна нулю для атомов, которых она не определена."""
def beautiful_line(line) -> list:
    line = line.split()
    try:
        int(line[2]) # проверка на пустоту в столбце со степенью окисления
        return line[:7] + [line[-1]]
    except:
        line.insert(2, 0)
        return line[:7] + [line[-1]]

class Atoms:
    def __init__(self, dataset: list):
        self.dataset = dataset

    #перевод данных в датафрейм
    def transfer_in_df(self):
        columns_ = self.dataset[5].split()[:7] + [self.dataset[5].split()[-1]]
        self.dataset = [beautiful_line(line) for line in self.dataset if self.dataset.index(line)>5]
        self.dataset = pd.DataFrame(self.dataset, columns=columns_)
