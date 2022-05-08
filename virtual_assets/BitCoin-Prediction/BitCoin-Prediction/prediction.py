# Necessary Packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot

# Bitcoin data
data1 = pd.read_csv('bitcoin.csv', header=0)

# 데이터 프레임, 처음 10개 요소 시각화
print(data1.head(4150))

# 그래픽 표현
data1.plot()
plt.show()

# read data again
series = read_csv('bitcoin.csv', header=3370, index_col=0)
from statsmodels.graphics.tsaplots import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
pyplot.figure()
pyplot.subplot(211)
plot_acf(series, ax=pyplot.gca(),lags=30)
pyplot.subplot(212)
plot_pacf(series, ax=pyplot.gca(),lags=30)
pyplot.show()

# 시계열의 반환값 또는 첫 번째 차이
returns=series.diff()
returns.plot()
plt.show()
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
model = pm.auto_arima(series, start_p=1, start_q=1, test='adf', max_p=6, max_q=6, m=1, d=None, seasonal=False, start_P=0, D=0,
                      trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
print(model.summary())
# 시리즈에 ARIMA 모델을 적용
model = ARIMA (series, order=(1,1,1))
model_fit = model.fit(disp=0)
print(model_fit.summary())

# 플롯 잔차 오차
residuals = DataFrame(model_fit.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()
print(residuals.describe())
print(model_fit.aic)

# Actual vs Fitted
def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual)) # MAPE
    me = np.mean(forecast - actual) # ME
    mae = np.mean(np.abs(forecast - actual)) # MAE
    mpe = np.mean((forecast - actual)/actual) # MPE
    rmse = np.mean((forecast - actual)**2)**.5 # RMSE
    corr = np.corrcoef(forecast, actual)[0,1] # corr
    mins = np.amin(np.hstack([forecast[:,None],actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None],actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs) # minmax
    #acf1 = acf(fc-test)[1] # ACF1
    return({'mape':mape, 'me':me, 'mae': mae,'mpe': mpe, 'rmse':rmse,'corr':corr, 'minmax':minmax})
yy=model_fit.predict(652)
xx=series.iloc[652:781,0]
tt=forecast_accuracy(yy, xx)
print('forecast accuracy',tt)
pyplot.figure()
plt.scatter(xx,yy, marker='o')
pyplot.show()
pyplot.figure()
model_fit.plot_predict(652,781)
model_fit.plot_predict(dynamic=False)
pyplot.show()

# 훈련 데이터와 테스트 데이터의 분리 (95% and 5%)
forecast3, stderr, conf_int = model_fit.forecast(10)
print(forecast3)
pyplot.plot(forecast3,color='green')
pyplot.show()
pyplot.figure()
model_fit.plot_predict(752,791)
pyplot.show()
from math import sqrt
from sklearn.metrics import mean_squared_error
rms = sqrt(mean_squared_error(yy,xx))
print('RMSE', rms)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.seasonal import seasonal_decompose
# Bitcoin data
data = pd.read_csv('bitcoin.csv')
# 훈련 세트와 검증 세트로 나눕니다.
train = data[:int(0.835*(len(data)))]
valid = data[int(0.835*(len(data))):]

#preprocessing (arima는 일변량 급수를 입력으로 사용하기 때문에)
train.drop('Date',axis=1,inplace=True)
valid.drop('Date',axis=1,inplace=True)
#plotting the data
train['bprice'].plot()
valid['bprice'].plot()
#building the model
from pmdarima import auto_arima
model = auto_arima(train, suppress_warnings=True)
model.fit(train)
trace=True,
error_action='ignore',
forecast = model.predict(n_periods=len(valid))
forecast = pd.DataFrame(forecast,index = valid.index,columns=['Prediction'])

# 검증 세트에 대한 예측 플롯
pyplot.figure()
plt.figure(figsize=(10, 6))
plt.plot(train, label='Train')
plt.plot(valid, label='Valid')
plt.plot(forecast, label='Prediction')
plt.show()

# rmse 계산
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
rms1 = sqrt(mean_squared_error(valid,forecast))
print('RMSE',rms1)
print('MAE', mean_absolute_error(valid, forecast))
