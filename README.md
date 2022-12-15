# Data Dictionary
| Feature | Definition |
|:--------|:-----------|
|fips| Federal Information Processing Standard code -  see https://en.wikipedia.org/wiki/FIPS_county_code for more detail|
|latitude| Latitude of the middle of the parcel multiplied by 10e6|
|longitude| Longitude of the middle of the parcel multiplied by 10e6|
|LA| fips code for LA county|
|Orange| fips code for Orange county|
|Ventura| fips code for Ventura county|
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