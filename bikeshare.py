import time
import pandas as pd
import numpy as np

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

    cities = {'chicago', 'new york city', 'washington'}
    city = input("\nHello! Let\'s explore some US bikeshare data!\n\nWhat city do you want to learn about (Chicago, New York City or Washington)? ").lower()
    while city not in cities:
        city = input("\nIt looks like your answer is not in our list. Please type Chicago, New York City or Washington: ").lower()

    months = {'all', 'january', 'february', 'march', 'april' 'may', 'june'}
    month = input("\nWhat month do you want to learn about? ").lower()
    while month not in months:
        month = input("\nIt looks like your answer is not in our list. Please type January, February, March, April, May, June or All: ").lower()

    days = {'all', 'monday', 'tuesday', 'wednesday', 'thursday' 'friday', 'saturday', 'sunday'}
    day = input("\nWhat day of the week do you want to learn about? ").lower()
    while day not in days:
        day = input("\nIt looks like your answer is not in our list. Please type Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All: ").lower()

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

    city_filter = pd.read_csv(CITY_DATA[city])

    df = city_filter

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.strftime('%B')

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    df['hour'] = df['Start Time'].dt.hour

    df['trip'] = df[['Start Station', 'End Station']].agg(' - '.join, axis=1)

    if month != 'all':

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most Popular Month: ', df['month'].mode()[0])

    print('\nMost Popular Day of the Week: ', df['day_of_week'].mode()[0])

    print('\nMost Popular Hour: ', df['hour'].mode()[0], ' h')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Popular Start Station: ', df['Start Station'].mode()[0])

    print('\nMost Popular End Station: ', df['End Station'].mode()[0])

    print('\nMost Popular Trip: ', df['trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Travel Time: ~', int(df['Trip Duration'].sum()/86400), ' days and ', int((df['Trip Duration'].sum()%86400)/3600), ' hours.')

    print('\nMean Travel Time: ~', int(df['Trip Duration'].mean()/60), ' minutes and ', int((df['Trip Duration'].mean()%60)), ' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Breakdown of User Type:\n\n", df['User Type'].value_counts())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def gender_birth(df):
    """Displays statistics on Gender and Birth Year of bikeshare users."""

    print('\nCalculating Gender and Birth Year Stats...\n')
    start_time = time.time()

    print("Breakdown of Gender:\n\n", df['Gender'].value_counts())

    print("\n Earliest year of birth:  ", int(df['Birth Year'].min()))
    print("\n Most recent year of birth:  ", int(df['Birth Year'].max()))
    print("\n Most common year of birth:  ", int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        if city != 'washington':
            gender_birth(df)
        else:
            print('\nNo info on Gender or Birth Year available for Washington')
            print('-'*40)
        start_count = 0
        end_count = 5
        while True:
            raw_data = input('\nDo you want to see the first five rows of the raw data?\n\nEnter yes or no.\n\n')
            start_count += 5
            end_count += 5
            if raw_data == 'yes':
                print(df.iloc[start_count:end_count])
            else:
                break
            if start_count > 4:
                while True:
                    raw_data = input('\nDo you want to see five additional rows of the raw data?\n\nEnter yes or no.\n\n')
                    start_count += 5
                    end_count += 5
                    if raw_data == 'yes':
                        print(df.iloc[start_count:end_count])
                    else:
                        break
                break

        restart = input('\nWould you like to start over?\n\nEnter yes or no.\n\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
