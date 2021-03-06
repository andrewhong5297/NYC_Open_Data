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

# df["Created (Date Only)"] = df["Created Date"].dt.date
# df["Closed (Date Only)"] = df["Closed Date"].dt.date
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
pivot = df.pivot_table(index="Created (Date Only)", 
                       columns = "Borough", values = "time to close out", aggfunc = np.mean)
pivot = pivot.rolling(7).mean()
pivot.iloc[:,:5].plot(kind="line", figsize=(10,10)).set(title="Days to Close Out Complaint", ylabel = "Days")

pivot = df[df["Created (Date Only)"] <= datetime.date(2020, 2, 27)].pivot_table(index="Created (Hour Only)", 
                       columns = "Borough", values = "time to close out", aggfunc = np.mean)
# pivot = pivot.rolling(7).mean()
pivot.iloc[:,:5].plot(kind="line", figsize=(10,10)).set(title="Days to Close Out Complaint", ylabel = "Days")


'''GIS plotting GIF'''
descriptors = ["Social Distancing"]
plot_df = df[df["Descriptor"].isin(descriptors)]

BBox = ((df.Longitude.min(),   df.Longitude.max(),      
         df.Latitude.min(), df.Latitude.max()))

#map from openstreetmap
ruh_m = plt.imread(r'C:\Users\Andrew\Documents\Python Scripts\Medium Charts\NYC Open Data\StreetMap.png')
        
import glob
import moviepy.editor as mpy
from collections import OrderedDict

#mapping consistent colors
unique = plot_df["Descriptor"].unique()
cmap = plt.cm.get_cmap('Set1')
cmap = [cmap(0.1),cmap(0.2),cmap(0.3),cmap(0.4),cmap(0.5)]
palette = dict(zip(unique, cmap))

dates = df["Created (Date Only)"].unique()
for date in dates[-70:]:
    fig, ax = plt.subplots(figsize = (10,10))
    plot_df_single_day = plot_df[plot_df["Created (Date Only)"] == date]
    
    #plotting nyc complaints
    sns.scatterplot(x = plot_df_single_day["Longitude"], y = plot_df_single_day["Latitude"]
                , hue = plot_df_single_day["Descriptor"], alpha = 0.7, ax = ax,zorder = 10,
                size = 0.1, palette = palette)
    
    #plotting nyc arrests
    
    #creating legend that is consistent and doesn't repeat
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(sorted(zip(labels[1:-3], handles[1:-3])))    
    ax.legend(by_label.values(), by_label.keys(), loc = "upper left")
    
    ax.set_title('Social Distancing 311 Calls NYC on: ' + str(date))
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'auto')
    fig.savefig(r"C:\Users\Andrew\Documents\Python Scripts\Medium Charts\GIF creation\{}.png".format(date), quality = 85)

gif_name = 'COVID NYC 311 Social Distancing Calls'
fps = 6
file_list = glob.glob(r'C:\Users\Andrew\Documents\Python Scripts\Medium Charts\GIF creation\*')
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif(r'C:\Users\Andrew\Documents\Python Scripts\Medium Charts\GIF creation\{}.gif'.format(gif_name), fps=fps)