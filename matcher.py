import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# Create Embedder
model_folder = './transformer_model'
embedder = SentenceTransformer('distiluse-base-multilingual-cased-v1', cache_folder=model_folder)


def index_search(embeddings, text_query):
    n_cells = 240
    num_dimensions = embeddings.shape[1]
    quantizer = faiss.IndexFlatL2(num_dimensions)
    index = faiss.IndexIVFFlat(quantizer, num_dimensions, n_cells)
    index.train(embeddings)
    index.add(embeddings)

    query_embedding = embedder.encode([text_query])
    num_results = 10
    distances, indexes = index.search(query_embedding, num_results)
    valid_indexes = indexes[0][indexes[0] != -1]
    return valid_indexes


#     job_full_embeddings = embedder.encode(job_df["job_full"].values)
#     np.save('job_full_embeddings.npy', job_full_embeddings)


def show_job_rec(valid_indexes, df):
    search_results_df = pd.DataFrame(columns=['Company', 'Location', 'Job title', 'Skills', 'Requirements', 'Preference', 'Role and responsibilities'])
    relevant_rows = df.iloc[valid_indexes]
    for i, row in relevant_rows.iterrows():
        # job_index = row['index']
        company = row['company']
        location = row['joblocation_address']
        job_title = row['job_title']
        skills = row['skills']
        req = row['job_req']
        pref = row['job_expab']
        role = row['job_role']

        new_row = {'Company': company,
                   'Location': location,
                   'Job title': job_title,
                   'Skills': skills,
                   'Requirements': req,
                   'Preference': pref,
                   'Role and responsibilities': role
                   }
        search_results_df = pd.concat([search_results_df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

    return search_results_df


def show_resume_rec(valid_indexes, df):
    search_results_df = pd.DataFrame(columns=['Work exp title', 'Skills', 'Education', 'Key work exp'])
    relevant_rows = df.iloc[valid_indexes]
    for i, row in relevant_rows.iterrows():
        # resume_index = row['index']
        work_exp_title = row['work_exp_title']
        skills = row['skill_list']
        edu = row['Education']
        resume_key_act = row['key_act_clean']

        new_row = {
                   'Work exp title': work_exp_title,
                   'Skills': skills,
                   'Education': edu,
                   'Key work exp': resume_key_act,
                   }
        search_results_df = pd.concat([search_results_df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

    return search_results_df


def recommend_resume(text_query):
    resume_df = pd.read_pickle('./resume_final.pkl')
    resume_full_embeddings = np.load('./resume_full_embeddings.npy')
    indexes = index_search(resume_full_embeddings, text_query)
    rec_results = show_resume_rec(indexes, resume_df)
    return rec_results


def recommend_job(text_query):
    job_df = pd.read_pickle('./job_final.pkl')
    job_full_embeddings = np.load('./job_full_embeddings.npy')
    indexes = index_search(job_full_embeddings, text_query)
    rec_results = show_job_rec(indexes, job_df)
    return rec_results
