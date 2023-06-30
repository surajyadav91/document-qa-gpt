import pandas as pd
import numpy as np
from datasets import load_from_disk
import openai

openai.api_key = open("key.txt", "r").read()

class Retriever:
    def __init__(self,config):
        self.hf_dataset = load_from_disk(config['hf_dataset'])
        self.hf_dataset.load_faiss_index('embedding',config['faiss_index_path'])
        self.embedding_model = config['embedding_model']
        self.top_k = config['top_k']

    def retrieve(self, question):
        question_embedding = openai.Embedding.create(input=question,model=self.embedding_model)['data'][0]['embedding']
        question_embedding = np.array(question_embedding)

        scores,samples = self.hf_dataset.get_nearest_examples('embedding',question_embedding,k=self.top_k)

        samples_df = pd.DataFrame.from_dict(samples)
        samples_df['scores'] = scores
        samples_df = samples_df.sort_values(by='scores',ascending=True)
        context = '\n'.join(samples_df['text'].tolist())
        return context


