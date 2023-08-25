

### Script of data processing:
##### Creating author - paper database:
* [data/scientists.csv](./data/scientists.csv) is file downloaded with filter "dispcipline = psychologia" from [radon database](https://radon.nauka.gov.pl/dane/nauczyciele-akademiccy-badacze-i-osoby-zaangazowane-w-dzialalnosc-naukowa)
Registration in that database is obligatory for all active scientists who work within Polish system of higher education, regulated by law. See [limitations](./wikifiles/Limitations.md).
* Raw dataset was processed using [data_creation_code/wrangle_scientists.py](./data_creation_code/wrangle_scientists.py) and split by affiliation into names.csv in data/institutions/affiliation folders.
* Those files are manually extended by adding scientists' Orcid link and email via project's Google Drive. Filled files are in [anonymized folder](./anonymized/readme.md). 
* For those scientists who have Orcid profile with at least one work listed, we used [data_creation_code/scrape_orcids.py](./data_creation_code/scrape_orcids.py) to get a list of their works