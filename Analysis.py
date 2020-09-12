# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 12:16:17 2020

@author: ghw27
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from collections import Counter

GAS_PRICE = 112.9
INTERNET_PRICE = 89.95

def get_week_end_date(date):
    
    day = date.weekday()
    
    day_dif = 6 - day
    
    return date + dt.timedelta(days = day_dif)

# Load data
filename = 'statement.csv'
data  = pd.read_csv(filename)

#Turning dates into datetime datatype
data.Date = pd.to_datetime(data.Date, format='%d/%m/%Y')

#Replacing all dates to be end of that week
for i in range(0, len(data)):
    
    data.Date[i] = get_week_end_date(data.Date[i])
    

num_weeks = len(Counter(data.Date))

current_total = 0 # Current total in account
current_total_arr = [] # array for account buffer after rent is payed
current_week = data.Date[0]

week_end_date_arr = [] # array of the date that the week ended
weekly_expenses_arr = [] # array of weekly expenses
weekly_data_arr = []


week_index = 0
for i in range(0, num_weeks - 1):
    
    #Getting data for the current week
    weekly_data = data[data.Date == current_week]
    weekly_data_arr.append(weekly_data)
    
    #Keeping a runnning total for the buffer
    current_total += sum(weekly_data.Amount)
    current_total_arr.append(current_total)    
    
    #Getting expenses as all non-rent outgoings in the account
    expenses = weekly_data.Amount[((weekly_data.Amount < 0) & (weekly_data.Amount != -800))]
    weekly_expenses_arr.append(abs(sum(expenses)))
    
    #Append the current week to week_end_date arr
    week_end_date_arr.append(current_week)
    
    #Go to next week
    while data.Date[week_index] == current_week:
        week_index += 1
    
    current_week = data.Date[week_index]
    
       

plt.figure(figsize = (18,18))
plt.plot_date(week_end_date_arr, current_total_arr, '-')
plt.plot_date(week_end_date_arr, weekly_expenses_arr, '-')
plt.show()
    

