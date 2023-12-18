import requests

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

    data = response.json()

    try:
        results = data.get('results')
        count = data.get('pagination').get('maxCount')
        newlastToken = data.get('pagination').get('token')

        with open('lastToken.txt', 'w', encoding='utf8') as f:
            f.write(lastToken)
        print(fistName, lastName, count, "works. New last token: ", newlastToken)
        if count > 99: print('Warning, to much works to download!')
        return results, count, newlastToken
    
    except:
        print(response)