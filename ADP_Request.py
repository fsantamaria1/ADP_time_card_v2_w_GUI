import requests
import json
from datetime import date
from datetime import timedelta
from FileOpener import TextFileReader
from Dates import Dates

# PEM file path
# cert_file_path = r"C:\ADP API\Certificates\berryit_auth.pem"
cert_file_path = r"Y:\05 Users\Cossell\ADP API\Certificates\berryit_auth.pem"
# KEY file path
# key_file_path = r"C:\ADP API\Certificates\berryit_auth.key"
key_file_path = r"Y:\05 Users\Cossell\ADP API\Certificates\berryit_auth.key"
# Both files combined
cert = (cert_file_path, key_file_path)
# Authorization token file path
auth_token_path = r"Y:\05 Users\Cossell\ADP API\Certificates\auth_token_encrypted.txt"
# Associate AOID file path
aoid_path = r"Y:\05 Users\Cossell\ADP API\Certificates\AOID.txt"
# Read and assign auth token to variable
auth_token = TextFileReader(auth_token_path).read_first_line()
# Get Associate OID
associate_id = TextFileReader(aoid_path).read_first_line()


# Class used to get bearer token and certain APIs
class APIRequest:
    # def __init__(self, cert, authorization_token, associate_id):
    def __init__(self):
        self.files = {}
        self.payload = {}
        # self.today = date.today()
        self.today = Dates().get_date_today()
        self.monday = Dates().get_date_monday()
        self.time_cards_list = []
        self.API_url_list = []
        self.certificate = cert
        self.associate_id = associate_id
        self.auth_token = auth_token

    # This method gets the token and returns it when called
    def get_token(self):
        """Returns the ADP API bearer token used to make API calls."""
        # URL used to get the bearer token
        self.url = "https://accounts.adp.com/auth/oauth/v2/token?grant_type=client_credentials"
        # self.auth_token = authorization_token
        self.headers = {
            'Authorization': 'Basic {0}'.format(self.auth_token)
        }
        self.response = requests.request("POST", url=self.url, headers=self.headers, data=self.payload,
                                         files=self.files, cert=self.certificate)
        # Loads the response into text format
        self.response_text = json.loads(self.response.text)
        # Retrieves the token from the response and assigns it to a variable
        self.token = self.response_text['access_token']
        # Adds the word 'Bearer' to the token since ADP requires it to be like that
        self.bearer_token = "Bearer " + self.token
        # print(self.bearer_token)
        return self.bearer_token
    # Generates headers that need to be used when making an API call
    def get_time_card_api_headers(self, bearer_token):
        """Returns the necessary headers used to make the ADP Time Card API calls."""
        self.bearer_token = bearer_token
        self.headers = {
            'Authorization': self.bearer_token,
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'api.adp.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Apache-HttpClient/4.5.2(Java/1.8.0_112)',
            'Accept': 'application/json',
            'Cookie': 'BIGipServerp_dc1_mobile_sor_integratedezlm=3938124043.15395.0000; BIGipServerp_dc2_mobile_apache_sor=3013608203.5377.0000; BIGipServerp_mkplproxy-dc1=1633878283.20480.0000; BIGipServerp_mkplproxy-dc2=670892811.20480.0000; BIGipServerp_dc1_mobile_apache_sor=153042955.5377.0000; Cookie_1=value'
        }
        return self.headers

    def generate_url(self, pay_period_start_date, top: int, skip: int):
        """Returns the necessary URL used to make the ADP Time Card API calls. Needs to be provided the following
        filtering criteria: top, skip, and the pay period start date """
        # Number of records
        self.top = top
        # Number of records skipped
        self.skip = skip
        # Pay period start date
        self.reference_date = pay_period_start_date
        self.url = "https://api.adp.com/time/v2/workers/{0}/team-time-cards?$expand=dayEntries&$top={1}&$skip={2}&$filter=timeCards/timePeriod/startDate eq '{3}'".format(
            self.associate_id, self.top, self.skip, self.reference_date)
        return self.url




