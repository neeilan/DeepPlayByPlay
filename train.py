import keras

WEIGHTS_FILENAME = 'dpbp_weights.hdf5'


def fit_epochs(epochs, model = model):
  validation_data = DataSet(data_root=VALIDATION_SET_PATH)
  
  early_stop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.05, patience=4)
  terminate_nan = keras.callbacks.TerminateOnNaN()
  checkpointer = keras.callbacks.ModelCheckpoint(filepath= SAVE_WEIGHTS_PATH + WEIGHTS_FILENAME, verbose=1, save_best_only=False)


  return model.fit_generator(generator=gen,
                      steps_per_epoch=500,  # 2250 - most of the training set
                      epochs=epochs,
                      verbose=1,
                      callbacks=[checkpointer],
                      validation_data=(validation_data.X, validation_data.Y),
                      max_queue_size=5,
                      workers=1,
                      use_multiprocessing=False,
                      shuffle=False)
