# -*- coding: utf-8 -*-
"""
Created on Fri May 29 00:37:47 2020

@author: Andrew
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import datetime
import glob 

arrest_df = pd.read_csv(r"C:\Users\Andrew\Documents\Python Scripts\data set\nyc open data\NYPD_Arrest_Data__Year_to_Date_.csv")
complaint_df = pd.read_csv(r"C:\Users\Andrew\Documents\Python Scripts\data set\nyc open data\NYPD_Complaint_Data_Historic.csv")
