import warnings

import numpy as np
from scipy.optimize import curve_fit

from .base_model import BaseModel

class LogisticModel(BaseModel):
    plot_name = 'Logistic'

    @staticmethod
    def logistic(t, a, b, c, d):
        return c + (d - c) / (1 + a * np.exp(- b * t))
    
    def train(self):
        lpopt, lpcov = curve_fit(self.logistic, self.x_train, self.y_train, maxfev=10000)
        lerror = np.sqrt(np.diag(lpcov))

        # for logistic curve at half maximum, slope = growth rate/2. so doubling time = ln(2) / (growth rate/2)
        ldoubletime = np.log(2) / (lpopt[1] / 2)
        # standard error
        ldoubletimeerror = 1.96 * ldoubletime * np.abs(lerror[1] / lpopt[1])

        # calculate R^2
        residuals = self.y_train - self.logistic(self.x_train, *lpopt)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((self.y_train - np.mean(self.y_train)) ** 2)
        logisticr2 = 1 - (ss_res / ss_tot)
        
        self.lpopt = lpopt
        
        if logisticr2 > 0.95:
            self.log(f'\n** Ajuste logistico**\n')
            self.log(f'\tR^2: {round(logisticr2, 5)}')
            self.log(f'\tTiempo para duplicarse (ritmo actual): {round(ldoubletime, 2)} (± {round(ldoubletimeerror, 2)}) días')
        else:
            warning_message = f'Logistic model is trained but the results might be inaccurate, as the R2 value is {logisticr2}'
            warnings.warn(warning_message)
        
        self.r2 = logisticr2
        self.is_trained = True
    
    def predict(self):
        self.y_pred = self.logistic(self.x_pred, *self.lpopt)
        self.is_predicted = True
