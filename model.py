import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import Holt, ExponentialSmoothing
from math import sqrt 


##-------------------------Train-Test Split-------------------------##

def post_pandemic_split(df):
    '''This function provides a new train test split based on the selection of test
    as crime reported post covid lockdown (March 2021 onwards)'''
    #Group data by day, sum the count of crime, create a new df
    new_df = df.groupby(['date']).sum()
    new_df = new_df[['count_of_crime']]
    ## Performing new train-test split
    train = new_df.loc['2017-03-14':'2019-03-15']
    validate = new_df.loc['2019-03-16':'2020-03-16']
    test = new_df.loc['2021-03-16':]
    
    return train, validate, test

##------------------------Model Evaluation--------------------------##

def evaluate_post_test(df, target_var):
    '''This function uses the simple average model to make predictions on test data,
    and returns the RMSE from this model'''
    #Splitting data
    train, validate, test = post_pandemic_split(df)
    #Make predictions from trainbased on simple average
    crime = round(train['count_of_crime'].mean(), 2)
    yhat_df = pd.DataFrame({'count_of_crime': [crime]}, index = test.index)
    #Calculate RMSE based on predictions
    rmse = round(sqrt(mean_squared_error(test[target_var], yhat_df[target_var])), 0)
    
    return rmse