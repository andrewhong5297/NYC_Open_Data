# -*- coding: utf-8 -*-
"""
Created on Thu May 28 22:53:52 2020

@author: Andrew
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import datetime

plt.style.use('ggplot')

# df = pd.read_csv(r"C:\Users\Andrew\Documents\Python Scripts\data set\nyc open data\311_Service_Requests_from_2019_to_Present.csv")
# df["time to close out"] = df["Closed (Date Only)"] - df["Created (Date Only)"]
# df = df[pd.notnull(df["time to close out"])]
# df["time to close out"] = df["time to close out"].dt.days

# df.to_pickle(r'C:\Users\Andrew\Documents\Python Scripts\data set\nyc open data\311_Service_Requests_from_2019_to_Present.pkl')

df = pd.read_pickle(r'C:\Users\Andrew\Documents\Python Scripts\data set\nyc open data\311_Service_Requests_from_2019_to_Present.pkl')

'''some exploration of data'''
df["Agency"].value_counts()
(df["Borough"].value_counts()[:10]/df.shape[0]).plot(kind="bar", figsize= (10,10))

(df[df["Agency"]=='NYPD']['Descriptor'].value_counts()/df.shape[0]).plot(kind="bar", figsize= (10,10))

# fig, ax = plt.subplots(figsize = (10,10))
# sns.barplot(x=df["Establishment Borough"], y = df["Number Of Employees"], hue = df["Business Sector"]
#             , ax = ax, ci = None)

'''What's happened to 311 calls since Covid Started?'''
pivot = df.pivot_table(index="Descriptor", columns = "Borough", values = "Unique Key", aggfunc = "count")
pivot = pivot.sort_values(by=['BRONX'],ascending=False)
pivot.iloc[:10,:5].plot(kind="bar", figsize=(10,10)).set(title="Number of Complaints by Type and Borough", ylabel = "Count")


pivot = df.pivot_table(index="Created (Date Only)", columns = "Borough", values = "Unique Key", aggfunc = "count")
pivot = pivot.rolling(7).mean()
pivot.iloc[-300:,:5].plot(kind="line", figsize=(10,10)).set(title="Number of Complaints by Borough", ylabel = "Count")

pivot = df[df["Created (Date Only)"] <= datetime.date(2020, 2, 27)].pivot_table(index="Created (Hour Only)", columns = "Descriptor", values = "Unique Key", aggfunc = "count")
pivot = pivot.T
pivot = pivot.sort_values(by=pivot.columns[-1],ascending=False)
pivot = pivot.T
# pivot = pivot.rolling(7).mean()
pivot.iloc[:,0:4].plot(kind="line", figsize=(10,10)).set(title="Number of Complaints by Type", ylabel = "Count")

'''who is partying?'''
pivot = df[df["Created (Date Only)"] >= datetime.date(2020, 2, 27)].pivot_table(index="Descriptor", columns = "Borough", values = "Unique Key", aggfunc = "count")
pivot = pivot.sort_values(by=['BRONX'],ascending=False)
pivot.iloc[:10,:5].plot(kind="bar", figsize=(10,10)).set(title="Number of Complaints by Type and Borough", ylabel = "Count")


'''What's happened to how long it takes to get a response or close?'''
pivot = df[df["Created (Date Only)"] <= datetime.date(2020, 2, 27)].pivot_table(index="Created (Hour Only)", 
                       columns = "Borough", values = "time to close out", aggfunc = np.mean)
# pivot = pivot.rolling(7).mean()
pivot.iloc[:,:5].plot(kind="line", figsize=(10,10)).set(title="Days to Close Out Complaint", ylabel = "Days")


'''GIS plotting'''
descriptors = ["Social Distancing"]
plot_df = df[df["Descriptor"].isin(descriptors)]

BBox = ((df.Longitude.min(),   df.Longitude.max(),      
         df.Latitude.min(), df.Latitude.max()))

#map from openstreetmap
ruh_m = plt.imread(r'C:\Users\Andrew\Documents\Python Scripts\Medium Charts\NYC Open Data\StreetMap.png')
        
fig, ax = plt.subplots(figsize = (10,10))
sns.scatterplot(x = plot_df["Longitude"], y = plot_df["Latitude"]
                , hue = plot_df["Descriptor"], alpha = 0.2, ax = ax,zorder = 10,
                size = 0.1)
ax.set_title('Plotting Complaint Data on NYC Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'auto')
