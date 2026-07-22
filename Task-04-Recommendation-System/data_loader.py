import os
import pandas as pd
import numpy as np

def generate_synthetic_data(data_dir):
    """
    Generates a rich, realistic synthetic movie dataset for demonstration purposes.
    Saves 'movies.csv' and 'ratings.csv' in the specified directory.
    """
    os.makedirs(data_dir, exist_ok=True)
    
    movies_path = os.path.join(data_dir, "movies.csv")
    ratings_path = os.path.join(data_dir, "ratings.csv")
    
    # 1. Create Movies Dataset
    movies_data = [
        # Action / Sci-Fi
        {
            "movie_id": 1,
            "title": "The Matrix",
            "genres": "Action|Sci-Fi",
            "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
        },
        {
            "movie_id": 2,
            "title": "Inception",
            "genres": "Action|Sci-Fi|Thriller",
            "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
        },
        {
            "movie_id": 3,
            "title": "Interstellar",
            "genres": "Sci-Fi|Drama|Adventure",
            "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
        },
        {
            "movie_id": 4,
            "title": "Avatar",
            "genres": "Action|Adventure|Sci-Fi",
            "overview": "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home."
        },
        {
            "movie_id": 5,
            "title": "The Dark Knight",
            "genres": "Action|Crime|Drama",
            "overview": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
        },
        {
            "movie_id": 6,
            "title": "Iron Man",
            "genres": "Action|Sci-Fi|Adventure",
            "overview": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil."
        },
        {
            "movie_id": 7,
            "title": "Blade Runner 2049",
            "genres": "Sci-Fi|Thriller|Mystery",
            "overview": "A new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos."
        },
        # Romance / Drama
        {
            "movie_id": 8,
            "title": "The Notebook",
            "genres": "Romance|Drama",
            "overview": "A poor and passionate young man falls in love with a rich young woman, giving her a sense of freedom, but they are soon separated because of their social differences."
        },
        {
            "movie_id": 9,
            "title": "Pride & Prejudice",
            "genres": "Romance|Drama",
            "overview": "Sparks fly when spirited Elizabeth Bennet meets single, rich, and proud Mr. Darcy. But Mr. Darcy reluctantly finds himself falling in love with a woman beneath his class."
        },
        {
            "movie_id": 10,
            "title": "La La Land",
            "genres": "Romance|Drama|Musical",
            "overview": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future."
        },
        {
            "movie_id": 11,
            "title": "Titanic",
            "genres": "Romance|Drama",
            "overview": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
        },
        {
            "movie_id": 12,
            "title": "The Fault in Our Stars",
            "genres": "Romance|Drama",
            "overview": "Two teenage cancer patients begin a life-affirming journey to visit a reclusive author in Amsterdam."
        },
        {
            "movie_id": 13,
            "title": "Before Sunrise",
            "genres": "Romance|Drama",
            "overview": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. However, they both know this will probably be their only night together."
        },
        # Comedy
        {
            "movie_id": 14,
            "title": "The Hangover",
            "genres": "Comedy",
            "overview": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing."
        },
        {
            "movie_id": 15,
            "title": "Superbad",
            "genres": "Comedy",
            "overview": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-filled party goes awry."
        },
        {
            "movie_id": 16,
            "title": "Dumb and Dumber",
            "genres": "Comedy",
            "overview": "After a woman leaves a briefcase at the airport terminal, two extremely stupid friends go on a road trip to Aspen to return it."
        },
        {
            "movie_id": 17,
            "title": "Anchorman: The Legend of Ron Burgundy",
            "genres": "Comedy",
            "overview": "Ron Burgundy is San Diego's top-rated newsman in the male-dominated 1970s broadcast journalism, but that's all about to change for Ron and his cronies when a new female anchor arrives."
        },
        # Thriller / Mystery / Crime
        {
            "movie_id": 18,
            "title": "Se7en",
            "genres": "Crime|Mystery|Thriller",
            "overview": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives."
        },
        {
            "movie_id": 19,
            "title": "Shutter Island",
            "genres": "Mystery|Thriller",
            "overview": "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane."
        },
        {
            "movie_id": 20,
            "title": "Pulp Fiction",
            "genres": "Crime|Drama",
            "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
        }
    ]
    
    movies_df = pd.DataFrame(movies_data)
    movies_df.to_csv(movies_path, index=False)
    print(f"Generated {len(movies_df)} movies in {movies_path}")
    
    # 2. Create Ratings Dataset (100 users, realistic rating patterns)
    np.random.seed(42)
    ratings_list = []
    
    # We define 4 user segments to create clear collaborative filtering patterns
    # Segment 1: Sci-Fi & Action lovers (Users 1-35)
    # Segment 2: Romance & Drama lovers (Users 36-70)
    # Segment 3: Comedy lovers (Users 71-90)
    # Segment 4: Generalists (Users 91-100)
    
    movie_genres = {m["movie_id"]: m["genres"] for m in movies_data}
    
    for user_id in range(1, 101):
        # Decide segment preference
        if 1 <= user_id <= 35:
            pref = "action_scifi"
        elif 36 <= user_id <= 70:
            pref = "romance_drama"
        elif 71 <= user_id <= 90:
            pref = "comedy"
        else:
            pref = "random"
            
        # Every user rates a subset of movies (10 to 15 movies)
        num_ratings = np.random.randint(8, 14)
        selected_movies = np.random.choice(list(movie_genres.keys()), size=num_ratings, replace=False)
        
        for movie_id in selected_movies:
            genres = movie_genres[movie_id]
            
            # Base rating
            rating = 3.0
            
            if pref == "action_scifi":
                if any(g in genres for g in ["Action", "Sci-Fi"]):
                    rating = np.random.choice([4.0, 5.0], p=[0.3, 0.7])
                elif any(g in genres for g in ["Romance", "Drama"]):
                    rating = np.random.choice([1.0, 2.0, 3.0], p=[0.5, 0.4, 0.1])
                else:
                    rating = np.random.choice([2.0, 3.0, 4.0], p=[0.3, 0.5, 0.2])
                    
            elif pref == "romance_drama":
                if any(g in genres for g in ["Romance", "Drama"]) and "Crime" not in genres: # Keep Pulp Fiction moderate
                    rating = np.random.choice([4.0, 5.0], p=[0.3, 0.7])
                elif any(g in genres for g in ["Action", "Sci-Fi"]):
                    rating = np.random.choice([1.0, 2.0, 3.0], p=[0.6, 0.3, 0.1])
                else:
                    rating = np.random.choice([2.0, 3.0, 4.0], p=[0.2, 0.6, 0.2])
                    
            elif pref == "comedy":
                if "Comedy" in genres:
                    rating = np.random.choice([4.0, 5.0], p=[0.2, 0.8])
                else:
                    rating = np.random.choice([2.0, 3.0, 4.0], p=[0.4, 0.4, 0.2])
                    
            else: # Random
                rating = float(np.random.randint(1, 6))
                
            ratings_list.append({
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": rating
            })
            
    ratings_df = pd.DataFrame(ratings_list)
    ratings_df.to_csv(ratings_path, index=False)
    print(f"Generated {len(ratings_df)} ratings for {len(ratings_df['user_id'].unique())} users in {ratings_path}")
    
    return movies_df, ratings_df

def load_data(data_dir="data"):
    """
    Helper function to load dataset. If CSV files do not exist, they are generated.
    """
    movies_path = os.path.join(data_dir, "movies.csv")
    ratings_path = os.path.join(data_dir, "ratings.csv")
    
    if not os.path.exists(movies_path) or not os.path.exists(ratings_path):
        return generate_synthetic_data(data_dir)
        
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    return movies_df, ratings_df

if __name__ == "__main__":
    load_data("data")
