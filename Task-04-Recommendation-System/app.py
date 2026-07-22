import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from data_loader import load_data
from recommender import ContentBasedRecommender, CollaborativeRecommender

# Set page configuration
st.set_page_config(
    page_title="Cinematique | AI Recommendation Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for custom premium styling (Glassmorphism & Dark Mode)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background & Title Styling */
    .main {
        background-color: #0d0e15;
        color: #e2e8f0;
    }
    
    h1 {
        background: linear-gradient(135deg, #FF3366, #FF9933);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .subtitle {
        color: #8a99ad;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Card Glassmorphism Styling */
    .movie-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
        transition: all 0.3s ease-in-out;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 51, 102, 0.4);
        box-shadow: 0 10px 25px rgba(255, 51, 102, 0.15);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .movie-title {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }
    
    .movie-genres {
        display: inline-block;
        background: linear-gradient(90deg, rgba(255, 51, 102, 0.15), rgba(255, 153, 51, 0.15));
        color: #ff5e7e;
        font-size: 0.75rem;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(255, 51, 102, 0.2);
    }
    
    .movie-desc {
        color: #a0aec0;
        font-size: 0.9rem;
        line-height: 1.4;
        margin-bottom: 0.75rem;
    }
    
    .metric-badge {
        font-size: 0.85rem;
        font-weight: 600;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        display: inline-flex;
        align-items: center;
    }
    
    .sidebar-title {
        color: #ffffff;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data and fit models
@st.cache_data
def get_cached_data():
    movies_df, ratings_df = load_data("data")
    return movies_df, ratings_df

movies_df, ratings_df = get_cached_data()

# Cache and fit recommender engines
@st.cache_resource
def get_models(movies, ratings):
    cb_model = ContentBasedRecommender()
    cb_model.fit(movies)
    
    cf_model = CollaborativeRecommender()
    cf_model.fit(movies, ratings)
    
    return cb_model, cf_model

cb_model, cf_model = get_models(movies_df, ratings_df)

# Sidebar layout
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Control Center</div>', unsafe_allow_html=True)
    st.write("Configure recommender parameters and settings.")
    
    engine_choice = st.radio(
        "Choose Engine Mode",
        ["Content-Based Filtering", "Collaborative Filtering", "Dataset Explorer"],
        index=0
    )
    
    st.markdown("---")
    top_n = st.slider("Number of Recommendations", min_value=3, max_value=10, value=5)
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    col1, col2 = st.columns(2)
    col1.metric("Movies", len(movies_df))
    col2.metric("Users", len(ratings_df['user_id'].unique()))
    st.metric("Total Ratings", len(ratings_df))

# Header Area
st.markdown("<h1>🎬 Cinematique</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Personalized Movie Recommendation Engine</div>', unsafe_allow_html=True)

# --- 1. DATASET EXPLORER ---
if engine_choice == "Dataset Explorer":
    st.subheader("📊 Dataset Statistics & Visualizations")
    
    tab1, tab2 = st.columns([1, 1])
    
    with tab1:
        st.markdown("### Movie Genres Distribution")
        # Explode genres to count them
        all_genres = movies_df['genres'].str.split('|').explode()
        genre_counts = all_genres.value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        # Altair bar chart
        genre_chart = alt.Chart(genre_counts).mark_bar().encode(
            x=alt.X('Count:Q', title='Number of Movies'),
            y=alt.Y('Genre:N', sort='-x', title='Genre'),
            color=alt.Color('Count:Q', scale=alt.Scale(scheme='magma'))
        ).properties(height=350)
        
        st.altair_chart(genre_chart, use_container_width=True)
        
    with tab2:
        st.markdown("### User Ratings Distribution")
        rating_counts = ratings_df['rating'].value_counts().reset_index()
        rating_counts.columns = ['Rating', 'Count']
        
        rating_chart = alt.Chart(rating_counts).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('Rating:O', title='Rating Value'),
            y=alt.Y('Count:Q', title='Count'),
            color=alt.value('#FF3366')
        ).properties(height=350)
        
        st.altair_chart(rating_chart, use_container_width=True)
        
    st.markdown("### Browse Movie List")
    st.dataframe(
        movies_df[['movie_id', 'title', 'genres', 'overview']], 
        use_container_width=True,
        column_config={
            "movie_id": "ID",
            "title": "Title",
            "genres": "Genres",
            "overview": "Overview Description"
        }
    )

# --- 2. CONTENT-BASED FILTERING ---
elif engine_choice == "Content-Based Filtering":
    st.subheader("🎯 Content-Based Recommendations")
    st.write(
        "Content-based filtering suggests movies similar to a target movie by analyzing genres and overview text using "
        "**TF-IDF Vectorization** and **Cosine Similarity**."
    )
    
    movie_list = sorted(movies_df['title'].tolist())
    selected_movie = st.selectbox("Select a target movie:", movie_list)
    
    # Get metadata of selected movie
    selected_details = movies_df[movies_df['title'] == selected_movie].iloc[0]
    
    st.markdown("#### Selected Movie Profile:")
    st.markdown(f"""
    <div class="movie-card" style="border-left: 5px solid #FF3366;">
        <div class="movie-title">{selected_details['title']}</div>
        <span class="movie-genres">{selected_details['genres'].replace('|', ' • ')}</span>
        <div class="movie-desc">{selected_details['overview']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"#### Top {top_n} Similar Movie Recommendations:")
    
    with st.spinner("Calculating similarity matrix..."):
        recs = cb_model.get_recommendations(selected_movie, top_n)
        
    if recs.empty:
        st.warning("No recommendations found.")
    else:
        # Display recommendations in structured columns or cards
        for idx, row in recs.iterrows():
            sim_pct = int(row['similarity_score'] * 100)
            st.markdown(f"""
            <div class="movie-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div class="movie-title">{row['title']}</div>
                    <span class="metric-badge">🎯 Match Score: {sim_pct}%</span>
                </div>
                <span class="movie-genres">{row['genres'].replace('|', ' • ')}</span>
                <div class="movie-desc">{row['overview']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    with st.expander("🔬 How does this work?"):
        st.markdown(r"""
        ### Content-Based Recommendation Algorithm
        1. **Feature Extraction**: We extract textual metadata for each movie by concatenating its genres (weighted higher) and its description plot.
        2. **TF-IDF Vectorization**: Term Frequency-Inverse Document Frequency (TF-IDF) converts the words in the profile to numerical vectors:
           $$TF\text{-}IDF(t, d, D) = TF(t, d) \times IDF(t, D)$$
        3. **Cosine Similarity**: We calculate the cosine of the angle between two movie vectors $A$ and $B$:
           $$CosineSimilarity(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$
        4. **Sorting**: Movies with the highest cosine score relative to the selected target movie are recommended.
        """)

# --- 3. COLLABORATIVE FILTERING ---
else:
    st.subheader("👥 Collaborative Filtering Recommendations")
    st.write(
        "Collaborative Filtering recommends movies by correlating rating behaviors. We use **Item-Based Collaborative Filtering** "
        "to calculate item-to-item correlation. We predict user ratings for unseen movies using their ratings of similar movies."
    )
    
    user_list = sorted(ratings_df['user_id'].unique().tolist())
    selected_user = st.selectbox("Select a User ID:", user_list)
    
    # Show user preference details
    user_ratings = ratings_df[ratings_df['user_id'] == selected_user].merge(movies_df, on='movie_id')
    top_rated_by_user = user_ratings.sort_values(by='rating', ascending=False).head(3)
    
    col_u1, col_u2 = st.columns([1, 2])
    
    with col_u1:
        st.markdown("#### User Preferences & Ratings:")
        st.write(f"User **#{selected_user}** has rated **{len(user_ratings)}** movies in total.")
        
        # Display top 3 rated movies
        st.write("**Top 3 Rated Movies by User:**")
        for idx, row in top_rated_by_user.iterrows():
            stars = "⭐️" * int(row['rating'])
            st.markdown(f"- **{row['title']}** ({row['genres'].split('|')[0]})\n  `Rating:` {stars} ({row['rating']}/5)")
            
    with col_u2:
        st.markdown(f"#### Personalized Recommendations for User #{selected_user}:")
        
        with st.spinner("Predicting ratings for unrated movies..."):
            recs = cf_model.get_recommendations(selected_user, top_n)
            
        if recs.empty:
            st.warning("No recommendations available.")
        else:
            for idx, row in recs.iterrows():
                pred_rating = round(row['predicted_score'], 1)
                stars = "⭐️" * int(np.round(pred_rating))
                st.markdown(f"""
                <div class="movie-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div class="movie-title">{row['title']}</div>
                        <span class="metric-badge" style="color: #ff9933; background: rgba(255, 153, 51, 0.1); border-color: rgba(255, 153, 51, 0.2);">
                            Predicted: {pred_rating} / 5
                        </span>
                    </div>
                    <span class="movie-genres">{row['genres'].replace('|', ' • ')}</span>
                    <div class="movie-desc">{row['overview']}</div>
                </div>
                """, unsafe_allow_html=True)
                
    with st.expander("🔬 How does this work?"):
        st.markdown(r"""
        ### Item-Based Collaborative Filtering
        1. **User-Item Matrix**: We build a ratings pivot matrix $R$ where cell $(u, i)$ represents the rating of user $u$ for movie $i$.
        2. **Mean Centering**: To adjust for users who rate too generously or strictly, we subtract the user's average rating:
           $$\bar{R}_{u, i} = R_{u, i} - \mu_u$$
           Unrated items are filled with 0 (representing the user's average rating).
        3. **Item Cosine Similarity**: We calculate the similarity $S_{i, j}$ between movie vectors $i$ and $j$ across all users:
           $$S_{i, j} = \frac{\vec{i} \cdot \vec{j}}{\|\vec{i}\| \|\vec{j}\|}$$
        4. **Rating Prediction**: To predict rating $\hat{R}_{u, i}$ for an unrated movie $i$, we take the weighted average of the ratings given by user $u$ on similar movies:
           $$\hat{R}_{u, i} = \frac{\sum_{j \in I_u} S_{i, j} \cdot R_{u, j}}{\sum_{j \in I_u} |S_{i, j}|}$$
           where $I_u$ is the set of items rated by user $u$ that have a positive similarity ($S_{i, j} > 0$) with item $i$.
        """)

# Footer Styling
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #4a5568; font-size: 0.85rem; padding-bottom: 2rem;'>"
    "Cinematique Recommendation System • Created for CODSOFT Task 4"
    "</div>", 
    unsafe_allow_html=True
)
