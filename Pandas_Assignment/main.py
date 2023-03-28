# Pandas Library - Python
# Author: Merna Islam Mohamed
# Last Modified: 28/3/2023

# Task 1 : import the CSV file data/brasil-real-estate-1.csv into dataframe df
import pandas as pd
df = pd.read_csv('brasil-real-estate-1.csv', encoding="latin")
print(df)

# Task 2 :Drop all rows with NAN values from df
df = df.dropna()
print(df)

# Task 3: use "lat-lon" columns to create two separate columns in df "lat", "lon". Make sure that the datatype will be float
print(df['lat-lon'].head())
df[['lat', 'lon']] = df['lat-lon'].str.split(",", expand=True)  # use ',' as a delimiter
print(df['lat'].head())
print(df['lon'].head())

# Task 4: Transform "price_USD" so that all values be floating points instead of strings
df['price_usd'] = df['price_usd'].str.replace('[,$]', '', regex=True).astype(float)  # Slicing to remove the first char '$'
print(df['price_usd'].head())

# Task 5: drop "lat-lon" columns
df.drop(columns=['lat-lon'], inplace=True)
print(df)

# Task 6: import the CSV file data/brasil-real-estate-2.csv into dataframe df2
df2 = pd.read_csv('brasil-real-estate-2.csv', encoding="latin")
print(df2)

# Task 7: use "price_brl" to create new columns named "price_usd" by dividing the value by 3.19
df2['price_usd'] = (df2['price_brl'] / 3.19).round(2)
print(df2.head())

# Task 8: drop "price_brl" from columns, as well as any rows that have Nan values
df2.drop(columns=['price_brl'], inplace=True)
df2.dropna(inplace=True)

# Task 9: concatenate df and df2 into new dataframe named df_new
df_new = pd.concat([df, df2])
print(df_new)

# Task 10: use describe method to create dataframe summary_stats for "area_m2" and "price_usd" columns
summary_stats = df_new[['area_m2', 'price_usd']].describe()
print(summary_stats)

# Task 11: use groupby method to create a series named mean_price_by_region that shows the mean home price in brazil, sorted from smallest to highest
mean_price_by_region = df_new.groupby('region')['price_usd'].mean().sort_values()
print(mean_price_by_region)

# Task 12: create new dataframe named df_south that contains all homes from df in South region
df_south = df_new[df_new['region'] == 'South']
print(df_south)

# Task 13: use value_counts method to create a series home_by_state that contains the number of properties in df_south
home_by_state = df_south.groupby('state')['property_type'].value_counts()
print(home_by_state)
#____________________________________
# PART TWO
# Task 14: Write a wrangle function that takes the name of csv as argument and perform the following :
#
# 1- read mexico-real-estate-1.csv into df
#
# 2- get only the apartment that locates in mexico city "Distrito Federal" that costs less than 100,000
#
# 3- create separate "lat" and "lon" columns as done before
#
# 4- drop columns that are more than 50 % Nan values
#
# 5- drop all columns with categorical values
#
# 6- return df at last
def wrangle(filename):

    # Part 1
    df = pd.read_csv(filename, encoding="latin")

    # Reading column names in a list to get the name of the last column (price)
    col_name_lst = list(df.columns)
    price_col_name = col_name_lst[-1]

    # Preparing for step 2 "price constraint"
    if df[price_col_name].dtype == object:
        df[price_col_name] = df[price_col_name].str.replace('[,$]', '', regex=True).astype(float)

    # Part 2
    if 'state' in df.columns:
        df = df.loc[(df['state'] == 'Distrito Federal') ]
    else:
        df = df.loc[df['place_with_parent_names'].str.contains('Distrito Federal')]

    df = df.loc[(df[price_col_name] < 100000) & (df['property_type'] == 'apartment')]

    # Part 3
    if 'lat-lon' in df.columns:
        df[['lat', 'lon']] = df['lat-lon'].str.split(',', expand=True).astype(float)
        df.drop('lat-lon', axis=1, inplace=True)

    # Part 4
    min_count = int(0.5 * df.shape[0] + 1)
    df.dropna(axis=1, thresh=min_count, inplace=True)

    # Part 5
    df.drop(df.select_dtypes(include=['object', 'category']), axis=1, inplace=True)

    # Part 6
    return df

new_df = wrangle('mexico-real-estate-3.csv')
print(new_df)

# use glob method to create list of files. it should contain the filename of all mexico real state.
import glob as gb
filename_list = []
for i in gb.glob('mexico-real-estate-[0-9].csv'):
    filename_list.append(i)
print(filename_list)

# combine your wrangle function, a list comprehension and pd.concat to create new dataframe df from all files names from previous task
df_mexico_1 = wrangle('mexico-real-estate-1.csv')
df_mexico_2 = wrangle('mexico-real-estate-2.csv')
df_mexico_3 = wrangle('mexico-real-estate-3.csv')
df_all = pd.concat([df_mexico_1, df_mexico_2, df_mexico_3])
print(df_all)

# _______ END OF ASSIGNMENT _______


