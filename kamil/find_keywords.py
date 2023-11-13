import pandas as pd
import os
import PyPDF2
import re
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
import pickle

PDF_DIR = r'D:\data\ranking\pdfs'

def pdf_to_text(url):
    pdfFileObj = open(url, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict = False)
    # text = []
    text = ''
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        # text.append(pageObj.extractText())
        text += pageObj.extractText()
    # if idx == 8:
    return text, pdfReader.numPages


eng_keywords_df = pd.read_csv('kamil/words_EN.csv', encoding = 'utf-8')
eng_keywords_df = eng_keywords_df[eng_keywords_df['core'] != 'Group']
pl_keywords_df = pd.read_csv('kamil/words_PL.csv', encoding = 'utf-8')
pl_keywords_df = pl_keywords_df[pl_keywords_df['core'] != 'Grup']


def create_patterns(keyword_phrases):
    regex_patterns = []

    for phrase in keyword_phrases:
        # Split the phrase on space to handle individual words
        parts = phrase.split()

        # Create regex for each part
        regex_parts = []
        for part in parts:
            first_letter = part[0]
            rest_of_word = part[1:]
            # Replace '*' with '\w*' for word characters, and escape other special characters
            regex_part = f'[{first_letter.upper()}{first_letter.lower()}]{rest_of_word}'.replace(r"\*", r"\w*")
            regex_parts.append(regex_part)

        # Join the regex parts with '\s+' to account for any amount of whitespace
        pattern = r"\s+".join(regex_parts)

        # Add word boundary to the beginning and end to ensure we match whole words
        pattern = r"\b" + pattern + r"\b"

        regex_patterns.append(pattern)

    return regex_patterns

def extract_context(text, compiled_patterns, original_keywords, context_size=5):
    pattern_list = []
    snippet_list = []
    for pattern , orig_key in zip(compiled_patterns, original_keywords):
        sentences = sent_tokenize(text)
        # Find all matches and their sentence indices
        matches = [(i, s) for i, s in enumerate(sentences) if pattern.search(s)]

        # Extract context around the matches
        extracted_contexts = []
        for match_index, _ in matches:
            start = max(0, match_index - context_size)
            end = min(len(sentences), match_index + context_size + 1)
            context = " ".join(sentences[start:end])
            extracted_contexts.append(context)

        snippet_list.extend(extracted_contexts)
        pattern_list.extend([orig_key]*len(extracted_contexts))

    return pattern_list, snippet_list


eng_keywords = create_patterns([key.lower() for key in eng_keywords_df['core']])
pl_keywords = create_patterns([key.lower() for key in pl_keywords_df['core']])
original_eng_keywords = eng_keywords_df['core'].values
original_pl_keywords = pl_keywords_df['core'].values
eng_keywords = [re.compile(pattern) for pattern in eng_keywords]
pl_keywords = [re.compile(pattern) for pattern in pl_keywords]


eng_patterns_list = []
eng_snippets_list = []
pl_patterns_list = []
pl_snippets_list = []
file_list_en = []
file_list_pl = []
failed = []
for file in tqdm(os.listdir(PDF_DIR)):
    try:
        text, pages  = pdf_to_text(os.path.join(PDF_DIR, file))
        if pages > 50:
            continue
        eng_patterns, eng_snippets = extract_context(text, eng_keywords, original_eng_keywords)
        pl_patterns, pl_snippets = extract_context(text, pl_keywords, original_pl_keywords)

        eng_patterns_list.extend(eng_patterns)
        eng_snippets_list.extend(eng_snippets)
        pl_patterns_list.extend(pl_patterns)
        pl_snippets_list.extend(pl_snippets)
        file_list_en.extend([file]*len(eng_patterns))
        file_list_pl.extend([file]*len(pl_patterns))
    except:
        failed.append(file)

# save separately
eng_df = pd.DataFrame({'file': file_list_en, 'pattern': eng_patterns_list, 'snippet': eng_snippets_list})
eng_df = pd.DataFrame({'file': file_list_en, 'pattern': eng_patterns_list, 'snippet': eng_snippet_new})
pl_df = pd.DataFrame({'file': file_list_pl, 'pattern': pl_patterns_list, 'snippet': pl_snippets_list})

# save
eng_df.to_csv('kamil/eng_key_results.csv', escapechar='\\', index=False)
pl_df.to_csv('kamil/pl_key_results.csv', index = False)


# save failed
with open('kamil/failed.pkl', 'wb') as f:
    pickle.dump(failed, f)
