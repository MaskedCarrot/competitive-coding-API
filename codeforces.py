from re import fullmatch
from constants import CODEFORCES_URL
import requests
import json
from constants import *


class CodeforcesUserData:

    def __init__(self, username=None):
        self.__username = username

    def get_personal_details(self):
        full_url = f'user.info?handles={self.__username}'
        url = CODEFORCES_URL+full_url

        result = {'status': STATE_PENDING}

        try:
            response = requests.get(url)
            json_object = response.json()

            data = json_object['result'][0]

            result['status'] = STATE_PASS

            result['name'] = data['firstName'] + ' ' + data['lastName']
            result['username'] = self.__username
            result['rank'] = data['rank']
            result['rating'] = data['rating']
            result['avatar'] = 'https:'+data['titlePhoto']
            result['city'] = data['city']
            result['country'] = data['country']
            result['organization'] = data['organization']
        except:
            result = {'status': STATE_ERROR_INVALID_USER,
                      'username': self.__username}
        finally:
            return result

    def get_friend_details(self):
        full_url = f'user.info?handles={self.__username}'
        url = CODEFORCES_URL+full_url

        friend_list = self.__username.split(';')

        result = {'status': STATE_PENDING}

        try:
            response = requests.get(url)
            json_object = response.json()

            for data, friend in zip(json_object['result'], friend_list):

                try:
                    temp_result = {}
                    temp_result['status'] = STATE_PASS

                    temp_result['name'] = data['firstName'] + \
                        ' ' + data['lastName']
                    temp_result['username'] = friend
                    temp_result['rank'] = data['rank']
                    temp_result['rating'] = data['rating']
                    temp_result['avatar'] = 'https:'+data['titlePhoto']
                    temp_result['city'] = data['city']
                    temp_result['country'] = data['country']
                    temp_result['organization'] = data['organization']

                    result[friend] = temp_result
                except:
                    temp_result = {
                        'status': STATE_ERROR_INVALID_USER, 'username': friend}
                    result[friend] = temp_result
        except:
            result = {'status': STATE_ERROR_INVALID_USER,
                      'username': self.__username}
        finally:
            return result

    def get_past_submissions(self):
        full_url = f'user.status?handle={self.__username}&from=1&count=100'
        url = CODEFORCES_URL+full_url

        result = {'status': STATE_PENDING}

        try:
            response = requests.get(url)
            json_object = response.json()

            result['status'] = STATE_PASS
            result['result'] = json_object['result']
        except:
            result = {'status': STATE_ERROR_INVALID_USER,
                      'username': self.__username}
        finally:
            return result

    def get_basic_details(self):
        full_url = f'user.rating?handle={self.__username}'
        url = CODEFORCES_URL+full_url

        result = {'status': STATE_PENDING}

        try:
            response = requests.get(url)
            json_object = response.json()

            result['status'] = STATE_PASS
            result['result'] = json_object['result']
        except:
            result = {'status': STATE_ERROR_INVALID_USER,
                      'username': self.__username}
        finally:
            return result

    def get_contest_details(self):
        ful_url = f'user.rating?handle={self.__username}'
        url = CODEFORCES_URL+ful_url

        result = {'status': STATE_PENDING}

        try:
            response = requests.get(url)
            json_object = response.json()
            result['status'] = STATE_PASS
            result['contest'] = json_object['result']
        except:
            result = {'status': STATE_ERROR_INVALID_USER,
                      'username': self.__username}
        finally:
            return result


def get_problems_by_tags(tags):
    full_url = f'problemset.problems?tags={tags}'
    url = CODEFORCES_URL+full_url

    result = {'status': STATE_PENDING}

    try:
        response = requests.get(url)
        json_object = response.json()

        result['status'] = STATE_PASS
        result['problems'] = json_object['result']
    except:
        result = {'status': STATE_ERROR_IN_CODEFORCES_TAGS}
    finally:
        return result