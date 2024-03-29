import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('TSLA.csv')
print(df.shape)
df = df['Open'].values
df = df.reshape(-1, 1)
print(df.shape)
dataset_train = np.array(df[:int(df.shape[0]*0.8)])
dataset_test = np.array(df[int(df.shape[0]*0.8):])
print(dataset_train.shape)
print(dataset_test.shape)
from sklearn.preprocessing import MinMaxScaler#scikit-learn
from keras.models import Sequential, load_model#keras,tensorflow
from keras.layers import LSTM, Dense, Dropout
scaler = MinMaxScaler(feature_range=(0,1))
dataset_train = scaler.fit_transform(dataset_train)
print(dataset_train[:5])
dataset_test = scaler.transform(dataset_test)
print(dataset_test[:5])
def create_dataset(df):
    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i-50:i, 0])
        y.append(df[i, 0])
    x = np.array(x)
    y = np.array(y)
    return x,y
x_train, y_train = create_dataset(dataset_train)
x_test, y_test = create_dataset(dataset_test)
model = Sequential()
model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96))
model.add(Dropout(0.2))
model.add(Dense(units=1))
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1, batch_size=32)
model.save('stock_prediction.h5')
model = load_model('stock_prediction.h5')
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))
from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

# plot function is created for 
# plotting the graph in 
# tkinter window
def plot():

    fig, ax = plt.subplots(figsize=(16,8))
    ax.set_facecolor('#000041')
    ax.plot(y_test_scaled, color='red', label='Original price')
    plt.plot(predictions, color='cyan', label='Predicted price')
    plt.legend()
    plt.xlabel('Days')
    plt.ylabel('Stock Price')
   ### matplotlib.pyplot.title('c')

    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()
  
# the main Tkinter window
window = Tk()
  
# setting the title 
window.title('Stock Prediction')
  
# dimensions of the main window
window.geometry("500x500")
  
# button that displays the plot
plot_button = Button(master = window, 
                     command = plot,
                     height = 2, 
                     width = 50,
                     text = "Predict the Tesla Stock")
  
# place the button 
# in main window
plot_button.pack()
  
# run the gui
window.mainloop()
