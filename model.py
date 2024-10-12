import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to recommend internships based on skills and location
def recommend_internships(internships_df, user_skills, user_location):
    # Combine relevant columns into a single feature for recommendation
    internships_df['combined_features'] = internships_df['Skills Required'] + ' ' + internships_df['Location']

    # Use TF-IDF Vectorizer to convert text data into numerical format
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(internships_df['combined_features'])

    # Create a feature string for the user (based on skills and location)
    user_input = user_skills + ' ' + user_location
    user_input_tfidf = tfidf.transform([user_input])

    # Calculate cosine similarity between user input and internships
    cosine_sim = cosine_similarity(user_input_tfidf, tfidf_matrix)

    # Sort internships based on similarity scores
    similarity_scores = cosine_sim[0]
    sorted_indices = similarity_scores.argsort()[::-1]  # Sort in descending order

    # Select top 5 most similar internships
    recommended_internships = internships_df.iloc[sorted_indices[:5]]

    return recommended_internships[['Profile', 'Company', 'Location', 'Stipend', 'About Internship']]
