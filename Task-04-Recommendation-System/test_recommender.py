import os
from data_loader import load_data
from recommender import ContentBasedRecommender, CollaborativeRecommender

def run_tests():
    print("[*] Running Recommendation System Tests...")
    
    # 1. Test data loader
    print("[*] Testing Data Loader...")
    movies_df, ratings_df = load_data("data")
    assert not movies_df.empty, "Movies DataFrame should not be empty"
    assert not ratings_df.empty, "Ratings DataFrame should not be empty"
    print("[+] Data Loader passed.")

    # 2. Test Content-Based Recommender
    print("[*] Testing Content-Based Recommender...")
    cb = ContentBasedRecommender()
    cb.fit(movies_df)
    
    movie_title = "Inception"
    recs_cb = cb.get_recommendations(movie_title, top_n=3)
    assert len(recs_cb) == 3, f"Expected 3 recommendations, got {len(recs_cb)}"
    assert 'similarity_score' in recs_cb.columns, "Output should contain similarity_score"
    print(f"[+] Content-Based passed. Recommendations for '{movie_title}':")
    for idx, row in recs_cb.iterrows():
        print(f"    - {row['title']} (Score: {row['similarity_score']:.4f})")

    # 3. Test Collaborative Recommender
    print("[*] Testing Collaborative Recommender...")
    cf = CollaborativeRecommender()
    cf.fit(movies_df, ratings_df)
    
    user_id = 5
    recs_cf = cf.get_recommendations(user_id, top_n=3)
    assert len(recs_cf) == 3, f"Expected 3 recommendations, got {len(recs_cf)}"
    assert 'predicted_score' in recs_cf.columns, "Output should contain predicted_score"
    print(f"[+] Collaborative Filtering passed. Recommendations for User {user_id}:")
    for idx, row in recs_cf.iterrows():
        print(f"    - {row['title']} (Predicted Rating: {row['predicted_score']:.2f}/5)")

    print("\n[+] All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
