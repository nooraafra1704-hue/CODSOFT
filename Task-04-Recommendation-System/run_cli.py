import os
import sys
from data_loader import load_data
from recommender import ContentBasedRecommender, CollaborativeRecommender

def main():
    print("=" * 60)
    print("🎬 CINEMATIQUE: RECOMMENDATION ENGINE CLI RUNNER")
    print("=" * 60)
    
    # 1. Load data
    data_dir = "data"
    print(f"[*] Loading data from {data_dir}...")
    movies_df, ratings_df = load_data(data_dir)
    print(f"[+] Loaded {len(movies_df)} movies and {len(ratings_df)} ratings.")
    print("-" * 60)
    
    # 2. Fit models
    print("[*] Initializing and training models...")
    
    cb_recommender = ContentBasedRecommender()
    cb_recommender.fit(movies_df)
    
    cf_recommender = CollaborativeRecommender()
    cf_recommender.fit(movies_df, ratings_df)
    
    print("[+] Models trained successfully!")
    print("=" * 60)
    
    while True:
        print("\nSelect an action:")
        print("1. Get Content-Based recommendations (similar movies)")
        print("2. Get Collaborative Filtering recommendations (personalized for user)")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            print("\nAvailable movies:")
            # Display movies in short grid
            for idx, title in enumerate(movies_df['title']):
                print(f"{idx+1:2d}. {title}")
                
            try:
                m_choice = int(input("\nSelect movie number: ")) - 1
                if 0 <= m_choice < len(movies_df):
                    target_movie = movies_df.iloc[m_choice]['title']
                    print(f"\n[+] Finding movies similar to '{target_movie}'...")
                    recs = cb_recommender.get_recommendations(target_movie, top_n=5)
                    
                    print("\nRecommendations:")
                    print(f"{'Title':<25} | {'Genres':<20} | {'Similarity Score'}")
                    print("-" * 65)
                    for _, row in recs.iterrows():
                        print(f"{row['title']:<25} | {row['genres']:<20} | {row['similarity_score']:.2f}")
                else:
                    print("[-] Invalid selection.")
            except ValueError:
                print("[-] Please enter a valid number.")
                
        elif choice == '2':
            # List some active users
            active_users = sorted(ratings_df['user_id'].unique())[:15]
            print(f"\nSample Active User IDs: {active_users}")
            
            try:
                u_choice = int(input("Enter User ID: "))
                print(f"\n[+] Calculating personalized recommendations for User #{u_choice}...")
                
                # Show past high ratings
                user_ratings = ratings_df[ratings_df['user_id'] == u_choice].sort_values(by='rating', ascending=False)
                if not user_ratings.empty:
                    print("\nUser's Top Rated Movies:")
                    for _, row in user_ratings.head(3).iterrows():
                        title = movies_df[movies_df['movie_id'] == row['movie_id']].iloc[0]['title']
                        print(f" - {title}: {row['rating']} / 5")
                
                recs = cf_recommender.get_recommendations(u_choice, top_n=5)
                
                print("\nRecommended Movies:")
                print(f"{'Title':<25} | {'Genres':<20} | {'Predicted Score'}")
                print("-" * 65)
                for _, row in recs.iterrows():
                    print(f"{row['title']:<25} | {row['genres']:<20} | {row['predicted_score']:.2f} / 5.0")
            except ValueError:
                print("[-] Please enter a valid User ID integer.")
                
        elif choice == '3':
            print("\nThank you for using Cinematique! Goodbye.")
            break
        else:
            print("[-] Invalid choice. Please pick between 1 and 3.")
            
        print("-" * 60)

if __name__ == "__main__":
    main()
