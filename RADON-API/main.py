import sys
# append system path
sys.path.append('RADON-API')


from radon_api import get_works_from_API
from utils import list_of_scientists
import time
from tqdm import tqdm

list_of_scientists = list_of_scientists()

lastToken = None

i=0
r = [0] * len(list_of_scientists)
c = [0] * len(list_of_scientists)
t = [0] * len(list_of_scientists)

update_lists_of_scientist = []

def retry_call(fistName, lastName, lastToken):
    res = get_works_from_API(fistName, lastName, lastToken)
    if res[2] is None:
        print("Retry")
        lastToken = None
        time.sleep(2)
        res = retry_call(fistName, lastName, lastToken)

    return res

fromY = "2017"
toY = '2021'

i = 0
for scientist in tqdm(list_of_scientists):
    scientist = list_of_scientists[i]
    fistName = scientist['firstName']
    lastName = scientist['lastName']
    res = retry_call(fistName,lastName,lastToken)

    if res[2] is not None:
        lastToken = res[2]
    else:
        break

    dict = {'n_results': res[1],
            'results': res[0]
            }
    
    scientist.update(dict)
    update_lists_of_scientist.append(scientist)

    time.sleep(1)
    i+=1

import json
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(update_lists_of_scientist, f)