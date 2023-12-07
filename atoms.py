import pandas as pd
class Atoms:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    #перевод данных в датафрейм
    def transfer_in_df(self):
        columns_ = self.dataset[5].split()[:7] + [self.dataset[5].split()[-1]]
        self.dataset = [beautiful_line(line) for line in self.dataset if self.dataset.index(line)>5]
        self.dataset = pd.DataFrame(self.dataset, columns=columns_)
