import pandas as pd
import numpy as np

input1 = [('a', 2), ('b', 5)]
input2 = [('a', 1), ('b', 2), ('c', 3)]  # Same output as for input1 for the below dataset

dataset = pd.DataFrame([[1, 2, 3], [1, 2, 3], [1, 1, 1], [
    2, 5, 6]], columns=['a', 'b', 'c'])


def create_query_condition(list_tuple, df_name):
    """ Create a string condition from the keys and values in list_
    Arguments:
        :param list_tuple: 2D array: 1st column is key, 2nd column is value
        :param df_name: dataframe name
    """
    my_array = np.array(list_tuple)
    # Get keys - values
    keys = my_array[:, 0]
    values = my_array[:, 1]
    # Create string query
    query = ' & '.join(['({0}.{1} == {2})'.format(df_name, k, v)
                        for k, v in zip(keys, values)])
    return query



print(select_data(input1,dataset))



query = create_query_condition(input2, 'dataset')
