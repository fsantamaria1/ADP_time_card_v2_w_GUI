from datetime import date, datetime, timedelta

"""This class is used to perform date operations"""


# Class used to find first day of the week, last day of week, and a list of first day's when given a date or dates
class Dates:

    def __init__(self, optional_first_date=date.today(), optional_second_date=date.today()):
        # If optional_first_date is not given then it is today's date
        self.given_date = optional_first_date
        self.second_given_date = optional_second_date
        # Call the __check__type class to create a date object from string or formats the date object
        self.given_date = self.__check_type__(self.given_date)
        self.second_given_date = self.__check_type__(self.second_given_date)

    # Converts string to date or formats date object
    def __check_type__(self, date_as_str):
        self.date_str = date_as_str
        # Convert string to date object
        if type(self.date_str) is str:
            self.date_str = datetime.strptime(self.date_str, '%Y-%m-%d')
            self.date_obj = self.date_str.date()
        # Formats date object
        else:  ## type(self.date_str) is datetime:
            self.date_str = datetime.strftime(self.date_str, '%Y-%m-%d')
            self.date_str = datetime.strptime(self.date_str, '%Y-%m-%d')
            self.date_obj = self.date_str.date()
        return self.date_obj

    #
    def __get_monday__(self, random_date):
        self.random_date = random_date
        self.monday = self.random_date - timedelta(days=self.random_date.weekday())
        # self.monday = self.monday.strftime('%Y-%m-%d')
        return self.monday

    #
    def __get_sunday__(self, random_date):
        self.random_date = random_date
        self.monday = self.__get_monday__(self.random_date)
        self.sunday = self.monday + timedelta(days=6)
        # self.sunday = self.monday.strftime('%Y-%m-%d')
        return self.sunday

    def get_date_monday(self):
        """This method returns monday's date based on the given date. If no date is given, then the given date is set
        to today's date."""
        self.monday = self.__get_monday__(self.given_date)
        return self.monday

    def get_date_previous_monday(self):
        """This method returns monday's date based on the given date. If no date is given, then the given date is set
        to today's date."""
        # Get monday's date
        self.monday = self.__get_monday__(self.given_date)
        # Subtract one day so it becomes previous sunday
        self.monday = self.monday - timedelta(days=1)
        # Find the previous monday's date
        self.previous_monday = self.__get_monday__(self.monday)
        return self.previous_monday

    def get_date_sunday(self):
        """This method returns sunday's date based on the given date. If no date is given, then the given date is set
        to today's date."""
        self.sunday = self.__get_sunday__(self.given_date)
        return self.sunday

    # def get_date_previous_sunday(self):
    #     """This method returns monday's date based on the given date. If no date is given, then the given date is set
    #     to today's date."""
    #     # Find previous sunday's date using previous monday's date
    #     self.previous_sunday = self.__get_sunday__(self.get_date_previous_monday())
    #     return self.previous_monday

    def get_list_of_mondays(self):
        """This method returns a list of monday's dates when two dates are given."""
        self.monday_list = []
        self.first_monday = self.__get_monday__(self.given_date)
        self.last_monday = self.__get_monday__(self.second_given_date)
        # Make sure the dates are in the correct order
        if self.first_monday > self.last_monday:
            self.temp = self.first_monday
            self.first_monday = self.last_monday
            self.last_monday = self.temp
        # Assign the first monday date to a variable which will be used the loop below
        self.current_monday = self.first_monday
        # Add the first monday date to the list
        self.monday_list.append(self.first_monday)
        # If the dates are not the same then this loop will add all the mondays in between to a list
        while self.current_monday != self.last_monday:
            self.current_monday = self.current_monday + timedelta(days=7)
            self.monday_list.append(self.current_monday)
        return self.monday_list

    def get_date_yesterday(self):
        """This method returns yesterday's date. If no date is given, then it subtracts a day from today's date"""
        self.yesterday = self.given_date - timedelta(days=1)
        return self.yesterday

    @staticmethod
    def get_date_yesterday_string():
        """This method returns yesterday's date. If no date is given, then it subtracts a day from today's date"""
        yesterday = date.today() - timedelta(days=1)
        yesterday_string = date.strftime(yesterday, '%Y-%m-%d')
        return yesterday_string

    def get_date_today(self):
        """This method returns today's date"""
        self.today = date.today()
        return self.today

    @staticmethod
    def get_date_today_string():
        """This method returns today's date"""
        today = date.today()
        today_string = date.strftime(today, '%Y-%m-%d')
        return today

    def format_date_str(self, date_to_be_formatted):
        self.date_to_formatted = date_to_be_formatted
        self.formatted_date = self.__check_type__(self.date_to_formatted)
        return str(self.formatted_date)

    def get_list_of_dates(self):
        self.first_date = self.given_date
        self.last_date = self.second_given_date
        self.list_of_dates = []
        if self.first_date > self.last_date:
            self.temp = self.first_date
            self.first_date = self.last_date
            self.last_date = self.temp
        self.date_to_add = self.first_date
        while self.last_date >= self.date_to_add:
            self.list_of_dates.append(self.date_to_add)
            self.date_to_add += timedelta(days=1)
        return self.list_of_dates
