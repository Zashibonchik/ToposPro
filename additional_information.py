import pandas as pd
class Additional_information:
    def __init__(self, dataset: pd.Series):
        """
        :param dataset: type – pd.Series, доп. информация
        :param Rsd_counts: type – dict, значение фильтра Rsd: кол-во пустот после фильтрации
        :param Rad_counts: type – dict, значение фильтра Rsd: средний размер Rad
        :param channel_ZA_values_filter: type – pd.Dataframe( columnds = ['Atom1', 'Atom2', 'SSeg'] ), часть МС без повторений
        """
        self.dataset = dataset
        self.Rsd_counts = {}
        self.Rad_counts = {}

    def distribution_Rsd(self, Rsd_min, ZA_values):
        self.Rsd_counts[Rsd_min] = ZA_values

    def distribution_Rad(self, Rsd_min):
        self.channel_ZA_values_filter['SSeg'] = self.channel_ZA_values_filter['SSeg'].astype('float')
        self.Rad_counts[Rsd_min] = self.channel_ZA_values_filter['SSeg'].describe()

    def center_environment(self, df):
        min_R = df['R'].min()
        max_R = df['R'].max()
        df_min = df[df['R'] == min_R]
        df_max = df[df['R'] == max_R]
        return df_min, df_max


