class Config:
    # columns = ['Code for class', 'Code for largest spot size', 'Code for spot distribution', 'Activity',
    # 'Evolution', 'Previous 24 hour flare activity code', 'Historically-complex', 'Pass across the sun\'s disk',
    # 'Area','Area of the largest spot', 'C-class flares production', 'M-class flares production',
    # 'X-class flares production']

    columns = ['Code for class', 'Code for largest spot size', 'Code for spot distribution', 'Activity', 'Evolution',
               'Previous 24 hour flare activity code', 'Historically-complex', 'Pass across the sun\'s disk', 'Area',
               'Area of the largest spot']

    input_path = '../input/'
    flare = 'flare.csv'

    output_path = '../output/'

    frequency_item_set = 'frequency_item_set.csv'

    item_pair_set = 'item_pair_set.csv'
