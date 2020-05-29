# -*- coding: utf-8 -*-
"""
Created on Thu May 28 22:23:48 2020

@author: Andrew
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('ggplot')

df = pd.read_csv(r"C:\Users\Andrew\Documents\Python Scripts\data set\nyc open data\NYC_Business_Acceleration_Businesses_Served_and_Jobs_Created.csv")
df = df.fillna(0)

bad_values = ['2/27/2015', '12/2/2013', '8/24/2015','5/11/2015', '3/5/2015']
df = df[~df["Number Of Employees"].isin(bad_values)]
df["Number Of Employees"] = df["Number Of Employees"].astype('int64')

fig, ax = plt.subplots(figsize = (10,10))
sns.barplot(x=df["Establishment Borough"], y = df["Number Of Employees"], hue = df["Business Sector"]
            , ax = ax, ci = None)