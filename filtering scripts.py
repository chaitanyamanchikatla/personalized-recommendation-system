# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s426b_FK3yYUmuQfrykYOKVjf2ZVhJF_

Collaborative Filtering Script (Using Surprise Library)
"""

!pip install scikit-surprise

import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate

# Step 1: Create Sample Data
data = {
    'user_id': [1, 1, 1, 2, 2, 3, 3, 4],
    'item_id': ['A', 'B', 'C', 'A', 'B', 'C', 'D', 'A'],
    'rating': [5, 4, 3, 5, 4, 3, 5, 4],
}
df = pd.DataFrame(data)

# Step 2: Prepare Data for Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

# Step 3: Train Collaborative Filtering Model
algo = SVD()  # Singular Value Decomposition algorithm
cross_validate(algo, data, cv=3, verbose=True)

# Step 4: Train and Predict
trainset = data.build_full_trainset()
algo.fit(trainset)

# Predict for a specific user-item pair
prediction = algo.predict(uid=2, iid='C')  # User 2, Item 'C'
print("Predicted Rating:", prediction.est)

"""Content-Based Filtering Script"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Create Sample Item Data
data = {
    'item_id': ['A', 'B', 'C', 'D'],
    'metadata': [
        "Action Adventure Fantasy",
        "Comedy Romance",
        "Sci-Fi Mystery",
        "Horror Thriller",
    ],
}
df = pd.DataFrame(data)

# Step 2: Convert Metadata to Feature Vectors
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['metadata'])

# Step 3: Calculate Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 4: Recommend Similar Items
def get_recommendations(item_id, cosine_sim=cosine_sim):
    idx = df[df['item_id'] == item_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]  # Exclude the first (itself)
    item_indices = [i[0] for i in sim_scores]
    return df['item_id'].iloc[item_indices]

# Example: Recommend similar items to 'A'
print("Recommended Items for 'A':", get_recommendations('A'))