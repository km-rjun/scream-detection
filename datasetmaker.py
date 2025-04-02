# this file is made for sound_classifier_nueral.py
# positive sound mean the sound that we want to predict
# negative sound mean sound except positive sound
import time
import psutil
import numpy as np
import pandas as pd
import os,threading
from scipy.io.wavfile import read
import os

class scream():

    def adder(self):
        ################################  getting negative sounds #################################################
        files = os.listdir('negative')
        arr = []
        for i in files:
            num = float(0)  # assigning labels to negative sounds
            i = 'negative/'+i
            try:
                data, rs = read(i)
                print(psutil.virtual_memory())
            except:
                print("removed "+i)
                os.remove(i)
                continue
            try:
                rs = rs.astype(float)
                rs = np.insert(rs,0,num)
                a = pd.Series(rs)
                arr.append(a)
                self.ctr+=1
            except:
                pass
        ########################################### end ###############################################

        ############################# getting positive sounds ######################################
        files = os.listdir('positive')
        for i in files:
            num = float(1)  # assigning labels to positive sounds
            i = 'positive/' + i
            try:
                data, rs = read(i)
                print(psutil.virtual_memory())
            except:
                print("removed "+i)
                os.remove(i)
                continue
            try:
                rs = rs.astype(float)
                rs = np.insert(rs, 0, num)
                a = pd.Series(rs)
                arr.append(a)
                self.ctr+=1
            except:
                pass

        self.starting_index_not_to_be_shuffled = self.ctr


        file = open("begining index of testing files.txt","w")
        file.write(str(self.ctr))
        file.close()


        print(str(self.ctr)+" have been added ")
        time.sleep(1)
        ########################################### end ##########################

        #################### loading testing sounds #########################
        files = os.listdir('testing')
        for i in files:
            if i.startswith("1"):
                num = float(1)
            else:
                num = float(0)

            i = 'testing/' + i
            try:
                data, rs = read(i)
                print(psutil.virtual_memory())
            except:
                print("removed "+i)
                os.remove(i)
                continue
            try:
                rs = rs.astype(float)
                rs = np.insert(rs, 0, num)
                a = pd.Series(rs)
                arr.append(a)
                self.ctr += 1
            except:
                pass
        print(psutil.virtual_memory())
        ############################### end ############################
        df = pd.DataFrame(arr)
        print(psutil.virtual_memory())
        df = df.dropna(axis=1)  ### removing columns containg null or NA
        df.to_csv('resources.csv')
    def __init__(self):
        self.ctr = 0
        self.starting_index_not_to_be_shuffled = 0
        self.adder()
        start_time = time.time()
        print('started')
        self.df = pd.read_csv('resources.csv', index_col=0, engine = 'c')
        print("without shuffling dataset contains "+str(len(self.df))+" rows and "+str(len(self.df.columns))+" columns")
        self.df.iloc[:self.starting_index_not_to_be_shuffled,:] = self.df.iloc[:self.starting_index_not_to_be_shuffled,:].sample(frac=1).reset_index(drop=True) # shuffling dataframe
        print("after shuffling dataset contains " + str(len(self.df)) + " rows and " + str(len(self.df.columns)) + " columns")
        self.df.to_csv('newresources.csv') # shuffled dataset
        print(self.df)

        file = open("input dimension for model.txt","w")
        file.write(str(len(self.df.columns)-1))
        file.close()

        print("\nwhole process takes %s seconds" % (time.time()-start_time))

scream()