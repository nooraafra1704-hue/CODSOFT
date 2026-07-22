import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self):
        self.movies_df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def fit(self, movies_df):
        """
        Fits the Content-Based Recommender by vectorizing movie metadata
        (genres and overview) and computing similarity.
        """
        self.movies_df = movies_df.copy()
        
        # Prepare content string: combine genres (spaces instead of pipes) and overview
        # We give more weight to genres by repeating them
        processed_genres = self.movies_df['genres'].apply(lambda x: " ".join(x.split('|')) * 2)
        self.movies_df['content_features'] = processed_genres + " " + self.movies_df['overview']
        
        # Fit-transform with TF-IDF
        self.tfidf_matrix = self.vectorizer.fit_transform(self.movies_df['content_features'])
        
        # Calculate Cosine Similarity Matrix
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_recommendations(self, movie_title, top_n=5):
        """
        Returns top_n similar movies for a given movie title.
        """
        if self.movies_df is None:
            raise ValueError("Recommender model has not been fitted yet.")
            
        # Case-insensitive title match
        match = self.movies_df[self.movies_df['title'].str.lower() == movie_title.lower()]
        if match.empty:
            # Fallback to partial match
            match = self.movies_df[self.movies_df['title'].str.lower().str.contains(movie_title.lower())]
            if match.empty:
                return pd.DataFrame(columns=['title', 'genres', 'similarity_score'])
        
        movie_idx = match.index[0]
        
        # Get pairwise similarity scores of all movies with this movie
        sim_scores = list(enumerate(self.cosine_sim[movie_idx]))
        
        # Sort movies based on similarity scores in descending order
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get scores of the top_n similar movies (skip the first one since it's the movie itself)
        top_sim_scores = [score for score in sim_scores if score[0] != movie_idx][:top_n]
        
        # Get movie indices and similarity values
        movie_indices = [i[0] for i in top_sim_scores]
        similarity_values = [i[1] for i in top_sim_scores]
        
        recommendations = self.movies_df.iloc[movie_indices][['movie_id', 'title', 'genres', 'overview']].copy()
        recommendations['similarity_score'] = similarity_values
        
        return recommendations


class CollaborativeRecommender:
    def __init__(self):
        self.movies_df = None
        self.ratings_df = None
        self.user_item_matrix = None
        self.item_sim_df = None

    def fit(self, movies_df, ratings_df):
        """
        Fits the Item-Based Collaborative Filtering model.
        """
        self.movies_df = movies_df.copy()
        self.ratings_df = ratings_df.copy()
        
        # Create User-Item matrix (users as rows, movies as columns)
        self.user_item_matrix = self.ratings_df.pivot(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        )
        
        # Fill missing values with user average to avoid bias
        # For simplicity, we mean-center each user's ratings, fill NaNs with 0 (which represents user's average)
        # This is standard Adjusted Cosine Similarity / Pearson Correlation equivalent
        user_means = self.user_item_matrix.mean(axis=1)
        matrix_centered = self.user_item_matrix.sub(user_means, axis=0).fillna(0)
        
        # Compute cosine similarity between items (columns of centered matrix)
        item_sim = cosine_similarity(matrix_centered.T)
        
        # Convert to DataFrame for easier lookups
        self.item_sim_df = pd.DataFrame(
            item_sim, 
            index=self.user_item_matrix.columns, 
            columns=self.user_item_matrix.columns
        )

    def get_recommendations(self, user_id, top_n=5):
        """
        Returns personalized movie recommendations for a given user_id
        using Item-Based Collaborative Filtering.
        """
        if self.user_item_matrix is None:
            raise ValueError("Recommender model has not been fitted yet.")
            
        if user_id not in self.user_item_matrix.index:
            # Cold-start: return top rated movies overall
            avg_ratings = self.ratings_df.groupby('movie_id').agg(
                avg_rating=('rating', 'mean'),
                rating_count=('rating', 'count')
            )
            # Filter movies with at least 3 ratings to avoid outliers
            popular_movies = avg_ratings[avg_ratings['rating_count'] >= 3].sort_values(
                by='avg_rating', 
                ascending=False
            ).head(top_n)
            
            recs = self.movies_df[self.movies_df['movie_id'].isin(popular_movies.index)].copy()
            recs = recs.merge(popular_movies, on='movie_id')
            recs.rename(columns={'avg_rating': 'predicted_score'}, inplace=True)
            return recs.sort_values(by='predicted_score', ascending=False)
            
        # Get active user's ratings
        user_ratings = self.user_item_matrix.loc[user_id]
        
        # Get movies user has NOT rated yet
        unrated_movies = user_ratings[user_ratings.isna()].index
        
        # Get movies user HAS rated
        rated_movies = user_ratings[user_ratings.notna()].index
        
        predicted_ratings = {}
        
        # Predict rating for each unrated movie
        for movie_id in unrated_movies:
            # Get similarity of this unrated movie with all rated movies
            similarities = self.item_sim_df.loc[movie_id, rated_movies]
            
            # Get user's ratings for those rated movies
            user_ratings_subset = user_ratings[rated_movies]
            
            # Weighted average: sum(similarity * rating) / sum(similarity)
            # We filter out negative similarities to avoid predicting high scores from disliked items
            pos_sim_mask = similarities > 0
            pos_sim = similarities[pos_sim_mask]
            pos_ratings = user_ratings_subset[pos_sim_mask]
            
            if pos_sim.sum() > 0:
                predicted_val = np.dot(pos_sim, pos_ratings) / pos_sim.sum()
                predicted_ratings[movie_id] = predicted_val
            else:
                # Default fallback: user's average rating
                predicted_ratings[movie_id] = user_ratings.mean()
                
        # Sort and get top_n
        sorted_predictions = sorted(predicted_ratings.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        movie_ids = [item[0] for item in sorted_predictions]
        scores = [item[1] for item in sorted_predictions]
        
        recommendations = self.movies_df[self.movies_df['movie_id'].isin(movie_ids)].copy()
        # Ensure ordered as sorted_predictions
        recommendations['predicted_score'] = recommendations['movie_id'].map(dict(sorted_predictions))
        recommendations = recommendations.sort_values(by='predicted_score', ascending=False)
        
        return recommendations
