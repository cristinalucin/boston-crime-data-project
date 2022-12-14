import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats



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