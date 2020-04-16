import warnings

import numpy as np
from scipy.optimize import curve_fit

from .base_model import BaseModel

class ExponentialModel(BaseModel):
    plot_name = 'Exponential'

    @staticmethod
    def exponential(t, a, b, c):
        return a * np.exp(b * t) + c
    
    def train(self):
        epopt, epcov = curve_fit(self.exponential, self.x_train, self.y_train, maxfev=10000)
        lerror = np.sqrt(np.diag(epcov))

        # for exponential curve at half maximum, slope = growth rate/2. so doubling time = ln(2) / (growth rate/2)
        edoubletime = np.log(2) / epopt[1]
        # standard error
        edoubletimeerror = 1.96 * edoubletime * np.abs(lerror[1] / epopt[1])

        # calculate R^2
        residuals = self.y_train - self.exponential(self.x_train, *epopt)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((self.y_train - np.mean(self.y_train)) ** 2)
        exponentialr2 = 1 - (ss_res / ss_tot)
        
        self.epopt = epopt
        
        if exponentialr2 > 0.95:
            self.log(f'\n** Ajuste exponencial**\n')
            self.log(f'\tR^2: {round(exponentialr2, 5)}')
            self.log(f'\tTiempo para duplicarse (ritmo actual): {round(edoubletime, 2)} (± {round(edoubletimeerror, 2)}) días')
        else:
            warning_message = f'Exponential model is trained but the results might be inaccurate, as the R2 value is {exponentialr2}'
            warnings.warn(warning_message)
        
        self.r2 = exponentialr2
        
        self.is_trained = True
    
    def predict(self):
        self.y_pred = self.exponential(self.x_pred, *self.epopt)
        self.is_predicted = True
