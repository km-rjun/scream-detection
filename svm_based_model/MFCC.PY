import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import librosa
data = pd.read_csv('D:/Dev_stuff/metadata/UrbanSound8K.csv')
x_train = []
x_test = []
y_train = []
y_test = []

for i in tqdm(range(len(data))):
    file = data.iloc[i]['slice_file_name']
    label = data.iloc[i]['classid']
    filename = "D:/Dev_stuff/audio_dataset/"+file
    y, sr = librosa.load(filename)
    mfccs = np.mean(librosa.feature.mfcc(y, sr, n_mfcc=40).T,axis=0)
    x_train.append(mfccs)
    y_train.append(label)
    if label == 1:
        sol = label

'''y,sr = librosa.load("D:/Dev_stuff/audio_dataset/f_cry_7.wav")
mfccs =np.mean(librosa.feature.mfcc(y,sr,n_mfcc=40).T,axis=0)
x_test.append(mfccs)
y_test.append(label)
print(label)
y,sr=librosa.load("D:/Dev_stuff/audio_dataset/376637__eflexmusic__fire-shoot-them-voice-lines-mixed1.wav")
mfccs =np.mean(librosa.feature.mfcc(y,sr,n_mfcc=40).T,axis=0)
x_test.append(mfccs)
y_test.append(sol)'''


y, sr = librosa.load("D:/Dev_stuff/audio_dataset/damm_0.wav")
mfccs = np.mean(librosa.feature.mfcc(y,sr,n_mfcc=40).T,axis=0)
x_test.append(mfccs)
y_test.append(sol)

x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

np.savetxt('train_data.csv', x_train, delimiter=',')
np.savetxt('test_data.csv', x_test, delimiter=',')
np.savetxt('train_labels.csv', y_train,delimiter=",")
np.savetxt('test_labels.csv', y_test,delimiter=",")
