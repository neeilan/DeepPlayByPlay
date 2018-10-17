import numpy as np

from config import LOAD_WEIGHTS_FILE, TEST_SET_PATH, CLASSNAME_MAPPING
from data.dataset_generator import DataSetGenerator
from model import PBPModel

TEST_SET_SIZE = 253


def evaluate(model, test_set_generator):
    ovrall_corr, ovrall_inc, twothree_corr, twothree_inc, binary_corr = 0, 0, 0, 0, 0

    count = 0
    for x_vi, y in test_set_generator.generate_data_finite():
        if count == TEST_SET_SIZE:
            break
        count += 1

        y = y[0]
        pred = model.predict(x_vi)
        y_pred = np.argmax(pred, axis=1)[0]

        pred_label = CLASSNAME_MAPPING[str(y_pred)]
        actual_label = CLASSNAME_MAPPING[str(np.argmax(y))]

        if actual_label == pred_label:

            ovrall_corr += 1
            twothree_corr += 1
        else:
            ovrall_inc += 1

            # Treat both midrange and inside shot as twos, and outside shots as threes, giving us 4 eval categories
            if actual_label in ['INSIDE_MAKE', 'MIDRANGE_MAKE'] and pred_label in ['INSIDE_MAKE', 'MIDRANGE_MAKE']:
                twothree_corr += 1
            elif actual_label in ['INSIDE_MISS', 'MIDRANGE_MISS'] and pred_label in ['INSIDE_MISS', 'MIDRANGE_MISS']:
                twothree_corr += 1
            else:
                twothree_inc += 1

        if ('_MISS' in actual_label and '_MISS' in pred_label) or ('_MAKE' in actual_label and '_MAKE' in pred_label):
            binary_corr += 1

    print('Overall accuracy: ' + str(ovrall_corr))
    print('4 category accuracy: ' + str(twothree_corr))
    print('Binary (make/miss) accuracy: ' + str(binary_corr/TEST_SET_SIZE))


if __name__ == '__main__':
    model = PBPModel().get_model()
    model.load_weights(LOAD_WEIGHTS_FILE)
    test_set_gen = DataSetGenerator(TEST_SET_PATH)
    evaluate(model, test_set_gen)
