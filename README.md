# Boston Crime Data Project
## Project Description

This project was created to examine crime data from the City of Boston. Specifically, this project focuses on examining crime data collected by the City of Boston and examining trends in fraud crime occurences at several periods. The onset of the COVID pandemic and it's impact is seen through the visualization of this data, which leads to further questions about crime data forecasting before and after the pandemic, both within Fraud crimes and crime rates in general

## Goals
### Create deliverables:

* READ ME
* Final Report
* Functional wrangle.py, explore.py, and model.py files
* Acquire data from Analyze Boston Website
* Prepare and split the data
* Explore the data and define hypotheses, running appropriate statistical tests to accept or reject each null hypothesis
* Fit and train three (3) time-series models to predict the amount of fraud crimes on validation data
* Evaluate the models by comparing their performance validation data utilizing RMSE score
* Select the best model and evaluate it on test data
* Develop and document findings, takeaways, recommendations and next steps

# Initial Thoughts

* Boston Fraud Crime will increase post-pandemic

# The Plan

* Aquire and clean the data

* Explore data in search of time series patterns for fraud crimes
    * Answer the following initial questions
        * What was the average fraud crime rate in the two years immediately prior to the pandemic?
        * Are certain months more likely to demonstrate greater reported fraud crimes?
        * Do Fraud Crimes follow a seasonal pattern?
        * Is the downtrend seen in 2017 significant?
        
* Develop a Model to predict fraud crimes
    * Evaluate models on train and validate data
    * Select the best model to use on test data
    
* Draw Conclusions

# Data Dictionary

| Feature | Definition |
|:--------|:-----------|
|fips| Federal Information Processing Standard code -  see https://en.wikipedia.org/wiki/FIPS_county_code for more detail|
|latitude| Latitude of the middle of the parcel multiplied by 10e6|
|longitude| Longitude of the middle of the parcel multiplied by 10e6|
|LA| fips for the LA county|
|Orange| fips for the Orange county|
|Ventura| fips for the Ventura county|
|yearbuilt| The Year the principal residence was built|
|age| The year sold, 2017, minus the yearbuilt|
|age_bin| The age of the residence divided into several bins|
|taxamount| The total property tax assessed for that assessment year|
|taxrate| The taxamount divided by tax value multiplied by 100|
|taxvalue| The total tax assessed value of the parcel|
|lot_sqft| Area of the lot in square feet|
|acres| lot_sqft divided by 43560|
|acres_bin| The acres of residence divided into several bins|
|sqft_bin| The sqft of residence divided into several bins|
|structure_dollar_per_sqft| The tax value divided by sqft|
|structure_dollar_sqft_bin| A division of the structure dollar divided into several bins|
|land_dollar_per_sqft| land_value divided by lot_sqft|
|lot_dollar_sqft_bin| land_dollar_per_sqft divided into several bins|
|bath_count| number of bathrooms in residence|
|bed_count| number of bedrooms in residence|
|bath_bed_ratio| bath_count divided by bed_count|
|cola| Whether or not a residence is in the city of LA|

# Steps to Reproduce
1) Clone this repository
2) Download Boston Crime Data from analyze Boston (https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system)
3) Put the data in  the file containing the cloned repo
4) Utilize code from project notebook to aggregate data into one .CSV, which can be used locally
4) Run notebook

# Takeaways and Conclusions
* Our model for predicting fraud crimes using a simple average was fairly effective
* Fraud crimes spiked during the pandemic
* This visualization shows that since lockdown restrictions were eased in Boston in the spring of 2021, Fraud crimes appears to be **decreasing** 
* When aggregating fraud crimes by day, there was low seasonality in this data
* Pre-pandemic, a simple average model was the best model for predicting fraud crime
* A simple average model performed extremely poorly on test data, which was the first year of COVID. In Boston, COVID restrictions meant strict lockdowns for the early stages of the pandemic
* Though lockdown restrictions have been completely lifted, the fraud crime rate has significantly decreased in Boston

# Recommendations

* Resampling fraud crimes by week or month to get a clearer picture of seasonality
* Creating a new model for post-pandemic data, excluding lockdown periods due to severe outliers

# Next Steps

* Literature Review to examine trends observed in this project compared to other examinations of crime data during the pandemic
* Examining Boston Crime Data for other crimes besides fraud, to see if other types of crime are more seasonal
* Examining Boston Crime Data for other crimes besides fraud, to see if COVID lockdowns created similar patterns of anomalies (spikes/dips) in and around lockdown periods
* Using location data to visualize crime types around the city (for a more Boston-centric approach)