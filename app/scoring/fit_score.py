from app.core.embeddings import embed
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def fit_score(job_text, resume_text):

    job_vec = np.array(embed(job_text)).reshape(1, -1)
    resume_vec = np.array(embed(resume_text)).reshape(1, -1)

    score = cosine_similarity(job_vec, resume_vec)[0][0]

    return round(score * 100, 2)
