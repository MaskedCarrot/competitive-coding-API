from datetime import datetime
import pytz
import requests
import json
from constants import *

epoch = datetime.utcfromtimestamp(0)
time_format = '%Y-%m-%dT%H:%M:%S'
time_str = datetime.now(pytz.timezone('UTC')).strftime(time_format)


def get_contests():
    result = {'status': STATE_PENDING, 'contests': []}

    full_url = f"{CLIST_KEY}&start__gte={time_str}&resource__id__in={CODEFORCES_CLIST_ID},{CODECHEF_CLIST_ID},{GOOGLE_CLIST_ID},{ATCODER_CLIST_ID}"
    url = CLIST_URL+full_url
    response = requests.get(url)

    json_object = response.json()
    data = json_object['objects']

    for contest in data:

        temp = {}

        if((contest['resource'])['id'] == CODEFORCES_CLIST_ID):
            temp['id'] = CODEFORCES_ID
        elif((contest['resource'])['id'] == CODECHEF_CLIST_ID):
            temp['id'] = CODECHEF_ID
        elif((contest['resource'])['id'] == GOOGLE_CLIST_ID):
            temp['id'] = GOOGLE_ID
        elif((contest['resource'])['id'] == ATCODER_CLIST_ID):
            temp['id'] = ATCODER_ID
        else:
            continue

        start_time_str = contest['start']
        end_time_str = contest['end']
        start_time_object = datetime.strptime(start_time_str, time_format)
        end_time_object = datetime.strptime(end_time_str, time_format)

        temp['href'] = contest['href']
        temp['event'] = contest['event']
        temp['duration'] = contest['duration'] * 10
        temp['start_time'] = int(
            (start_time_object - epoch).total_seconds() * 100)
        temp['end_time'] = int((end_time_object - epoch).total_seconds() * 100)

        result['contests'].append(temp)

    return json.dumps(result, indent=4)


if __name__ == '__main__':
    print(get_contests())
