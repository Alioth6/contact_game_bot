import pandas as pd
from tqdm import tqdm


'''
Model test full example:

from src.models.sim_model import SimWords
from src.metrics.score import NaiveMetric
import torch

w2v_model = torch.load('wiki0_model')
sim_model = SimWords(w2v_model)
test_model('rus_test_set.csv', sim_model, NaiveMetric())
'''


def test_model(test_set_name, model, metric):
    '''
    example:

    test_model('rus_test_set.csv', sim_model, NaiveMetric())
    '''

    # test set: word, defs
    test_set = pd.read_csv(test_set_name)
    n_defs = test_set.shape[0]

    not_in_dict = 0

    for i in tqdm(range(n_defs)):
        word = test_set.iloc[i]['word']
        if model.is_in_vocab(word):
            def_text = test_set.iloc[i]['defs']
            prefix_size = 0

            res = model.get_words(def_text, word[:prefix_size])
            metric.update(word, res)
        else:
            not_in_dict += 1

    print('Test score: ', metric.score())
    print('Not in dictionary: ', not_in_dict)