import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june']

DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city not in CITY_DATA.keys():
            print('\nSorry, please input a valid city!')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you like to filter the data by which month - January, February, March, April, May, or June? Type "all" for no time filter.\n').lower()
        if month in MONTH_LIST or month == 'all':
            break
        else:
            print('\nSorry, please input a valid month!')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWould you like to filter the data by which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type "all" for no time filter.\n').lower()
        if day in DAY_LIST or day == 'all':
            break
        else:
            print('\nSorry, please input a valid day of week!')
            continue

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular day of week:', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df.groupby(['Start Station'])['Start Station'].count().nlargest(1)
    print('Most commonly used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df.groupby(['End Station'])['End Station'].count().nlargest(1)
    print('Most commonly used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station'])['Start Station'].count().nlargest(1)
    print('Most commonly used Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', round(total_travel_time,0), 'seconds')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Avearge travel time:', round(average_travel_time,0), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('Counts of genders:\n', genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        yob_min = int(df['Birth Year'].min())
        print('Earliest year of birth:\n', yob_min)
        yob_max = int(df['Birth Year'].max())
        print('Most recent year of birth:\n', yob_max)
        yob_pop = int(df['Birth Year'].mode()[0])
        print('Most common year of birth:\n', yob_pop)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_trip(df):
    """Displays detailed trips without any aggregation."""
    
    individual_trip_count = 0
    while True:
        to_show_more = input('Would you like to view individual trip data? Type "yes" or "no" \n').lower()
        if to_show_more == 'yes':
            df_selected = df.iloc[individual_trip_count: individual_trip_count + 5]
            for key, value in df_selected.items():
                print(key, ': ', value, '\n')
            individual_trip_count += 5
            continue
        elif to_show_more == 'no':
            break
        else:
            print('\nSorry, please input yes or no!')
            continues   


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_trip(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
