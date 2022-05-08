# Loading the data and the preprocessing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from math import sqrt
# Bitcoin data
df = pd.read_csv('bitcoin.csv')
# visualize the data frame, first 10 elements
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index(['Date'], drop=True)
df.head(10)

#graphical representation
plt.figure(figsize=(10, 6))
plt.title('Bitcoin price')
df['bprice'].plot();
split_date = pd.Timestamp('2020-04-1')
df = df['bprice']
trainf = df.loc[:split_date]
testf = df.loc[split_date:]
train2d = testf.values.reshape(-1,1)
test2d = testf.values.reshape(-1,1)
plt.figure(figsize=(10, 6))
ax = trainf.plot()
testf.plot(ax=ax)
plt.legend(['train', 'test'])
plt.title('Bitcoin Price train vs test')
plt.show()
plt.figure(figsize=(10, 6))
plt.title('Bitcoin Price test')
testf.plot();
plt.show()
prices = read_csv('bitcoin.csv', header=0, index_col=0)
prices.head()
seq_length = 265
minMax = MinMaxScaler()
X = minMax.fit_transform(prices)
X = X.squeeze()
x = []
y = []
for i in range(len(prices) - seq_length):
    x.append(X[i: i+(seq_length)-1])
    y.append(X[i+(seq_length)-1])
x = np.array(x)
y = np.array(y)
x_train, x_test, y_train, y_test= train_test_split(x, y)
print(x_train.shape)
print(x_test.shape)
print(y_test.shape)
print(y_train.shape)
x_train = x_train.reshape(-1, seq_length-1,1)
x_test = x_test.reshape(-1, seq_length-1,1)

# # Model building and training
import keras
from keras.layers import Input, LSTM, Activation, Dense
from keras.models import Sequential, Model
from keras.callbacks import LearningRateScheduler
model = Sequential()
input_data = Input((seq_length - 1, 1))
X = LSTM(160, recurrent_dropout= 0.5)(input_data)
X = Dense(1)(X)
model = Model(input_data, X)
model.compile(loss='mse', optimizer='adam')
def reduce(epoch, lr):
    if epoch%10 == 0:
        return lr
    return lr
scheduler = LearningRateScheduler(reduce)
history = model.fit(x_train, y_train, epochs=100, validation_split=0.2)
pyplot.figure()
plt.figure(figsize=(10, 6))
plt.plot(list(history.history['val_loss']))
plt.show()
pyplot.figure()
plt.figure(figsize=(10, 6))
plt.plot(list(history.history['loss']))
plt.show()
#Testing
predictions = model.predict(x_test)
from math import sqrt
rms1 = (sqrt(mean_squared_error(y_test, predictions)))
print('MAE1', mean_absolute_error(y_test, predictions))
print('RMSE1', rms1)
mape1 = np.mean(np.abs(predictions - y_test)/np.abs(y_test))
print('MAPE1', mape1)
pyplot.figure()
plt.figure(figsize=(10, 6))
plt.scatter(y_test,predictions, marker='o')
plt.show()
pred = minMax.inverse_transform(predictions)
#y_test=y_test.reshape(-1,1)
pred = pred.squeeze()
# test loss using mean absolute error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from math import sqrt
y1_test=minMax.inverse_transform(y_test.reshape(-1,1))
y1_test=y1_test.squeeze()
rms = (sqrt(mean_squared_error(y1_test, pred)))
print('MAE',mean_absolute_error(y1_test, pred))
print('RMSE', rms)
mape = np.mean(np.abs(pred - y1_test)/np.abs(y1_test))
print('MAPE', mape)
corr = (np.corrcoef(pred, y1_test)[0,1])
print('Corr' , corr)
#print(y1_test-pred)
mean=np.mean(y1_test)
print('mean', mean)
pyplot.figure()
plt.figure(figsize=(10, 6))
plt.scatter(y1_test,pred, marker='o')
plt.show()
pyplot.figure()
plt.figure(figsize=(10, 6))
plt.plot(y1_test)
plt.plot(pred)
plt.show()
# plotting subset from the data
pyplot.figure()
plt.figure(figsize=(10, 6))
p = model.predict(x[414:543].reshape(-1, seq_length-1, 1))
p = minMax.inverse_transform(p)
p = p.squeeze()
plt.plot(p)
plt.plot(minMax.inverse_transform(y[414:543].reshape(1,-1)).squeeze())
plt.show()
# ploting data of the past 2 years
pyplot.figure()
plt.figure(figsize=(10, 6))
p = model.predict(x.reshape(-1, seq_length-1, 1))
p = minMax.inverse_transform(p)
p = p.squeeze()
pyplot.figure()
plt.figure(figsize=(10, 6))
plt.plot(p)
plt.plot(minMax.inverse_transform(y.reshape(-1,1)).squeeze())
plt.show()