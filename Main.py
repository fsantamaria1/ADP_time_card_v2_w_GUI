from datetime import date, timedelta
from Response_Filtering import ResponseFilter
from decimal import Decimal

from ADP_Request import APIRequest
from FileOpener import TextFileReader
from Dates import Dates
from Employees import Employees
from Response_Filtering import ResponseFilter
from Timecard import Timecard, Timecardv2, TimeEntry


# Gets single time card and adds the multiple responses to a list
def single_week_time_cards(date_within_pay_period: date):
    given_date = date_within_pay_period
    # employees_object = Employees()
    time_cards = Employees().get_time_cards_from_single_date(given_date)
    # for time_card in time_cards:
    #     for person in time_card['teamTimeCards']:
    #         print(person['personLegalName']['formattedName'])
    #         print(person['timeCards'][0]['timePeriod']['startDate'])
    return time_cards


# Generates a list of time cards
def multiple_week_time_cards(date_within_first_pay_period: date, date_within_last_pay_period: date):
    employees_object = Employees()
    time_cards_list = employees_object.get_time_cards_from_date_range(date_within_first_pay_period,
                                                                      date_within_last_pay_period)
    # for time_cards in time_cards_list:
    #     for time_card in time_cards:
    #         for person in time_card['teamTimeCards']:
    #             print(person['personLegalName']['formattedName'])
    #             print(person)
    return time_cards_list


def file_writer(file_name: str, time_card_object):
    try:
        file = open(fr"{file_name}", "w")
        file.write(Timecard.csvTitles())
        for card in time_card_object:
            file.write(card.CsvStr())
        file.close()
    except:
        print("Error writing file Single Day")


def file_writer_multiple_days(file_name: str, time_card_list_object):
    try:
        file = open(fr"{file_name}", "w")
        file.write(Timecard.csvTitles())
        for time_card_list in time_card_list_object:
            for card in time_card_list:
                file.write(card.CsvStr())
            # file.write(time_card_list.CsvStr())
        file.close()
    except:
        print("Error writing file Multiple Days")
