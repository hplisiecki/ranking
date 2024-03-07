import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cdist
from Levenshtein import distance as levenshtein_distance
from tqdm import tqdm
import re
import pickle
article_list = pd.read_csv('official_repo/data/Orcid_raw_article_list.csv')

titles = list(article_list['journal'].unique())
titles = [j for j in titles if str(j) != 'nan']
titles.sort()

# load
with open('assorted_journals4.pickle', 'rb') as f:
    assorted_list = pickle.load(f)

all_values = list(assorted_list.values())
# flatten
all_values = [item for sublist in all_values for item in sublist]

# valued to keys
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

wykaz = pd.read_excel('data/wykaz_czasopism.xlsx', header=0)

# first row are the column names
wykaz.columns = wykaz.iloc[0]
wykaz = wykaz[1:]

wykaz_names = list(wykaz['Tytuł 1'])
wykaz_names = [j for j in wykaz_names if str(j) != 'nan']

def clean_title(title):
    # Convert to lowercase
    title = title.lower()
    # Remove numbers
    title = re.sub(r'\d+', '', title)
    # Remove punctuation
    title = re.sub(r'[^\w\s]', '', title)
    return title

def compute_closest_titles(original_titles, query_titles, X=3):
    # Clean titles
    cleaned_original_titles = [clean_title(title) for title in original_titles]
    cleaned_query_titles = [clean_title(title) for title in query_titles]

    # Compute TF-IDF vector similarity for the cleaned original titles
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_original_titles)
    cosine_sim = cosine_similarity(tfidf_matrix)

    # Compute pairwise Levenshtein distances for the cleaned original titles
    levenshtein_dist_matrix = np.array([[levenshtein_distance(t1, t2) for t2 in cleaned_original_titles] for t1 in cleaned_original_titles])
    levenshtein_dist_matrix = levenshtein_dist_matrix / np.max(levenshtein_dist_matrix)

    # Initialize an empty DataFrame
    columns = ['Original Title'] + [f'Closest {i+1}' for i in range(X)]
    results_df = pd.DataFrame(columns=columns)

    # For each title in the cleaned query list, find the X closest titles from the cleaned original list
    collate_df = []
    for query_title in tqdm(cleaned_query_titles):
        # Compute distances from the query title to each cleaned original title
        query_vector = vectorizer.transform([query_title])
        query_cosine_sim = cosine_similarity(query_vector, tfidf_matrix).flatten()
        query_levenshtein_dist = np.array([levenshtein_distance(query_title, t) for t in cleaned_original_titles]) / np.max(levenshtein_dist_matrix)
        query_combined_dist = 0.3 * abs((1 - query_cosine_sim)) + 0.7 * query_levenshtein_dist

        # Find the indices of the X closest titles
        closest_indices = np.argsort(query_combined_dist)[:X]

        # Select the closest titles and add them to the DataFrame
        closest_titles = [original_titles[i] for i in closest_indices]  # Use original (not cleaned) titles for display
        collate_df.append(pd.DataFrame([[query_title] + closest_titles], columns=columns))

    results_df = pd.concat(collate_df, ignore_index=True)
    return results_df


# Example usage
closest_titles_df = compute_closest_titles(wykaz_names, titles_5, X=3)
print(closest_titles_df)

# save
closest_titles_df.to_csv('data/journal_cleaning/closest_titles.csv', index=False)

# to excel
closest_titles_df.to_excel('data/journal_cleaning/closest_titles.xlsx', index=False)

import pandas as pd
import re
# load
closest_titles_df = pd.read_csv('data/journal_cleaning/closest_titles.csv')
# dropnan
closest_titles_df = closest_titles_df.dropna(subset=['Original Title'])
article_list = pd.read_csv('official_repo/data/New_ID_Orcid_raw_article_list.csv')
# sort

# dropna from journals
article_list = article_list.dropna(subset=['journal'])

article_list['clean_titles'] = article_list['journal'].apply(clean_title)

collate_doi = []
collate_id = []
collate_orcid = []
for idx, original_title in enumerate(closest_titles_df['Original Title']):
    article_doi = article_list[article_list['clean_titles'] == original_title]['doi'].iloc[0]
    article_id = article_list[article_list['clean_titles'] == original_title]['Article_ID'].iloc[0]
    article_orcid = article_list[article_list['clean_titles'] == original_title]['orcid'].iloc[0]
    collate_doi.append(article_doi)
    collate_id.append(article_id)
    collate_orcid.append(article_orcid)

closest_titles_df['doi'] = collate_doi
closest_titles_df['Article_ID'] = collate_id
closest_titles_df['ORCID'] = collate_orcid
# save
closest_titles_df.to_csv('data/journal_cleaning/closest_titles_with_doi.csv', index=False)
# to excel
closest_titles_df.to_excel('data/journal_cleaning/closest_titles_with_doi.xlsx', index=False)

# load
closest_titles_df = pd.read_csv('data/journal_cleaning/closest_titles_with_doi.csv')