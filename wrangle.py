import pandas as pd
import numpy as np
from datetime import datetime

def aggregate_csv():
    '''This function concatenates all yearly crime reports and returns one 
    dataframe with all project data'''
    #Get data from CSV files
    df2015 = pd.read_csv("crime-incident-reports-2015.csv")
    df2016 = pd.read_csv("crime-incident-reports-2016.csv")
    df2017 = pd.read_csv("crime-incident-reports-2017.csv")
    df2018 = pd.read_csv("crime-incident-reports-2018.csv")
    df2019 = pd.read_csv("crime-incident-reports-2019.csv")
    df2020 = pd.read_csv("crime-incident-reports-2020.csv")
    df2021 = pd.read_csv("crime-incident-reports-2021.csv")
    df2022 = pd.read_csv("crime-incident-reports-2022.csv")
    # # Forming a table from DFs
    table = []
    table.append(df2015)
    table.append(df2016)
    table.append(df2017)
    table.append(df2018)
    table.append(df2019)
    table.append(df2020)
    table.append(df2021)
    table.append(df2022)
    # # #Combine all tables, ignore index
    df = pd.concat(table, ignore_index=True)
    # #Save data as combined csv
    df.to_csv('boston_crime.csv')
    #Get CSV from file
    df = pd.read_csv('boston_crime.csv', index_col=0)
    
    return df


def combine_data():
    ''' Combine retrieved CSV files from Boston Crime Incident Reports Website
    (https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system)
    into one CSV, and returns a data frame. This function should be used once all files are downloaded
    from the Boston Crime Incident Reports are downloaded and appropriately named
    '''
    #get my data from csv files
    df2015 = pd.read_csv("crime-incident-reports-2015.csv")
    df2016 = pd.read_csv("crime-incident-reports-2016.csv")
    df2017 = pd.read_csv("crime-incident-reports-2017.csv")
    df2018 = pd.read_csv("crime-incident-reports-2018.csv")
    df2019 = pd.read_csv("crime-incident-reports-2019.csv")
    df2020 = pd.read_csv("crime-incident-reports-2020.csv")
    df2021 = pd.read_csv("crime-incident-reports-2021.csv")
    df2022 = pd.read_csv("crime-incident-reports-2022.csv")
    #Forming a table from DFs
    table = []
    table.append(df2015)
    table.append(df2016)
    table.append(df2017)
    table.append(df2018)
    table.append(df2019)
    table.append(df2020)
    table.append(df2021)
    table.append(df2022)
    #Combine all tables, ignore index
    df = pd.concat(table, ignore_index=True)
    #Save data as combined csv
    df.to_csv('boston_crime.csv')
    
    return df

def get_clean_data():
    '''This function takes in the Boston Crime dataframe from a csv file and addresses the messiness
    by renaming columns, filling whitespace, imputing NaN values, standardizing field values, and recasting
    data types'''
    #Get CSV from file
    df = pd.read_csv('boston_crime.csv', index_col=0)
    #Rename columns to remove capital letters
    df.columns = df.columns.str.lower()
    #Replace a whitespace sequence or empty with a NaN value and reassign this manipulation to df
    df = df.replace(r'^\s*$', np.nan, regex=True)
    #Replace NaN values in offense code group with unknown
    df['offense_code_group'].fillna("unknown", inplace=True)
    #Changing Y in shooting to 1(Yes)
    df.loc[df["shooting"] == "Y", "shooting"] = 1
    #Replace Nan Values in shooting with zeroes
    df['shooting'].fillna(0, inplace=True)
    #Recasting shooting column as an integer
    df['shooting'] = df['shooting'].astype(int)
    #Replace NaN values in ucr part with unknown
    df['ucr_part'].fillna("unknown", inplace=True)
    #Going to fill NaN with zeroes for reporting area, which represents where a crime is reported from
    df['reporting_area'].fillna(0, inplace=True)
    #Make everything lowercase in offense code group and description
    df['offense_code_group'] = df['offense_code_group'].str.lower()
    df['offense_description'] = df['offense_description'].str.lower()
    
    return df

def create_fraud_df(df):
    '''This function takes in the crime dataframe, and creates a new dataframe based on the categorization
    of crime description. It also renames columns for usability, converts the date column to a DateTime type,
    takes the date and transforms the index into a DateTime index, and adds a column called "count of crime",
    which assigns a value of 1 to every row'''
    #Uses str.contains to get fraud from description
    fraud_df = df[df['offense_description'].str.contains('fraud')]
    #Rename date column to make it easier
    fraud_df.rename(columns = {'occurred_on_date':'date'}, inplace = True)
    #Occured on date is an object, lets make it date time
    fraud_df['date'] = pd.to_datetime(fraud_df['date'])
    #adding a column to the dataframe to get a count of crime
    fraud_df['count_of_crime'] = 1
    #Remove hour from date time, since we aren't looking for that now
    fraud_df['date'] = fraud_df['date'].dt.normalize()
    # #Reset index to date time
    fraud_df = fraud_df.set_index('date').sort_index()
    fraud_df
    
    return fraud_df