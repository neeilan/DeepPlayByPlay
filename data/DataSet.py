# DataSet Generator class

import numpy as np
from os import listdir
from os import path
from os.path import isdir
from os.path import join
import skvideo.io
import skvideo.utils
import random

from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

video_dimensions = (240, 320, 1)


class DataSet():
    def __init__(self, data_root, augmentations=[], shuffle=True, first_n=None):
        self.data_root = data_root
        self.augmentations = augmentations
        self.classes = sorted(DataSet.class_names(data_root))

        self.XY_meta = self.load_metadata()
        
        self.X, self.Y = self.load_data(frames=90, shuffle=shuffle, first_n=first_n)

        for i, label in enumerate(self.classes):
          print("{} : {}".format(label, i))
          
        print('X shape: {}'.format(self.X.shape))
        print('Y shape: {}'.format(self.Y.shape))
        print(self.Y[:5,:])

    @staticmethod
    def class_names(data_root):
        return [file_name for file_name in listdir(data_root)
                if isdir(join(data_root, file_name))]

    @staticmethod
    def encode(Y, classes):
        label_encodings = LabelEncoder().fit_transform(classes + Y)
        return to_categorical(label_encodings)[len(classes):, :]

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
            video = skvideo.utils.rgb2gray(video)

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
        Y = DataSet.encode(Y, self.classes)

        return np.array(X), np.array(Y)
      

class DataSetGenerator():
  def __init__(self, data_root):
    self.data_root = data_root
    self.classes = sorted(DataSetGenerator.class_names(data_root))
            
    self.XY_meta = self.load_metadata()
    print(len(self.XY_meta))
    random.shuffle(self.XY_meta)
    
  @staticmethod
  def class_names(data_root):
      return [file_name for file_name in listdir(data_root)
              if isdir(join(data_root, file_name))]

  @staticmethod
  def encode(Y, classes):
      label_encodings = LabelEncoder().fit_transform(classes + Y)
      return to_categorical(label_encodings)[len(classes):, :]

    
  def load_metadata(self):
      meta_pairs = []
      for class_name in self.classes:
          class_dir = join(self.data_root, class_name)
          for file_name in listdir(class_dir):
              meta_pairs.append((join(class_dir, file_name), class_name))
      return meta_pairs
    
  def generate_data(self, frames=90):
    # keras generators need to be infinitely iterable
    # (or at least # epochs * stepe per epoch)
    while True:
      #yield self.generate_data_finite(frames)
      for video_path, y_label in self.XY_meta:

          try:
            video = skvideo.io.vread(video_path)  # add a try xcept continue here
            video = skvideo.utils.rgb2gray(video)
          except:
            print('Failed to read ' + video_path)
            continue

          f, h, w, c = video.shape
          assert (h, w, c) == video_dimensions

          if f >= frames:
              video = video[:frames, :, :, :]
          else:
              video = np.vstack((video, np.random.randn(frames-f, h, w, c)))

          v_min = video.min(axis=(0, 1), keepdims=True)
          v_max = video.max(axis=(0, 1), keepdims=True)
          video = (video - v_min)/(v_max - v_min)

          flipped_vid = np.flip(video, axis=2)
          encoded_label = DataSetGenerator.encode([y_label], classes=self.classes)

          yield (np.array([video]), np.array(encoded_label))
          yield (np.array([flipped_vid]), np.array(encoded_label))
    
  def generate_data_finite(self, frames=90):
      '''
      Loads the video data into memory.
      '''
      for video_path, y_label in self.XY_meta:

          try:
            video = skvideo.io.vread(video_path)
            video = skvideo.utils.rgb2gray(video)
          except:
            print('Failed to read ' + video_path)
            continue

          f, h, w, c = video.shape
          assert (h, w, c) == video_dimensions

          if f >= frames:
              video = video[:frames, :, :, :]
          else:
              video = np.vstack((video, np.random.randn(frames-f, h, w, c)))

          v_min = video.min(axis=(0, 1), keepdims=True)
          v_max = video.max(axis=(0, 1), keepdims=True)
          video = (video - v_min)/(v_max - v_min)

          flipped_vid = np.flip(video, axis=2)
          encoded_label = DataSetGenerator.encode([y_label], classes=self.classes)

          yield (np.array([video]), np.array(encoded_label))
          yield (np.array([flipped_vid]), np.array(encoded_label)) 
