# This file is for stock price predection

# For downloading data
import yfinance as yf

# For manipulating data
import pandas as pd
import numpy as np

# For mathematical operations
import math

# For visualization
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

# For data normalisation
from sklearn.preprocessing import MinMaxScaler

# For building the model
from keras.layers import LSTM, Dropout, Dense
from keras.models import Sequential

#import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# # Settings the figsize parameter for the plots in this notebook to standardize the size of plots
#%matplotlib inline
rcParams['figure.figsize'] = 20, 10

ticker = 'MSFT'
df = pd.read_csv("data/historical_data13081.csv", index_col=1, parse_dates=True)
df.drop(columns=['Unnamed: 0'], inplace=True)

# Check the dataset
print(df.head())

# Plot the close price 
df['close'].plot()
plt.ylabel('Close price')
plt.title(f'Price history for {ticker}')
plt.show()

# Create a dataframe with just the close prices
df1 = df[['close']].copy()

# Check the filtered dataset
print(df1.head())

# Rename the column to close for convenience
df1.rename(columns={'close':'Close'}, inplace=True)

# Create an array called prices with the values of all the Close prices from the filtered dataframe.
prices = df1.values
print(prices)

# Computing the number of records we want in the training data set
train_len = math.ceil(len(prices) * 0.8)
print(train_len)

# Normalize the data to values between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(prices.reshape(-1, 1)[:train_len, :])
scaled_prices = scaler.transform(prices.reshape(-1, 1))

# Check the scaled prices array
print(scaled_prices)

# Create the training data set with the first n rows of the scaled prices
# n is the number of records required in the training data set, computed above

train_data = scaled_prices[0:train_len, :]

# Create an empty list for the feature data and label data
x_train, y_train = [], []

#Use previous 60 days To predict next day price
# Create a 60-days window of historical prices (i-60) as our feature data (x_train) and the following 60-days window as label data (y_train).
for i in range(60, len(train_data)):
    x_train.append(scaled_prices[i-60:i, 0])
    y_train.append(scaled_prices[i, 0])

# Convert the x_train and y_train into numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape into a three-dimensional array
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

#Extract the closing prices from our normalized dataset (the last 20% of the dataset).
#Similar to the training set, create feature data (x_test) and label data (y_test) from our test set.
#Convert the feature data (x_test) and label data (y_test) into Numpy array. Reshape again the x_test and y_test into a three-dimensional array
test_data = scaled_prices[train_len-60:, :]
x_test = []
y_test = prices[train_len:]

for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))


# Define the features and the labels
#  Define a Sequential model which consists of a linear stack of layers.
model = Sequential()

# Add a LSTM layer by giving it 100 network units. Set the return_sequence to true so that the output of the layer will be another sequence of the same length
model.add(LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))

# Add another LSTM layer with also 100 network units. But we set the return_sequence to false for this time to only return the last output in the output sequence
model.add(LSTM(100, return_sequences=False))

# Add a densely connected neural network layer with 25 network units
model.add(Dense(25))

# Add a densely connected layer that specifies the output of 1 network unit
model.add(Dense(1))

# Show the summary of our LSTM network architecture
model.summary()


#Training the LSTM Model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=3)


# Apply the model to predict the stock prices based on the test set
predictions = model.predict(x_test)
# Use the inverse_transform method to denormalize the predicted stock prices
predictions = scaler.inverse_transform(predictions)
# Apply the RMSE formula to evaluate the correctness of the predictions
rmse = np.sqrt(np.mean((predictions - y_test)**2))
print("Predicted Price RMSE:", rmse)   #RMSE = average prediction error in actual price units.

## Start .....Gemini added this code to predict the next day price 
# Predict the next day's stock price
# Get the last 60 days of closing prices
last_60_days = df1[-60:].values
# Scale the data to be values between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
# Create an empty list
X_test = []
# Append the past 60 days
X_test.append(last_60_days_scaled)
# Convert the X_test data set to a numpy array
X_test = np.array(X_test)
# Reshape the data
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
# Get the predicted scaled price
pred_price = model.predict(X_test)
# Undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(f"Predicted Price for the next day: {pred_price[0][0]}")

## end .....Gemini added this code to predict the next day price 


# Section 9: Visualizing the Predicted Prices

# Create a new dataframe for plotting
# The 'train' part will hold the data the model was trained on
# The 'validation' part will hold the actual prices and the model's predictions for the test set
data = df.filter(['close'])
train_data = data[:train_len]
validation_data = data[train_len:]
validation_data['Predictions'] = predictions

# Visualize the data
plt.figure(figsize=(16, 8))
plt.title(f'Model Prediction vs Actual Price for {ticker}')
plt.xlabel('Date', fontsize=14)
plt.ylabel('Close Price INR (₹)', fontsize=14)

# Plot the training and validation data
plt.plot(train_data['close'])
plt.plot(validation_data['close'])
plt.plot(validation_data['Predictions'])

# Add a clear legend
plt.legend(['Training Data', 'Actual Price (Test Set)', 'Predicted Price (Test Set)'], loc='lower right')

plt.show()

