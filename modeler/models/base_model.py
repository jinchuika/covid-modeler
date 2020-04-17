from datetime import timedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go


class BaseModel:
    use_dates = False
    is_trained = False
    is_predicted = False

    record = ''

    def __init__(self, x_train, y_train, predict_len=15, plot=True, plot_name='', start_date=None):
        self.x_train = np.asarray(x_train, dtype='float64')
        self.y_train = np.asarray(y_train, dtype='float64')

        self.x_pred = np.arange(x_train.size + int(predict_len))
        self.y_pred = np.array([])
        
        self.plot_name = self.get_plot_name()
        if start_date:
            self.set_date_range(start_date)

        self.train()
        self.predict()
        if plot:
            self.chart = self.plot()

    def get_plot_name(self):
        return self.plot_name

    def train(self):
        pass

    def predict(self):
        return
    
    def set_date_range(self, start_date):
        end_date = pd.to_datetime(start_date).date() + timedelta(days=self.x_pred.size - 1)
        self.date_range = pd.Series([str(d.date()) for d in pd.date_range(str(start_date), end_date)])
        self.use_dates = True
    
    def plot(self):
        if not self.is_predicted:
            raise RuntimeError('Model needs to be predicted before plotting. Please execute the `predict` method')

        x = self.date_range if self.use_dates else self.x_pred
        return go.Scatter(
            x=x,
            y=np.round_(self.y_pred),
            mode='lines',
            name=self.plot_name
        )
    
    def log(self, text):
        self.record += text
