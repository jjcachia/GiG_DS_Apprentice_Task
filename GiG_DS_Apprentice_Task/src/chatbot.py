import os
import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append(os.path.abspath(os.path.join("..")))
from src.utils import prepare_text


class ChatbotV1:
    def __init__(self, data_dir, data_file="cleaned_gig_docs.csv", tfidf_file="tfidf_data.pkl"):
        self.data_dir = data_dir
        self.data_path = os.path.join(data_dir, data_file)
        self.tfidf_path = os.path.join(data_dir, tfidf_file)

        # Load the data
        self.df = pd.read_csv(self.data_path, index_col='Doc_ID')

        with open(self.tfidf_path, "rb") as f:
            tfidf_data = pickle.load(f)
        
        self.vectorizer = tfidf_data["vectorizer"]
        self.tfidf_matrix = tfidf_data["matrix"]
        self.doc_ids = tfidf_data["doc_ids"]

    def find_answer(self, user_question):
        answer_doc_id = self.__match_question_tfidf(user_question)
        answer = self.__get_answer_by_id(answer_doc_id)
        return answer, answer_doc_id

    def __match_question_tfidf(self, user_question):

        question_cleaned = prepare_text(user_question)
        question_cleaned = " ".join(question_cleaned)

        query_vector = self.vectorizer.transform([question_cleaned])

        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        best_idx = np.argmax(similarities)
        best_doc_id = self.doc_ids[best_idx]

        return best_doc_id

    def __get_answer_by_id(self, doc_id):
        if doc_id in self.df.index:
            return self.df.loc[doc_id, 'Answer_Snippet']
        return None
    
