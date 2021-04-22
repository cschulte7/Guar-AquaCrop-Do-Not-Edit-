# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:01:04 2020

@author: carol
"""

import sys
import csv
_=[sys.path.append(i) for i in ['.', '..']] # finds 'AquaCrop' file

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns # Visualization tool used for high-level interface for drawing attractive and informative stastical graphics
import numpy as np
import pandas as pd
from aquacrop.core import *
from aquacrop.classes_Guar import *

# Reads in the weather data
weather = pd.read_csv('GuarWeather_Clovis_2018.csv') 
# Prepares the weather data that is in the csv to the format that the aquacrop code needs it in (ten spaces between each value)
with open('GuarWeather_Clovis_2018.txt', 'w') as f: weather.to_string(f, col_space = 10, index=False, justify = 'left') 
# Uses the function prepare weather to convert weather data
wdf = prepare_weather('GuarWeather_Clovis_2018.txt') 
# Grabs the soil class from the classes.py file
soil = SoilClass('ClayLoamGuar2018') 
# Prepares the crop class with the name of the crop, planting date, and harvest date
crop = CropClass('GuarGDD', PlantingDate='07/03',HarvestDate='11/16') 
# Initialize water content to be field capacity 
InitWC = InitWCClass(value=['FC']) 
# The model is run using SimStartTime, SimEndTime, weather data, soil, crop, initial water content
model = AquaCropModel('2018/07/03','2018/11/16', wdf,soil,crop, InitWC) 
model.initialize() 
model.step(till_termination=True)

# Allows for the outputs below to show all columns when printed
pd.set_option('max_columns', None) 
 # Daily Water Flux dataframe. The 'none' removes the limit from the output so all the data can be shown
FluxHead = model.Outputs.Flux.head(None)
# Soil-water content in each soil compartment dataframe
WaterHead = model.Outputs.Water.head(None) 
# Crop growth dataframe
GrowthHead = model.Outputs.Growth.head(None) 
# Final summary (seasonal total) dataframe
FinalHead = model.Outputs.Final.head(None) 

# The following are print statements to see different outputs
# Final summary (season total)
print('\n Final Summary = \n', FinalHead) 
# Daily water flux
print('\n Daily Water Flux = \n', FluxHead) 
 # Soil water content in each soil compartment
print('\n Soil Water Content = \n', WaterHead)
# Crop growth
print('\n Crop Growth = \n', GrowthHead) 

# Plotting canopy coverage over time (days after planting)
GrowthHead = GrowthHead[(GrowthHead.T != 0).any()]
plt1 = GrowthHead.plot(x ='DAP', y='CC', kind='line', label = 'With stress', title = 'Canopy Coverage over Time')
GrowthHead.plot(x ='DAP', y='CC_NS', kind='line', color = 'y', label = 'Without stress', ax=plt1)
plt1.set_ylabel("Canopy Coverage")
plt1.set_xlabel("Days After Planting (DAP)")

# Plotting biomass with no stress and stress conditions over time (days after planting) on the same graph
plt2 = GrowthHead.plot(x ='DAP', y='B_NS', kind='line', color = "k", label = 'Without stress', title = 'Biomass over Time')
GrowthHead.plot(x ='DAP', y='B', kind='line', color = "r", label='With stress', ax=plt2)
plt2.set_ylabel("Biomass (kg/ha)")
plt2.set_xlabel("Days After Planting (DAP)")
#Plot one less point 



