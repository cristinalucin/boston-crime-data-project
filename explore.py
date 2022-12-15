import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats
import datetime as dt



##------------------------Train-Test Split----------------------##

def train_validate_test_split(df):
    '''This function splits the dataframe by taking two years of data for train 
    (March 2017-March 2019) and validate from the year immediately preceding the pandemic
    (March 2019-March 2020). Finally, it uses test data from when the majority of lockdown 
    restrictions were lifted in the city of Boston (March 2021 onward). It includes only 
    the target of 'count_of_crime', where each row is the total count of fraud crimes occuring
    on that day, and returns train, validate, and test dataframes'''
    #Grouping the data by day
    df = df.groupby(['date']).sum()
    #Creating a DF with only the target
    df = df[['count_of_crime']]
    #Performing the split
    # ### Performing new train-test split
    train = df.loc['2017-03-14':'2019-03-15']
    validate = df.loc['2019-03-16':'2020-03-16']
    test = df.loc['2020-03-16': '2021-03-15']
    
    return train, validate, test

##--------------------Visualizations--------------------------##

def monthly_fraud_viz(fraud_df):
    '''This function visualizes mean fraud crimes by month'''
    #Aggregate sum of fraud by day
    fraud_df = fraud_df.groupby(['date']).sum()
    #Create series with just target variable
    y = fraud_df.count_of_crime
    #Resampled by month, average taken
    y.resample('M').mean().plot(figsize=(12,8), color='cornflowerblue')
    #Set style
    sns.set_style("darkgrid")
    #Plot it
    plt.title('Mean Fraud Crimes Resampled by Month', fontsize='18')
    plt.xlabel('Date')
    plt.ylabel('Average Fraud Crimes')
    #Set V lines and annotation for pandemic
    plt.axvline(dt.datetime(2020, 3, 15), color='tab:red', linestyle= '--')
    plt.axvline(dt.datetime(2021, 3, 15), color='tab:red', linestyle= '--')
    plt.text(dt.datetime(2019,2,15), 15, 'Lockdown Began')
    plt.text(dt.datetime(2021,4,15), 15, 'Lockdown Ended')
    plt.show()
    
def train_test_viz(train, validate, test):
    '''This function visualizes the train, validate, test split utilized in modeling'''
    #Set Style
    sns.set_style('darkgrid')
    # change the figure size
    plt.figure(figsize=(12,8))
    plt.title('Distribution of Train, Test, and Validate', fontsize='18')
    #Plot it
    plt.plot(train.index, train.count_of_crime, color='powderblue')
    plt.plot(validate.index, validate.count_of_crime, color='lightskyblue')
    plt.plot(test.index, test.count_of_crime, color='dodgerblue')
    #Label Axes
    plt.xlabel('Date')
    plt.ylabel('Count of Fraud Crimes')
    #Annotation
    plt.axvline(dt.datetime(2020, 3, 15), color='crimson', linestyle= '--')
    plt.text(dt.datetime(2019,1,30), 25, 'COVID Pandemic Begins')
    plt.show()