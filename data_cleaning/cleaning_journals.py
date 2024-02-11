import pandas as pd
import string
import pickle
from tqdm import tqdm


article_list = pd.read_csv('official_repo/data/Orcid_raw_article_list.csv')

journals = list(article_list['journal'].unique())
# alphabetically
# get rid of nans
journals = [j for j in journals if str(j) != 'nan']
journals.sort()

def levenshtein_distance(stringA, stringB):
    # Convert to lowercase
    stringA = stringA.lower()
    stringB = stringB.lower()

    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    stringA = stringA.translate(translator)
    stringB = stringB.translate(translator)

    if len(stringA) > len(stringB):
        stringA, stringB = stringB, stringA

    distances = list(range(len(stringA) + 1))
    for index2, char2 in enumerate(stringB):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(stringA):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min(distances[index1], distances[index1 + 1], new_distances[-1]))
        distances = new_distances

    return distances[-1]


assorted_dict = {}
assorted_list = []
# i = 0
for journal in tqdm(journals):
    temp_list = []
    if journal in assorted_list:
        continue
    assorted_list.append(journal)
    for other_journal in journals:
        if journal != other_journal:
            distance = levenshtein_distance(journal, other_journal)
            if distance < 3:
                temp_list.append(other_journal)

    assorted_dict[journal] = temp_list


# with open('assorted_journals.pickle', 'rb') as f:
#     assorted_dict = pickle.load(f)
#
# with open('assorted_journals_list.pickle', 'rb') as f:
#     assorted_list = pickle.load(f)
#
# with open('assorted_journals_i.pickle', 'rb') as f:
#     i = pickle.load(f)







# i = 0
for journal in journals:
    i += 1
    temp_dict = {}
    temp_list = []
    if journal in assorted_list:
        continue
    print('Original:')
    print('############################               ', journal, '               ############################')
    assorted_list.append(journal)
    for other_journal in journals[i:]:
        if other_journal in assorted_list:
            continue
        if journal != other_journal:
            distance = levenshtein_distance(journal, other_journal)
            temp_dict[other_journal] = distance
        # sort the temp_dict
    sorted_dict = sorted(temp_dict.items(), key=lambda x: x[1])
    for k, v in sorted_dict:
        print('Pretendent match:')
        print('############################               ', k, '               ############################')
        x = input('Is this the same journal? (y/n)')
        if x == 'y':
            temp_list.append(k)
            assorted_list.append(k)
            print('ACCEPTED')
        else:
            assorted_dict[journal] = temp_list
            print('REJECTED')
            print('====================================================================================================================================================')  # separator
            print('====================================================================================================================================================')  # separator
            print('====================================================================================================================================================')  # separator
            print(f'============================================= Left to assort: {i}, {len(journals)}================================================')  # separator
            print('====================================================================================================================================================')
            print('====================================================================================================================================================')  # separator
            print('====================================================================================================================================================')  # separator
            break

    # save the temp_list to the assorted_dict to pickle
    with open('assorted_journals.pickle', 'wb') as f:
        pickle.dump(assorted_dict, f)

    with open('assorted_journals_list.pickle', 'wb') as f:
        pickle.dump(assorted_list, f)

    # save i
    with open('assorted_journals_i.pickle', 'wb') as f:
        pickle.dump(i, f)




