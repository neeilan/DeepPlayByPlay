import numpy as np
import skvideo.io
import skvideo.utils
import random

from os import listdir
from os import path
from os.path import isdir
from os.path import join

from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

from config import VIDEO_DIMENSIONS

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
    # (or at least # epochs * steps per epoch)
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
          assert (h, w, c) == VIDEO_DIMENSIONS

          if f >= frames:
              video = video[:frames, :, :, :]
          else:
              video = np.vstack((video, np.zeros((frames-f, h, w, c))))

          video = video / 255.0

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
          assert (h, w, c) == VIDEO_DIMENSIONS

          if f >= frames:
              video = video[:frames, :, :, :]
          else:
              video = np.vstack((video, np.zeros((frames-f, h, w, c))))
          
          video = video / 255.0

          flipped_vid = np.flip(video, axis=2)
          encoded_label = DataSetGenerator.encode([y_label], classes=self.classes)

          yield (np.array([video]), np.array(encoded_label))
          yield (np.array([flipped_vid]), np.array(encoded_label))
          
