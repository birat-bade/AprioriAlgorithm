import pandas as pd

from apriori_algorithm_implementation.config import Config
from apriori_algorithm_implementation.apriori import Apriori

dataset = pd.read_csv(Config.input_path + Config.flare, encoding='ISO-8859-1', dtype=object).fillna('')

apriori = Apriori(dataset, 0.8, 0.8, 5)

apriori.evaluate_frequency_item_set()
apriori.evaluate_item_pair_set()
