import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import Holt, ExponentialSmoothing
from math import sqrt 
import explore as e
import wrangle as w


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

def evaluate_holt(target_var):
    '''evaluate function to compute rmse for holt models'''
    #get clean data
    df = w.get_clean_data()
    #Create fraud df
    fraud_df = w.create_fraud_df(df)
    #Get train, validate, test
    train, validate, test = e.train_validate_test_split(fraud_df)
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse

def plot_and_eval(target_var):
    '''plots and evaluates RMSE for holt models'''
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label = 'Train', linewidth = 1)
    plt.plot(validate[target_var], label = 'Validate', linewidth = 1)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate_holt(target_var)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()
    
def append_eval_df(model_type, target_var):
    '''appends eval df for holt models'''
    rmse = evaluate_holt(target_var)
    d = {'model_type': [model_type], 'target_var': [target_var], 'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)

def evaluate_holt_models(train,validate,test):
    #Create eval df to place results
    eval_df = pd.DataFrame(columns=['model_type', 'target_var', 'rmse'])
    #Building place for predictions
    crime = train['count_of_crime'][-1:][0]
    yhat_df = pd.DataFrame({'count_of_crime': [crime]}, index = validate.index)
    
    #Holts Linear
    # Create the model object
    model_holt = Holt(train['count_of_crime'], exponential=False, damped_trend=True).fit(optimized=True)
    # make predictions for each date in validate 
    predictions_holt = model_holt.forecast(len(validate))
    #Set index to return date time
    predictions_holt.index=yhat_df.index
    # add predictions to yhat_df
    yhat_df['count_of_crime'] = round(predictions_holt, 2)
    #Place results in evaluate dataframe
    eval_df = append_eval_df(model_type = 'Holts', 
                             target_var = 'count_of_crime')
    
    #holts seasonal
    #fit
    fit1 = ExponentialSmoothing(train.count_of_crime, seasonal_periods=365, trend='add',
                            seasonal='add', use_boxcox=True).fit()
    #forecast
    predictions_holt_seasonal = fit1.forecast(validate.shape[0]).rename('count_of_crime').to_frame()
    #Set index
    predictions_holt_seasonal.index = yhat_df.index
    # add predictions to yhat_df
    yhat_df['count_of_crime'] = round(predictions_holt, 2)
    eval_df = append_eval_df(model_type = 'Holts seaonal add', 
                             target_var = 'count_of_crime')
    
    return eval_df

def eval_timeseries_models(train,validate,test):
    '''This function evaluates time series models, taking in train, validate
    and test, and producing a dataframe with their performances on train and validate data'''
    #Making predictions dataframes
    predictions_train = pd.DataFrame(index=train.index)
    predictions_validate = pd.DataFrame(index=validate.index)
    #Creating scores dataframe
    scores = pd.DataFrame(columns=['model_name', 'train_score', 'validate_score'])
    
    #Simple average
    avg_crime = round(train['count_of_crime'].mean(), 2)
    predictions_train['simple_average'] = avg_crime
    predictions_validate['simple_average'] = avg_crime
    RMSE_train = round(np.sqrt(mean_squared_error(train['count_of_crime'], predictions_train['simple_average'])))
    RMSE_validate = round(np.sqrt(mean_squared_error(validate['count_of_crime'], predictions_validate['simple_average'])))
    model_name='simple_average'
    scores.loc[len(scores)] = [model_name, RMSE_train, RMSE_validate]
    
    #Moving averages
    target = 'count_of_crime'
    period = 30
    ma = '30 d moving_average'
    rolling_count = round(train.count_of_crime.rolling(period).mean()[-1], 2)
    predictions_train[ma] = rolling_count
    predictions_validate[ma] = rolling_count
    RMSE_train = round(np.sqrt(mean_squared_error(train['count_of_crime'], predictions_train['30 d moving_average'])))
    RMSE_validate = round(np.sqrt(mean_squared_error(validate['count_of_crime'], predictions_validate['30 d moving_average'])))
    model_name='30 d moving_average'
    scores.loc[len(scores)] = [model_name, RMSE_train, RMSE_validate]
    
    period = 90
    ma = '90 d moving_average'
    rolling_count_90 = round(train.count_of_crime.rolling(period).mean()[-1], 2)
    predictions_train[ma] = rolling_count_90
    predictions_validate[ma] = rolling_count_90
    RMSE_train = round(np.sqrt(mean_squared_error(train['count_of_crime'], predictions_train['90 d moving_average'])))
    RMSE_validate = round(np.sqrt(mean_squared_error(validate['count_of_crime'], predictions_validate['90 d moving_average'])))
    model_name='90 d moving_average'
    scores.loc[len(scores)] = [model_name, RMSE_train, RMSE_validate]
    
    return scores

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