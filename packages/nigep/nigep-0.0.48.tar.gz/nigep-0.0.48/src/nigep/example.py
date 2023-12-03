import os
import sys
from keras.utils import get_file
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from nigep import Nigep
from layers import SaltAndPepperNoise
import zipfile
from keras.layers import Flatten, Dense, Conv2D, MaxPooling2D, Dropout
from keras.models import Sequential, Model
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.optimizers.legacy import Adam, SGD, RMSprop