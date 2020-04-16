from datetime import datetime, timedelta

import pandas as pd
import numpy as np


class CountryData:

    def __init__(self):
        self.download()

    def download(self):
        self.df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

    def get_country(self, country, dates=True):
        co = self.df[self.df['Country/Region'] == country].iloc[:,4:].T.sum(axis = 1)
        co = pd.DataFrame(co)
        co.columns = ['Cases']
        co = co.loc[co['Cases'] > 0]

        y = np.array(co['Cases'])
        x = np.arange(y.size)
        if dates:
            start_date = pd.to_datetime(co.index[0], dayfirst=True)
            end_date = pd.to_datetime(co.index[-1], dayfirst=True)
            x_range = np.array([str(d.date()) for d in pd.date_range(start_date, end_date)])
            return np.array([x, y, x_range])
        return np.array([x, y])
    
    def show_countries(self, start=None):
        if start:
            return self.df[self.df['Country/Region'].str.lower().str.contains(start.lower())]['Country/Region'].unique().tolist()
        else:
            return self.df['Country/Region'].unique().tolist()
