import pandas as pd
import re
from find_job_titles import Finder
from nltk import tokenize
import pickle


def extract_edu(text):
    pattern = r'Education\s*(.*?)(?=\s*(?:Contact|Summary|Work Experience|Experience|Skill|Technical Skill|Certification|Project|Award|Publication|Affiliation|Volunteer|Interest|Hobb|Reference})|$)'
    resume_edu = re.findall(pattern, text)
    return ", ".join(resume_edu)


def extract_skill(text):
    pattern = r'(?:Skills|SKILLS|Technical Skills|Framework|Languages)([^,]{1,35}(?:\(.*year\))?,[^,]{1,35}(?:\(.*year\))?,.*?)(?=\s*(?:Education|Contact|Summary|SUMMARY|Work Experience|Experience|Certification|Award|Publication|Affiliation|Volunteer|Interest|Hobb|Reference|Links|Additional)|$)'
    resume_skill = re.findall(pattern, text)
    resume_skill = ", ".join(resume_skill)
    resume_skill = re.sub(r'\s\([\w\s\d+]+\s(?:year)s?\)', '', resume_skill)
    return resume_skill


def extract_title(text):
    finder = Finder()
    try:
        result = finder.findall(text)
    except RuntimeError:
        return None
    job_titles = set()
    for each in result:
        if " " in each.match:
            job_titles.add(each.match)
    return ", ".join(job_titles)


def sentence_segmentation(text):
    matches = re.finditer(r"\s{2,}", text)
    positions = [match.start() for match in matches]
    offset = 0
    for index in positions:
        text = text[:index+offset] + '.' + text[index+offset:]
        offset += 1
    text = text.replace("\n", ". ").replace("\t", ". ")
    text = re.sub(r'(\w)\s+[^a-zA-Z0-9\s,\.\(\)]{1,}', r'\1. ', text)
    text = re.sub(r'([\.,;])\s*[^a-zA-Z0-9\s,\.\(\)]{1,}', r'\1', text)
    return tokenize.sent_tokenize(text)


def valid_sentence(sentence_list):
    filtered_strings = []
    for string in sentence_list:
        words = string.split()
        word_count = sum(1 for word in words if word != ".")
        comma_count = string.count(',')
        if word_count >= 6 and word_count <= 70 and comma_count <= 6:
            filtered_strings.append(string)
    return filtered_strings


def extract_activity_phrase(sentence_list):
    with open('nlp_model.pkl', 'rb') as file:
        nlp = pickle.load(file)
    stop_verbs = {
        'have',
        'must',
        'do',
        'be',
        'can',
        'could',
        'will',
        'would',
        'shall',
        'should',
        'may',
        'might',
        'must',
        'include',
        'follow'
    }

    condensed_sentence_list = []
    for sentence in sentence_list:
        activity_phrase = []
        doc = nlp(sentence)

        find_verb = False
        find_noun = False

        for token in doc:
            if not find_verb:
                if token.pos_ == 'VERB' and token.lemma_ not in stop_verbs:
                    activity_phrase.append(token.lemma_)
                    find_verb = True
            else:
                if token.pos_ not in ['NOUN', 'PRON']:
                    if find_noun:
                        break
                    if token.lemma_ in stop_verbs:
                        continue
                    if token.pos_ == 'VERB':
                        activity_phrase.append(token.lemma_)
                        continue
                    activity_phrase.append(token.text)
                else:
                    activity_phrase.append(token.text)
                    find_noun = True

        if 2 <= len(activity_phrase) <= 20:
            condensed_sentence = ' '.join(activity_phrase)
            condensed_sentence_list.append(condensed_sentence)
    return ', '.join(condensed_sentence_list)


def extract_from_resume(text):
    resume_edu = extract_edu(text)
    resume_skill = extract_skill(text)
    resume_title = extract_title(text)
    sentence_list = valid_sentence(sentence_segmentation(text))
    resume_act = extract_activity_phrase(sentence_list)
    return resume_title, resume_title + '. ' + resume_skill + '. ' + resume_edu + '. ' + resume_act

    # print(resume_edu)
    # print(resume_skill)
    # print(resume_title)
    # print(resume_act)
