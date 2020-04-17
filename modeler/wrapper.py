import os
from datetime import timedelta

import pandas as pd
import numpy as np

import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go

from . import countries, models

class Modeler:
    default_models = {
        'linear': models.LinearModel,
        'logistic': models.LogisticModel,
        'exponential': models.ExponentialModel
    }
    processed_models = {}

    record = ''

    def __init__(self, country=None, predict_len=15, use_default_models=True, mode='notebook', output_folder='output', plot_mode='image', show_plot=False):
        self.predict_len = predict_len
        self.c = countries.CountryData()
        if country is not None:
            self.set_country(country)
        if use_default_models:
            self.models = self.default_models
        
        # export options
        if mode not in ('notebook', 'cli'):
            raise RuntimeError('El modo debe ser `notebook` o `cli`')
        self.mode = mode
        self.output_folder = output_folder
        self.plot_mode = plot_mode
        self.show_plot = show_plot
    
    def log(self, text):
        self.record += text
    
    def process(self):
        self.record = ''

        if len(self.data[1]) >= 7:
            current = self.data[1].astype(int)[-1]
            lastweek = self.data[1].astype(int)[-8]
            
            if current > lastweek:
                self.log(f'Resultados para *{self.country_name}*')
                self.log('\n** Basado en los datos de la última semana **\n')
                self.log(f'\n\tCasos confirmados en {self.data[2][-1]} \t {current}')
                self.log(f'\n\tCasos confirmados en {self.data[2][-8]} \t {lastweek}')
                ratio = current / lastweek
                self.log(f'\n\tProporción: {round(ratio, 2)}')
                self.log(f'\n\tIncremento semanal: {round( 100 * (ratio - 1), 1)}%')
                dailypercentchange = round( 100 * (pow(ratio, 1/7) - 1), 1)
                self.log(f'\n\tIncremento diario: {dailypercentchange}% por día')
                recentdbltime = round( 7 * np.log(2) / np.log(ratio), 1)
                self.log(f'\n\tTiempo que tarda en duplicarse (al ritmo actual): {recentdbltime} días')
        
        for name, model in self.models.items():
            self.processed_models[name] = model(
                x_train=self.data[0],
                y_train=self.data[1],
                predict_len=self.predict_len,
                start_date=self.data[2][0]
            )
        
        self.create_record()
        self.plot()
        self.export()
    
    def set_country(self, country):
        self.data = self.c.get_country(country)
        self.country_name = country
    
    def create_record(self):
        best_r2 = 0
        best_model = ''
        for name, model in self.processed_models.items():
            self.log(model.record)
            if hasattr(model, 'r2') and model.r2 > best_r2:
                best_r2 = model.r2
                best_model = model.plot_name
        if best_r2 > 0:
            self.log(f"\nMejor modelo: {best_model} (R2 = {best_r2})")
        
    def plot(self):
        plot_data = []
        end_date = pd.to_datetime(self.data[2][0]).date() + timedelta(days=len(self.data[2]))
        original_data = go.Scatter(
            x=pd.date_range(start=str(self.data[2][0]), end=end_date),
            y=self.data[1],
            mode='markers',
            name='Casos confirmados'
        )
        plot_data.append(original_data)
        for name, model in self.processed_models.items():
            plot_data.append(model.chart)
        
        layout = dict(
            title = self.country_name,
            xaxis_type='date'
        )
        self.fig = go.Figure(data=plot_data, layout=layout)
    
    def export(self):
        if self.mode == 'notebook':
            print(self.record)
            self.fig.show()
            return
        
        # Crear la carpeta de destino
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)
        
        with open(os.path.join(self.output_folder, f'results_{self.country_name}.txt'), 'w', encoding='utf8') as output_file:
            print(self.record)
            output_file.write(self.record)
            print("******************************************")
            print(f"Resultados escritos en {output_file.name}")
            print("******************************************")
        
        # export the plot
        if self.plot_mode == 'image':
            self.export_image_plot()
        if self.plot_mode == 'html':
            self.export_html_plot()
    
    def export_image_plot(self):
        try:
            file_name = os.path.join(self.output_folder, f'results_{self.country_name}.png')
            self.fig.write_image(os.path.join(self.output_folder, f'results_{self.country_name}.png'))
            print(f'El gráfico fue exportado en {file_name}')
            if self.show_plot:
                self.fig.show()
        except ValueError as e:
            print("Hubo un error al exportar la imagen")
            print("Este error probablemente se debe a que se requiere la instalación de Orca para exportar imágenes")
            print("La guía de instalación se encuentra en: https://github.com/plotly/orca")
    
    def export_html_plot(self):
        file_name = os.path.join(self.output_folder, f'results_{self.country_name}.html')
        self.fig.write_html(file_name)
        print(f'El gráfico fue exportado en {file_name}')
        if self.show_plot:
            self.fig.show()
