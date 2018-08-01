import keras
from keras.layers.convolutional import Conv3D, MaxPooling3D
from keras.layers import Dense, Flatten, Dropout

from keras.models import Sequential, load_model
from keras.optimizers import Adam, RMSprop


class PBPModel():
    def __init__(self, metrics = ['accuracy']):
        self.input_shape = (1, 90, 240, 320, 1)
        self.num_classes = 6
        
        self.model = self.cnn()
        
        optimizer = Adam(lr=1e-5, decay=1e-6)

        self.model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,metrics=metrics)
        
        print(self.model.summary())
        
        
    def get_model(self):
      return self.model
        

    def cnn(self):
        model = Sequential()
        samples, frames, x, y, channels = self.input_shape

        model.add(Conv3D(
            32, (2,3,3), activation='relu', input_shape=(frames, x, y, channels), data_format='channels_last'
        ))
        model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(2, 2, 2)))
        
        model.add(Conv3D(64, (2,2,2), activation='relu'))
        model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(2, 3, 3)))
        
        model.add(Conv3D(128, (3,3,3), activation='relu'))
        model.add(Conv3D(128, (3,3,3), activation='relu'))
        model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(2, 3, 3)))
        model.add(Dropout(0.25))
        
        model.add(Conv3D(256, (2,2,2), activation='relu'))
        model.add(Conv3D(256, (2,2,2), activation='relu'))
        model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(2, 3, 3)))

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Dropout(0.25))
        model.add(Dense(1024))
        model.add(Dropout(0.25))
        model.add(Dense(self.num_classes, activation='softmax'))

        return model
