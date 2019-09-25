import time
import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nA. Enter the city you like to analyze- chicago, new york city, washington or all?\n").lower()

    while city not in ('chicago', 'new york city', 'washington', 'all'):
        print("Sorry, Invalid Entry. Try Again!\n")
        city = input("RE-ENTER one of the following: chicago, new york city, washington OR all\n").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nB. Enter the month you like to view- january, february, march, april, may, june OR all\n").lower()

    while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        print("Sorry, Invalid Entry. Try Again!\n")
        month = input("B. RE-ENTER one of the following: january, february, march, april, may, june OR all\n").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nC. Which week day would you like to view? Type a day OR type 'all' to view data for all days\n").lower()

    while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        print("Sorry, Invalid Entry. Try Again!\n")
        day = input("C. RE-ENTER one of the following- monday, tuesday, wednesday, thursday, friday, saturday, sunday OR all\n").lower()

    print('-'*60)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'all':
        #combine all files in the list
        df = pd.concat(map(pd.read_csv, ['chicago.csv', 'new_york_city.csv','washington.csv']),sort=True)

    else:
        df = pd.read_csv(CITY_DATA[city])

    #Change the 'Start Time' column into datetime data structure
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract 'month' from 'Start Time' column and create a new column
    df['month'] = df['Start Time'].dt.month

    #Extract 'day of week' from Start Time and cread a new column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Given user selects a specific month, filter the dataset with that month
    if month != 'all' :
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        #Convert the month-name into month-number format by using index of months
        month_num = months.index(month) + 1

        month_chosen =  df['month']== month_num
        df = df[month_chosen]

    #Given user selects a specific day, filter the dataset with that day
    if day != 'all' :
        day_chosen = df['day_of_week']== day.title()
        df = df[day_chosen]


    return df

def print_dataset(df, month, day):
    filtered_dataset = input('\n1. Based on your choice of \'Month = {}\' & \'Day = {}\', Would you like to view the Filtered Dataset? Enter yes or no.\n'.format(month.upper(), day.upper())).lower()

    while True:
        print('\nBELOW IS A SAMPLE OF FILTERED DATA BASED ON MONTH & DAY CHOSEN\n')
        #print(df.head())
        print(df.sample(n=5))
        filtered_dataset = input('\nWould you like to view another set of Filtered Dataset? Enter yes or no.\n').lower()

        if filtered_dataset != 'yes':
            break

    print('-'*60)



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n2. TIME STATISTIC ANALYSIS: Maximum Frequency of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    #Extract 'hour' from the 'Start Time' column
    df['hour'] = df['Start Time'].dt.hour

    #Find the most frequent appearing hour
    popular_hour = df['hour'].mode()[0]

    #from tabulate import tabulate
    print(tabulate([['Month-wise', popular_month], ['Day-wise', popular_day], ['Hour-wise', popular_hour]], headers=['MOST FREQUENT USUAGE OF BIKE', 'ANALYSIS'], tablefmt='orgtbl'))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n3. STATIONS STATISTIC ANALYSIS: Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1).reset_index(name='count')

    print(tabulate([['Start Station', popular_start_station], ['End Station', popular_end_station], ['Trip: Start-End', popular_trip]], headers=['MOST POPULAR STATIONS/TRIP', 'ANALYSIS'], tablefmt='orgtbl'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n4. TIME ANALYSIS: Calculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time_sum = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    total_travel_time_mean = df['Trip Duration'].mean()

    print(tabulate([['Sum', total_travel_time_sum, total_travel_time_sum/60.0, total_travel_time_sum/3600.0], ['Mean', total_travel_time_mean, total_travel_time_mean/60.0, total_travel_time_mean/3600.0]], headers=['TOTAL TRAVEL TIME', 'SECONDS', 'MINUTES', 'HOURS'], tablefmt='orgtbl'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    if city == 'washington':
        print('\n5. USERS STATISTICS:\nSorry, User details are not defined in this dataset (washington.csv)\n')

    else:
        print('\n5. USERS STATISTICS: Calculating User Stats...\n')
        start_time = time.time()

        # TO DO: Display counts of user types
        user_type = df['User Type'].value_counts()
        print("\n5a. COUNT OF USER TYPES:\n{}".format(user_type))

        # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("\n5b. COUNT OF USEAGE BASED ON GENDER:\n{}".format(gender_count))

        # Get current year (to find the age of oldest and youngest user who used BikeShare services)
        currentYear = datetime.now().year

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        age_oldest_person = currentYear - earliest_year

        recent_year = df['Birth Year'].max()
        age_youngest_person = currentYear - recent_year

        most_common_year = df['Birth Year'].mode()[0]
        age_most_common_year = currentYear - most_common_year

        print("\n5c. USERS AGE ANALYSIS:\n")
        print(tabulate([['Oldest Person', earliest_year, age_oldest_person], ['Youngest Person', recent_year, age_youngest_person], ['Most Common Users', most_common_year, age_most_common_year]], headers=['USER', 'YEAR BORN', 'AGE'], tablefmt='orgtbl'))

        print("\nThis took %s seconds." % (time.time() - start_time))

        print('-'*60)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print_dataset(df, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
