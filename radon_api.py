import requests
import json
 


# curl -X 'GET' \
#   'https://radon.nauka.gov.pl/opendata/polon/publications?resultNumbers=100&firstName=Micha%C5%82&lastName=Bilewicz&yearFrom=2017&yearTo=2021' \
#   -H 'accept: application/json'

def get_works_from_API(fistName, lastName, lastToken = None, fromY = "2017", toY = '2021'):
    params = {}
    
    if lastToken == lastToken: params['token'] = lastToken

    params.update({
        'resultNumbers' : 100,
        'firstName'     : fistName,
        'lastName'      : lastName,
        'yearFrom'      : fromY,
        'yearTo'        : toY,
    })

    response = requests.get('https://radon.nauka.gov.pl/opendata/polon/publications', params=params)

    data = response.text
    data = json.loads(data)

    # try:
    results = data.get('results')
    count = data.get('pagination').get('maxCount')
    newlastToken = data.get('pagination').get('token')
    if newlastToken is not None:
        with open(r'D:\PycharmProjects\ranking\RADON-API\lastToken.txt', 'w', encoding='utf8') as f:
            f.write(newlastToken)
    print(fistName, lastName, count, "works. New last token: ", newlastToken)
    if count >= 100: print('Warning, to much works to download!')
    return (results, count, newlastToken)
    # except:
    #     print(response)


# lastToken = "MTY5ODY3NzE0MjcyOQ=="
# fistName = "Rafał"
# lastName = "Abramciów"
#
# r, c, t = get_works_from_API(fistName, lastName, lastToken)