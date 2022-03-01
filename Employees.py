import requests
import json

import ADP_Request
from datetime import date
from Dates import Dates

# from ADP_Request import *

class Employees(ADP_Request.APIRequest):
    def __init__(self):
        super().__init__()
        # self.api_object = ADP_Request.APIRequest()
        #
        # self.bearer_token = self.api_object.get_token()
        # # self.time_card_headers = self.api_object.get_time_card_api_headers(self.bearer_token)
        # self.time_card_headers = self.api_object.get_time_card_api_headers(self.bearer_token)
        self.date_monday = Dates().get_date_monday()
        self.bearer_token = self.get_token()
        self.time_card_headers = self.get_time_card_api_headers(self.bearer_token)

    # Makes an API call and returns the response in text format
    def __get_time_card_api_response__(self, pay_period_start_date, top=50, skip=0):
        self.date = pay_period_start_date
        self.top = top
        self.skip = skip
        self.continue_request = True
        self.url = self.generate_url(self.date, self.top, self.skip)
        self.response = requests.request("GET", url=self.url, headers=self.time_card_headers, data=self.payload,
                                         files=self.files, cert=self.certificate)
        # Loads the response into text format
        self.response_text = json.loads(self.response.text)
        return self.response_text

    # This method can be used to generate a list of time cards from a date range
    # Currently not being used
    def __get_time_card__(self, pay_period_start_date_list: list):
        self.dates = pay_period_start_date_list
        self.all_time_cards = []
        for self.date in self.dates:
            self.top = 25
            self.skip = 0
            self.time_cards = []
            self.continue_request = True
            while self.continue_request == True:
                self.api_response = self.__get_time_card_api_response__(self.date, self.top, self.skip)
                # print(self.url)
                self.top += 25
                self.skip += 25
                self.time_cards.append(self.response_text)  # Might try extending the list instead
                # self.time_cards2.extend(self.response_text['teamTimeCards'])
                # Retrieves the number of employees from the response and assigns it to a variable
                if self.api_response['meta']['completeIndicator'] == True:
                    self.continue_request = False
            self.all_time_cards.append(self.time_cards)
        return self.all_time_cards

    def get_current_number_of_employees(self):
        """Returns the current number of active employees in ADP"""
        # self.reference_date = str(self.today)
        self.top = 25
        self.skip = 0
        self.api_response = self.__get_time_card_api_response__(self.date_monday, self.top, self.skip)
        self.number_of_timecards = self.api_response['meta']['totalNumber']
        # Meta data indicates the time card response is not completed yet
        # self.response_text['meta']['completeIndicator'] == False
        # Returns the number of employees when the method is called
        return self.number_of_timecards

    # Generates time cards within a date range
    def get_time_cards_from_date_range(self, start_date, end_date):
        """Returns the weekly time card records from given date ranges"""
        self.first_date = start_date
        self.last_date = end_date
        self.list_of_mondays = Dates(self.first_date, self.last_date).get_list_of_mondays()
        self.api_response = self.__get_time_card__(self.list_of_mondays)
        return self.api_response

    def get_time_cards_from_single_date(self, single_date_within_pay_period):
        """Returns the time card records for the pay week based on the given date"""
        self.given_date = single_date_within_pay_period
        # print(self.given_date)
        self.list_of_mondays = Dates(self.given_date, self.given_date).get_list_of_mondays()
        # print(self.list_of_mondays)
        self.api_response = self.__get_time_card__(self.list_of_mondays)
        return self.api_response[0]

    def get_time_cards_current_week(self):
        """Returns the time card records for the current week (next pay week)"""
        # A date list is required by the method providing
        self.monday = []
        self.monday.append(Dates().get_date_monday())
        # self.monday_date.append(self.date_monday)
        self.api_response = self.__get_time_card__(self.monday)
        # print(len(self.api_response))
        return self.api_response[0]
