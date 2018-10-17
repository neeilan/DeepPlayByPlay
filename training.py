import keras

from data.dataset import DataSet
from config import SAVE_WEIGHTS_PATH, STEPS_PER_EPOCH, WEIGHTS_FILENAME


def fit_epochs(epochs, model, data_generator, validation_data):
    terminate_nan = keras.callbacks.TerminateOnNaN()
    checkpointer = keras.callbacks.ModelCheckpoint(
        filepath=SAVE_WEIGHTS_PATH + WEIGHTS_FILENAME, verbose=1, save_best_only=False)

    return model.fit_generator(generator=data_generator.generate_data(),
                               steps_per_epoch=STEPS_PER_EPOCH,
                               epochs=epochs,
                               verbose=1,
                               callbacks=[terminate_nan, checkpointer],
                               validation_data=(
                                   validation_data.X, validation_data.Y),
                               max_queue_size=5,
                               workers=1,
                               use_multiprocessing=False,
                               shuffle=False)
