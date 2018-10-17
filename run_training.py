from config import VALIDATION_SET_PATH, TRAINING_SET_PATH, EPOCHS_TO_TRAIN

from data.dataset import DataSet
from data.dataset_generator import DataSetGenerator

from model import PBPModel


from training import fit_epochs

if __name__ == '__main__':
    model = PBPModel().get_model()
    training_set_gen = DataSetGenerator(data_root=TRAINING_SET_PATH)
    validation_data = DataSet(data_root=VALIDATION_SET_PATH)
    fit_epochs(EPOCHS_TO_TRAIN, model, training_set_gen, validation_data)