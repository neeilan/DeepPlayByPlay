# Configure the variables in this file (mostly paths to various locations)

# Training/validation/test set paths are directories which in turn
# contain a directory for each class of data. For example:

# TRAINING_SET
# |- INSIDE_MAKE
#    |- an_inside_make.mp4
#    |- another_inside_make.mp4
# |- INSIDE_MISS
# |- MIDRANGE_MAKE
# |- MIDRANGE_MISS
# |- THREE_PONINT_MAKE
# |- THREE_POINT_MISS

# It it important that the class folder names are consistent across the
# training/validation/test set directories, as the class names are determined
# by simply reading the name of the folders.

TRAINING_SET_PATH = 'path/to/training/set'
VALIDATION_SET_PATH = 'path/to/validation/set'
TEST_SET_PATH = 'path/to/test/set'


# Path to directory in which to save weights during training
SAVE_WEIGHTS_PATH = 'path/to/save/weights'
WEIGHTS_FILENAME = 'dpbp_weights.hdf5'
LOAD_WEIGHTS_FILE = 'path/to/load/weights/from.hdf5' # For run_inference; can be same as above file

# Path to video to run inference on
ANNOTATE_PATH = 'path/to/video/to/annotate'

# Mapping of integer encoded string class names to category names
NUM_CLASSES = 6

CLASSNAME_MAPPING = {'0': 'INSIDE_MAKE',
                     '1': 'INSIDE_MISS',
                     '2': 'MIDRANGE_MAKE',
                     '3': 'MIDRANGE_MISS',
                     '4': 'THREE_POINT_MAKE',
                     '5': 'THREE_POINT_MISS'}

# Video dimension
FRAMES_PER_VIDEO = 90
VIDEO_DIMENSIONS = (240, 320, 1)  # x by y by number of channels

# Training parameters
EPOCHS_TO_TRAIN = 5
STEPS_PER_EPOCH = 500
