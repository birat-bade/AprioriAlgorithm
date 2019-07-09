import pandas as pd
from itertools import combinations, product

from apriori_algorithm_implementation.config import Config


class Apriori:
    def __init__(self, dataset, min_support, min_confidence, min_length):

        self.dataset = dataset
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.min_length = min_length

        self.frequency_item_set = pd.DataFrame()
        self.item_pair_set = pd.DataFrame()
        self.output = pd.DataFrame()

    def evaluate_frequency_item_set(self):

        for column in Config.columns:
            temp_list = list((set(self.dataset[column].tolist())))

            for temp_data in temp_list:
                count_df = self.dataset[self.dataset[column] == temp_data]
                frequency = len(count_df)
                support = len(count_df) / len(self.dataset)

                # key = column + '|' + temp_data

                temp_df = pd.DataFrame()

                if support >= self.min_support:
                    temp_df['column'] = [column]
                    temp_df['item'] = [temp_data]
                    temp_df['frequency'] = [frequency]
                    temp_df['support'] = [support]
                    temp_df['combined'] = [column + '=' + temp_data]

                    self.frequency_item_set = self.frequency_item_set.append(temp_df)
        self.frequency_item_set.to_csv(Config.output_path + Config.frequency_item_set, index=False)

    def evaluate_item_pair_set(self):

        self.item_pair_set = self.item_pair_set.append(self.frequency_item_set)

        for r in range(2, self.min_length + 1):
            temp_list = list(set(list(self.frequency_item_set['column'])))
            temp_list = [items for items in combinations(temp_list, r)]

            for columns in temp_list:

                item_sets = list()

                for column in columns:
                    item = self.frequency_item_set[self.frequency_item_set['column'] == column]['item']
                    item_sets.append(item.tolist())

                item_collection = [i for i in product(*item_sets)]

                column_value_combination = list()

                for collection in item_collection:
                    column_value_combination.append([(columns[i], collection[i]) for i in range(0, len(collection))])

                for combination in column_value_combination:

                    tup = [i[1] for i in combination]

                    count_df = select_data(combination, self.dataset)
                    frequency = len(count_df)

                    support = len(count_df) / len(self.dataset)

                    combined = list()

                    for b in range(0, len(columns)):
                        combined.append(columns[b] + '=' + tup[b])

                    combined = sorted(combined)

                    if support >= self.min_support:
                        temp_df = pd.DataFrame()
                        temp_df['column'] = ['|'.join(columns)]
                        temp_df['item'] = ['|'.join(tup)]
                        temp_df['frequency'] = frequency
                        temp_df['support'] = [support]
                        temp_df['combined'] = ['|'.join(combined)]
                        self.item_pair_set = self.item_pair_set.append(temp_df)

        combined_list = self.item_pair_set['combined'].tolist()
        combined_list = [items for items in product(combined_list, repeat=2)]

        combined_dict = dict(zip(list(self.item_pair_set['combined']), list(self.item_pair_set['support'])))

        ant = [i[0] for i in combined_list]
        det = [i[1] for i in combined_list]
        combined = [i[0] + '|' + i[1] for i in combined_list]
        ant_support = [combined_dict.get(i[0]) for i in combined_list]
        det_support = [combined_dict.get(i[1]) for i in combined_list]

        # pair_support = [combined_dict.get(i[0] + '|' + i[1]) for i in combined_list]

        self.output['antecedent'] = ant
        self.output['consequent'] = det
        self.output['combined'] = combined
        self.output['antecedent_support'] = ant_support
        self.output['consequent_support'] = det_support
        self.output['support'] = self.output.apply(get_pair_support, 1, args=[combined_dict])

        self.output = self.output.fillna('')

        self.output = self.output[self.output['support'] != '']

        self.output['confidence'] = self.output.apply(compute_confidence, 1)

        self.output = self.output[(self.output['confidence'] >= self.min_confidence)]

        self.item_pair_set.to_csv(Config.output_path + Config.item_pair_set, index=False)

        self.output.to_csv(Config.output_path + Config.confidence_matrix, index=False)

        print(self.output.shape)

      
def compute_confidence(row):
    antecedent = row['antecedent_support']
    pair = row['support']

    confidence = pair / antecedent

    return confidence


def select_data(filter_lst, df):
    d = dict(filter_lst)
    res = df.loc[(df[list(d.keys())] == pd.Series(d)).all(axis=1)]
    return res


def get_pair_support(row, args):
    combined = row['combined']

    combined = '|'.join(sorted(combined.split('|')))

    pair_support = args.get(combined)

    return pair_support


def find_all_sub_sets(index, superset, sep):
    output = list()
    for i in range(index, len(superset) + 1):
        iterable = combinations(superset, i)
        for j in iterable:
            output.append(sep.join(list(j)))
    return output
