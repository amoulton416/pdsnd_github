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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('Please enter a valid city.')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month_filter = input('\nDo you want to filter the data by a specific month? Yes or No\n').lower()
        if month_filter == 'no':
            month = 'all'
            break
        elif month_filter == 'yes':
            while True:
                month = input('\nWhich month? January, February, March, April, May or June\n').lower()
                if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                    print('Please enter a valid month.')
                else:
                    break
            break
        else:
            print('Not a valid input.  Please enter Yes or No')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_filter = input('\nDo you want to filter the data by a day of the week? Yes or No\n').lower()
        if day_filter == 'no':
            day = 'all'
            break
        elif day_filter == 'yes':
            while True:
                day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n').lower()
                if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    print('Please enter a valid day.')
                else:
                    break
            break
        else:
            print('Not a valid input.  Please enter Yes or No')

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

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Popular Month For Traveling:', popular_month)

    # display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('Most Popular Day For Traveling:', popular_day)

    # display the most common start hour
    popular_hour = df['start_hour'].mode()[0]
    print('Most Popular Hour to Start Traveling:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Station To Start From:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular Station to End At:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Popular Trip:', popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = int(df['Trip Duration'].sum())
    (tt_hours, tt_remainder) = divmod(total_time, 3600)
    (tt_minutes, tt_seconds) = divmod(tt_remainder, 60)
    print('Total Travel Time: {} Hours {} Minutes {} Seconds'.format(tt_hours, tt_minutes, tt_seconds))

    # display mean travel time
    mean_time = int(df['Trip Duration'].mean())
    (mt_hours, mt_remainder) = divmod(mean_time, 3600)
    (mt_minutes, mt_seconds) = divmod(mt_remainder, 60)
    print('Average Travel Time: {} Hours {} Minutes {} Seconds'.format(mt_hours, mt_minutes, mt_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type:')
    print(user_types.to_string())

    # display counts of gender
    print('\nGender:')
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print(gender_count.to_string())
    else:
        print('No Gender Data Provided For Washington.')

    # display earliest, most recent, and most common year of birth
    print('\nYear of Birth:')
    if city != 'washington':
        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        popular_year = int(df['Birth Year'].mode()[0])
        print('Earliest:', min_year)
        print('Most Recent:', max_year)
        print('Most Common Year:', popular_year)
    else:
        print('No Year of Birth Data Provided For Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Asks users if the want to see raw data and displays 5 rows at a time."""

    # while yes print next 5 lines of raw data and get user input if they want to see 5 more lines
    while True:
        view_raw = input('\nDo you want to see the first 5 lines of raw data? Yes or No\n').lower()
        i = 0
        if view_raw == 'yes':
            while view_raw == 'yes':
                print(df.iloc[i: i + 5])
                i += 5
                view_raw = input('\nDo you want to view 5 more lines of raw data? Yes or No\n').lower()
            break
        elif view_raw == 'no':
            break
        else:
            print('Not a valid input.  Please enter Yes or No')

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
