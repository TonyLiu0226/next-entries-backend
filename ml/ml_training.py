import os
import sklearn
import numpy as np
import pandas as pd

#loads data from a txt file
#file: file to read from. Each line in file must be split into two parts with a specified character char
#char: character to split each line with
#arr: array to store each line

def load_data(file, char, arr):
    with open(file) as f:
        for line in f:
            segments = line.split(char)
            list = []
            list.append(segments[0])
            list.append(segments[1].split('\n')[0])
            arr.append(list)
    return None

data = []
load_data("./emotions/train.txt", ';', data)
load_data("./emotions/val.txt", ';', data)

df = pd.DataFrame(data=data, columns=["entries", "emotions"])
print(df)