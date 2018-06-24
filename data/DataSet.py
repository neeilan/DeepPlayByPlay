import numpy as np
from os import listdir
from os import path
from os.path import isdir
from os.path import join
import skvideo.io
import random

from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

video_dimensions = (240, 320, 3)


class DataSet():
    def __init__(self, data_root, augmentations=[], shuffle=True):
        self.data_root = data_root
        self.augmentations = augmentations
        self.classes = DataSet.class_names(data_root)

        self.XY_meta = self.load_metadata()
        self.X, self.Y = self.load_data(frames=85, shuffle=shuffle, first_n=5)

        print('X shape: {}'.format(self.X.shape))
        print('Y shape: {}'.format(self.Y.shape))

    @staticmethod
    def class_names(data_root):
        return [file_name for file_name in listdir(data_root)
                if isdir(join(data_root, file_name))]

    @staticmethod
    def encode(Y):
        label_encodings = LabelEncoder().fit_transform(Y)
        return to_categorical(label_encodings)

    def load_metadata(self):
        meta_pairs = []
        for class_name in self.classes:
            class_dir = join(self.data_root, class_name)
            for file_name in listdir(class_dir):
                meta_pairs.append((join(class_dir, file_name), class_name))
        return meta_pairs

    def load_data(self, frames, shuffle, first_n=None):
        '''
        Loads the video data into memory.
        '''
        _XY_meta = self.XY_meta.copy()

        if shuffle:
            random.shuffle(_XY_meta)

        XY_pairs = []
        for video_path, y_label in _XY_meta[:first_n]:

            video = skvideo.io.vread(video_path)

            f, h, w, c = video.shape
            assert (h, w, c) == video_dimensions

            if f >= frames:
                video = video[:frames, :, :, :]
            else:
                video = np.vstack((video, np.random.randn(frames-f, h, w, c)))

            XY_pairs.append((video, y_label))

            for aug in self.augmentations:
                XY_pairs.append((aug(video), y_label))

        if shuffle and len(self.augmentations):
            random.shuffle(XY_pairs)

        X, Y = [x for x, _ in XY_pairs], [y for _, y in XY_pairs]
        Y = DataSet.encode(Y)

        return np.array(X), np.array(Y)
