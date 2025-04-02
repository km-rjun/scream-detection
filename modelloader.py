from tensorflow import keras
import pandas as pd
from scipy.io.wavfile import read
def process_file(filename):
    arr = []
    model = keras.models.load_model('.')
    print(filename)
    data, rs = read(filename)
    file = open("input dimension for model.txt", "r")
    suitable_length_for_model = int(file.read())
    file.close()
    rs = rs.astype(float)
    rs = rs[0:suitable_length_for_model+1]
    a = pd.Series(rs)
    arr.append(a)
    df = pd.DataFrame(arr)
    X2 = df.iloc[0:, 1:]
    #print(X2)
    predictions = model.predict(X2)
    rounded = [round(x[0]) for x in predictions]

    #print("predicted value is" + str(rounded))
    if str(rounded)=='[1.0]':
        return True
    else:
        return False
print(process_file("/home/rjun/scream-detection/positive/damm_6.wav"))
#model = keras.models.load_model('.')
#print('hi')
#df = pd.read_csv('newresources.csv', index_col=0, engine = 'c')



#row_num_for_verification_of_model = 154
#X2 = df.iloc[row_num_for_verification_of_model:row_num_for_verification_of_model+1,1:]
#X2 = df.iloc[row_num_for_verification_of_model:,1:]
#predictions = model.predict(X2)

# round predictions
#rounded = [round(x[0]) for x in predictions]

#print("predicted value is"+str(rounded))
#print("actual value was"+str(list(df.iloc[row_num_for_verification_of_model:,0])))
