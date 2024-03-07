import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
from Levenshtein import distance as levenshtein_distance
import pandas as pd
import pickle
import re

article_list = pd.read_csv('official_repo/data/Orcid_raw_article_list.csv')

titles = list(article_list['journal'].unique())
titles = [j for j in titles if str(j) != 'nan']
titles.sort()

def clean_title(title):
    # Convert to lowercase
    title = title.lower()
    # Remove numbers
    title = re.sub(r'\d+', '', title)
    # Remove punctuation
    title = re.sub(r'[^\w\s]', '', title)
    return title

def compute_clusters(titles, epsilon= 0.1, cleaned = False):
    # Assume `titles` is your list of journal titles

    # Step 1: Compute TF-IDF vector similarity
    if cleaned:
        original_titles = titles
        titles = [clean_title(title) for title in titles]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(titles)
    cosine_sim = cosine_similarity(tfidf_matrix)

    # Step 2: Compute pairwise Levenshtein distances
    # Normalize Levenshtein distances to be between 0 and 1
    levenshtein_dist_matrix = np.array([[levenshtein_distance(t1, t2) for t2 in titles] for t1 in titles])
    levenshtein_dist_matrix = levenshtein_dist_matrix / np.max(levenshtein_dist_matrix)

    # Step 3: Combine the similarities/distances
    # Here, we simply average the normalized TF-IDF cosine similarity and the normalized Levenshtein distance
    # Note: You might want to experiment with different ways of combining these two measures
    combined_dist_matrix = 0.3 * abs((1 - cosine_sim)) + 0.7 * levenshtein_dist_matrix

    # Step 4: Cluster using DBSCAN
    # Adjust `eps` and `min_samples` as necessary based on your combined distance matrix
    dbscan = DBSCAN(eps=epsilon, min_samples=2, metric="precomputed")
    clusters = dbscan.fit_predict(combined_dist_matrix)

    if cleaned:
        # Output the clusters
        grouped_titles = {}
        for i, cluster_label in enumerate(clusters):
            if cluster_label not in grouped_titles:
                grouped_titles[cluster_label] = []
            grouped_titles[cluster_label].append(original_titles[i])

        return grouped_titles

    # Output the clusters
    grouped_titles = {}
    for i, cluster_label in enumerate(clusters):
        if cluster_label not in grouped_titles:
            grouped_titles[cluster_label] = []
        grouped_titles[cluster_label].append(titles[i])

    return grouped_titles



not_to_add = [230, 187, 173, 169, 156, 140, 139, 128, 115, 99, 98, 93, 89, 88, 84, 82, 75, 73, 72, 70, 69, 68, 59, 48, 43, 34, 31,
              30, 29, 23, 22, 20, 14, 10]

for c_id in range(len(grouped_titles)-1):
    if c_id in not_to_add:
        continue
    add(grouped_titles[c_id])

# save the assorted list
with open('assorted_journals.pickle', 'wb') as f:
    pickle.dump(assorted_list, f)

# load
with open('assorted_journals.pickle', 'rb') as f:
    assorted_list = pickle.load(f)

all_values = list(assorted_list.values())
# flatten
all_values = [item for sublist in all_values for item in sublist]


# valued to keys
reversed_assorted_list =  {}
for key, value in assorted_list.items():
    for v in value:
        reversed_assorted_list[v] = key


titles_2 = []
for title in titles:
    if title not in all_values:
        titles_2.append(title)
    else:
        key = reversed_assorted_list[title]
        if key not in titles_2:
            titles_2.append(key)



a = compute_clusters(titles_2, epsilon = 0.2)

not_to_add = [112, 104, 103, 100, 98, 93, 92, 91, 90, 89, 86, 85, 84, 83,
              82, 81, 79, 77, 76, 75, 74, 73, 71, 70, 68, 67, 66, 65, 64, 60,
              59, 58, 56, 55, 54, 53, 52, 50, 49, 48, 47, 45, 44, 43, 40, 39,
              38, 37, 35, 34, 33, 31, 30, 29, 28, 27, 26, 25, 23, 22, 21, 20,
              19, 18, 17, 15, 14, 13, 12, 10, 8, 7, 4, 3, 2, 0]

def add(cluster):
    global assorted_list
    collate = []
    for component in cluster:
        if component in assorted_list.keys():
            collate.append(assorted_list[component])
            # delete the key for now
            del assorted_list[component]
        else:
            collate.append([component])
    collate = [item for sublist in collate for item in sublist]

    assorted_list[collate[0]] = collate

for c_id in range(len(a)-1):
    if c_id in not_to_add:
        continue
    add(a[c_id])


# save
with open('assorted_journals2.pickle', 'wb') as f:
    pickle.dump(assorted_list, f)

# load
with open('assorted_journals2.pickle', 'rb') as f:
    assorted_list = pickle.load(f)

all_values = list(assorted_list.values())
# flatten
all_values = [item for sublist in all_values for item in sublist]

# valued to keys
reversed_assorted_list =  {}
for key, value in assorted_list.items():
    for v in value:
        reversed_assorted_list[v] = key


titles_3 = []
for title in titles:
    if title not in all_values:
        titles_3.append(title)
    else:
        key = reversed_assorted_list[title]
        if key not in titles_3:
            titles_3.append(key)

a = compute_clusters(titles_3, epsilon = 0.25)

leftover = [title for title in titles if title not in all_values]


to_add = [82, 77, 74, 71, 39, 34, 31, 15]


separate_adds = [['Polish Psychological Bulletin',
  'Polish Psychological Bulletin, 237-246.',
  'Polish Psychological Bulletin, 49 (1), pp 1-2',
  'Polish Psychological Bulletin.'],

                 ['Environmental Research',
  'Environmental research'],

['Women & Health',
  'Women and Health'],


['European Journal of Psychological Assessmen',
  'European Journal of Psychological Assessment'],


['Annals of Psychology / Roczniki Psychologiczne',
  'Roczniki Psychologiczne',
  'Roczniki Psychologiczne = Annals of Psychology',
'Annals of Psychology'
        ]

                 ]

for c_id in range(len(a)-1):
    if c_id in to_add:
        add(a[c_id])

for cluster in separate_adds:
    add(cluster)

# save
with open('assorted_journals3.pickle', 'wb') as f:
    pickle.dump(assorted_list, f)


# load
with open('assorted_journals3.pickle', 'rb') as f:
    assorted_list = pickle.load(f)

all_values = list(assorted_list.values())
# flatten
all_values = [item for sublist in all_values for item in sublist]

# valued to keys
reversed_assorted_list =  {}
for key, value in assorted_list.items():
    for v in value:
        reversed_assorted_list[v] = key


titles_4 = []
for title in titles:
    if title not in all_values:
        titles_4.append(title)
    else:
        key = reversed_assorted_list[title]
        if key not in titles:
            titles_4.append(key)


a = compute_clusters(titles_4, epsilon = 0.2, cleaned  = True)

to_add = [82, 75, 74, 72, 71, 69, 68, 43, 35, 30, ]


separate_adds = [
    ['FIDES ET RATIO',
  'Fides et Ratio',
  'Quaterly Journal Fides et Ratio'],
    ['Człowiek i Społeczeństwo',
  'Człowiek i Społeczeństwo, 51, 109-126'],

    ['Czasopismo Psychologiczne -Pychological Journal',
  'Czasopismo Psychologiczne Psychological Journal (CPPJ)',
  'Czasopismo Psychologiczne, 23(1), 137-146',
  'Czasopismo Stomatologiczne',
  'Czasopsmo Psychologiczne, Psychological Journal',
  'Czassopismo Psychologiczne, Psychological Journal'],
 ['Adaptive Behavior',
  'Addictive Behaviors']
]

for c_id in range(len(a)-1):
    if c_id in to_add:
        add(a[c_id])

for cluster in separate_adds:
    add(cluster)

# save
with open('assorted_journals4.pickle', 'wb') as f:
    pickle.dump(assorted_list, f)


# load
with open('assorted_journals4.pickle', 'rb') as f:
    assorted_list = pickle.load(f)

all_values = list(assorted_list.values())
# flatten
all_values = [item for sublist in all_values for item in sublist]

# values to keys
reversed_assorted_list =  {}
for key, value in assorted_list.items():
    for v in value:
        reversed_assorted_list[v] = key

titles_5 = []
for title in titles:
    if title not in all_values:
        titles_5.append(title)
    else:
        key = reversed_assorted_list[title]
        if key not in titles:
            titles_5.append(key)