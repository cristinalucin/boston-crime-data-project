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

def target_dist_viz(train):
    '''This function visualizes the distribution of the target variable (Count of
    Crimes) by visualizing its frequency in training data. X axis represents number of
    crimes reported by day'''
    #define y for plotting
    y = train.count_of_crime
    #Set style
    sns.set_style('darkgrid')
    #define font family to use for all text
    plt.rcParams['font.sans-serif'] = ['Verdana']
    #Distribution of target variable histogram
    fig, ax = plt.subplots(figsize =(9, 6))
    #Plot it
    y.plot.hist(color='paleturquoise',ec='gray')
    #Title
    plt.title('2017-2019 Distribution of Fraud Crimes Occuring Per Day', fontsize=20)
    #Annotation and labels
    dfmean = y.mean()
    plt.axvline(dfmean, color = 'indianred', linestyle=':', linewidth=2)
    ax.text(dfmean, 0.99, 'Mean', color='indianred', ha='right', va='top', rotation=90,fontsize=14,
            transform=ax.get_xaxis_transform())
    plt.xlabel('Daily Number of Fraud Crimes Occuring', fontsize=16)
    plt.ylabel('Frequency of Days', fontsize=16)
    plt.show()

def monthly_crime_hist(fraud_df):
    '''This function visualizes pre-pandemic fraud crime by month'''
    #grouping by day to aggregate
    fraud_df = fraud_df.groupby(['date']).sum()
    # ### Taking pre-pandemic data
    pre_pandemic = fraud_df.loc[:'2020-03-15']
    #Create y out of target variable
    y = pre_pandemic.count_of_crime
    #Set theme
    sns.set_style("darkgrid")
    #Plot it
    y.groupby(y.index.month).sum().plot.bar(figsize=(9,6), width=.9, ec='black', color='thistle')
    plt.xticks(rotation=0)
    plt.title('Pre-Pandemic Fraud Crimes are Lowest in April and May', fontsize=20)
    plt.xlabel('Month', fontsize=16)
    plt.ylabel('Count of Fraud Crimes', fontsize=16)
    plt.show()

def decomp_viz(fraud_df):
    '''This function visualizes a decomposition of all data prior to covid'''
    fraud_df = fraud_df.groupby(['date']).sum()
    # ### Performing train-test split
    train = fraud_df.loc[:'2019-03-14']
    y = train.count_of_crime.resample('W').mean()
    result = sm.tsa.seasonal_decompose(y)
    decomposition = pd.DataFrame({
    'y': result.observed,
    'trend': result.trend,
    'seasonal': result.seasonal,
    'resid': result.resid,
    })
    #Plot it
    sns.set_theme()
    decomposition.iloc[:, 1:].plot()
    plt.title('Some Seasonality is Present, with a Trend Down in 2017', fontsize=20)
    plt.xlabel('Date by Month', fontsize=16)
    plt.show()
    #Now plotting it separately
    result.plot()

def monthly_fraud_viz(fraud_df):
    '''This function visualizes mean fraud crimes by month'''
    #Aggregate sum of fraud by day
    fraud_df = fraud_df.groupby(['date']).sum()
    #Create series with just target variable
    y = fraud_df.count_of_crime
    #Resampled by month, average taken
    y.resample('M').mean().plot(figsize=(9,6), color='cornflowerblue')
    #Set style
    sns.set_style("darkgrid")
    #Plot it
    plt.title('Mean Fraud Crimes Resampled by Month', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Average Fraud Crimes', fontsize=16)
    #Set V lines and annotation for pandemic
    plt.axvline(dt.datetime(2020, 3, 15), color='tab:red', linestyle= '--')
    plt.axvline(dt.datetime(2021, 3, 15), color='tab:red', linestyle= '--')
    plt.text(dt.datetime(2018,10,15), 15, 'Lockdown Began', fontsize=14)
    plt.text(dt.datetime(2021,4,15), 15, 'Lockdown Ended', fontsize=14)
    plt.show()
    
def train_test_viz(train, validate, test):
    '''This function visualizes the train, validate, test split utilized in modeling'''
    #Set Style
    sns.set_style('darkgrid')
    # change the figure size
    plt.figure(figsize=(9,6))
    plt.title('Distribution of Train, Test, and Validate', fontsize='20')
    #Plot it
    plt.plot(train.index, train.count_of_crime, color='powderblue')
    plt.plot(validate.index, validate.count_of_crime, color='lightskyblue')
    plt.plot(test.index, test.count_of_crime, color='dodgerblue')
    #Label Axes
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Count of Fraud Crimes', fontsize=16)
    #Annotation
    plt.axvline(dt.datetime(2020, 3, 15), color='crimson', linestyle= '--')
    plt.text(dt.datetime(2018,11,30), 25, 'COVID Pandemic Begins', fontsize=14)
    plt.show()
    
##----------------------------Statistics---------------------------------##

def get_april_ttest(fraud_df):
    '''This function compares fraud rates in the month of April, pre-pandemic, to fraud rates
    of all other months'''
    #Making df of just april
    april_df = fraud_df[(fraud_df.month == 4) & (fraud_df.year < 2020)]
    #Now grouping by day
    april_df = april_df.groupby(['date']).sum()
    #Making a population df for stats test
    fraud_df= fraud_df.groupby(['date']).sum()
    #Create y out of target variable
    y = april_df.count_of_crime
    z = fraud_df.count_of_crime
    # Taking the mean for the t-test
    overall_population = z.mean()
    #Setting alpha and running the test
    alpha = 0.05
    t, p = stats.ttest_1samp(y, overall_population)
    
    return print(f't-statistic:{round(t,3)}, P-Value:{round(p/2,3)}, alpha={alpha}')

def get_2017_ttest(fraud_df):
    '''This function compares the mean of fraud crimes in 2017 to the mean of fraud crimes for the
    dataframe using a one-sample t-test'''
    #Separate 2017 values
    fraud_2017 = fraud_df.loc['2017-01-01':'2018-1-1']
    #Now grouping by day
    fraud_2017 = fraud_2017.groupby(['date']).sum()
    #Making a population df for stats test
    fraud_df= fraud_df.groupby(['date']).sum()
    #Create y out of target variable
    y = fraud_2017.count_of_crime
    z = fraud_df.count_of_crime
    # Taking the mean for the t-test
    overall_population = z.mean()
    #Setting alpha and running the test
    alpha = 0.05
    t, p = stats.ttest_1samp(y, overall_population)
    
    return print(f't-statistic:{round(t,3)}, P-Value:{round(p/2,3)}, alpha={alpha}')

def pre_post_t_test(fraud_df):
    '''get t-test for pre and post covid fraud crimes'''
    #Seperate samples into pre-covid and post-covid lockdown
    post_covid_df = fraud_df['2021-03-16':]
    pre_covid_df = fraud_df['2018-03-15':'2020-03-16']
    #Grouping by day
    post_covid_df = post_covid_df.groupby(['date']).sum()
    pre_covid_df = pre_covid_df.groupby(['date']).sum()
    #Run t-test on these groups, variances are not equal
    t, p = stats.ttest_ind(pre_covid_df.count_of_crime, post_covid_df.count_of_crime, equal_var=False)
    #Set Alpha
    alpha = 0.05
    
    null_hypothesis = "Fraud crime rates pre-pandemic are less than or equal to fraud crime rates post pandemic."
    alternative_hypothesis = "Fraud crime rates pre-pandemic are greater than fraud crime rates post pandemic."
    
    if (p/2 < alpha) & (t > 0):
        print("Reject the null hypothesis that", null_hypothesis)
        print("Sufficient evidence to move forward understanding that", alternative_hypothesis)
    else:
        print("Fail to reject the null")

    print(f't = {t:.4f}')
    print(f'p = {p:.4f}') 