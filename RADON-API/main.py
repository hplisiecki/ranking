from radon_api import get_works_from_API
from utils import list_of_scientists
import time

list_od_scientists = list_of_scientists()

lastToken = 'MTY5ODY2Njc0Mzk2OQ=='

i=0
r = [0] * len(list_od_scientists)
c = [0] * len(list_od_scientists)
t = [0] * len(list_od_scientists)

update_lists_of_scientist = []

for scientist in list_od_scientists:
    print(i)
    fistName = scientist['firstName']
    lastName = scientist['lastName']
    try:
        r[i], c[i], t[i] = get_works_from_API(fistName,lastName,lastToken)
        if t[i] is not None:
            lastToken = t[i]
    except:
        r[i]= 'error'
        c[i]= 'error'
        t[i]= 'error'
        
    dict = {'n_results': c[i],
            'results': r[i]
            }
    
    scientist.update(dict)
    update_lists_of_scientist.append(scientist)

    time.sleep(2)
    i += 1

import json
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(update_lists_of_scientist, f)