# dataset for this model can be easily prepare by datasetmaker.py file
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense
df = pd.read_csv('newresources.csv', index_col=0, engine = 'c')
file = open("begining index of testing files.txt","r")
data1 = int(file.read())
file.close()
row_num_for_verification_of_model = data1
X = df.iloc[:row_num_for_verification_of_model,1:]  #independent variables columnns
print(row_num_for_verification_of_model)
X2 = df.iloc[row_num_for_verification_of_model:,1:]
file = open("input dimension for model.txt","r")
data2 = int(file.read())
file.close()
print(data2)
total_number_of_column_required_for_prediction = data2
column_number_of_csv_having_labels = 0
y = df.iloc[:data1,column_number_of_csv_having_labels] # dependent variable column
# # define the keras model
model = Sequential()
model.add(Dense(12, input_dim=total_number_of_column_required_for_prediction, activation='relu'))
model.add(Dense(8, activation='relu'))

model.add(Dense(10, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(3, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
history = model.fit(X, y,validation_split=0.33, epochs=150, batch_size=50

                    )


# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy * 100))

# make probability predictions with the model
predictions = model.predict(X2)

# round predictions
rounded = [round(x[0]) for x in predictions]

print("predicted value is"+str(rounded))
print("actual value was"+str(list(df.iloc[row_num_for_verification_of_model:,column_number_of_csv_having_labels])))

model.save('.')
