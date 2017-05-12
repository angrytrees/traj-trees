import json
import zipfile
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import csv
import operator
import Geohash
from build import TreeBuilding
from decision import haversine
from sklearn.cross_validation import train_test_split
import pickle

air_trajs = pd.read_csv('air_trajs.csv',
                        usecols = ['POLYLINE', 'Destination'],
                        converters={'POLYLINE': lambda x: json.loads(x), 'Destination': lambda x: json.loads(x)})

trajectories = list(air_trajs['POLYLINE'])
targets = list(air_trajs['Destination'])

X_train, X_test, y_train, y_test = train_test_split(trajectories, targets, train_size=0.005, random_state = 0)

tb = TreeBuilding()
tb = tb.fit(X_train, y_train, 10, 1)