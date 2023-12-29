import pandas as pd
class Additional_information:
    def __init__(self, dataset: pd.Series):
        """
        :param dataset: type – pd.Series, доп. информация
        :param Rsd_counts: type – dict, значение фильтра Rsd: кол-во пустот после фильтрации
        """
        self.dataset = dataset
        self.Rsd_counts = {}

    def distribution_Rsd(self, Rsd_min, ZA_values):
        self.Rsd_counts[Rsd_min] = ZA_values



