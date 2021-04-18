from contests import get_contests
import json 

contests_json = json.loads(get_contests())
with open('data/contests.json', 'w') as outfile:
    json.dump(contests_json, outfile)

