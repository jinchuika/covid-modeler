from .base_model import BaseModel

import numpy as np
from sklearn.linear_model import LinearRegression


class LinearModel(BaseModel):
    plot_name = 'Linear'

    def train(self):
        x, y = np.reshape(self.x_train, (-1, 1)), np.reshape(self.y_train, (-1, 1))
        self.model = LinearRegression().fit(x, y)
        self.is_trained = True

    def predict(self):
        y_pred = self.model.predict(self.x_pred.reshape(-1, 1))
        self.y_pred = y_pred.reshape(y_pred.size)
        self.is_predicted = True
