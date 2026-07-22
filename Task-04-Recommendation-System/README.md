# 🎬 Cinematique: Movie Recommendation System

An AI-powered, interactive movie recommendation system implementing both **Content-Based Filtering** and **Collaborative Filtering** models. This project is built as part of the CODSOFT Machine Learning Internship (Task 4).

It includes a self-contained, realistic movie dataset, a standard command-line runner (CLI), and a modern, high-fidelity **Streamlit Web Application** utilizing glassmorphism styling and interactive dashboards.

---

## ✨ Features

- **Dual Recommendation Engine**:
  - **Content-Based Filtering**: Suggests movies similar to a target movie based on metadata (genres and plot descriptions) using **TF-IDF Vectorization** and **Cosine Similarity**.
  - **Collaborative Filtering**: Provides personalized recommendations for individual users using **Item-Based Collaborative Filtering** with Adjusted Cosine Similarity.
- **Modern Interactive Web App**: A beautiful Streamlit dashboard with full data visualization (genre distributions, ratings statistics) and clean UI elements.
- **Interactive CLI**: Command-line fallback interface for testing recommendation outcomes.
- **Self-Contained Data Engine**: Automatically generates a realistic synthetic dataset (movies, user profiles, and rating matrices with realistic interest biases) so it runs instantly without downloading large external files.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Core ML libraries**: `scikit-learn`, `numpy`, `pandas`
- **Frontend Dashboard**: `streamlit`, `altair`

---

## 🚀 How to Run the Project

Follow these steps to run the application on your local machine:

### 1. Clone or Extract the Project
Extract the zip folder or navigate to the directory containing these files:
```bash
cd Task-04-Recommendation-System
```

### 2. Create and Activate a Virtual Environment (Recommended)
This prevents package conflicts with your system python.
- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### 4. Run the Web Application 💻
To launch the modern Streamlit web dashboard:
```bash
streamlit run app.py
```
This will start a local server and open the app in your default web browser (typically at `http://localhost:8501`).

### 5. Run the CLI Runner 🖥️
If you want to run the system directly in your terminal:
```bash
python run_cli.py
```

### 6. Run Unit Verification Tests 🧪
To verify the engine math and outputs:
```bash
python test_recommender.py
```

---

## 🧠 Algorithm Explanations

### 1. Content-Based Filtering
We compute similarities between items using their descriptions and genres:
1. **Feature Merging**: Combine genres (duplicated to weight them higher) and the text description of the movie.
2. **TF-IDF Vectorization**: Extract word significance frequencies:
   $$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \log\left(\frac{N}{\text{DF}(t)}\right)$$
3. **Cosine Similarity**: Measure cosine distance of normalized vectors:
   $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

### 2. Collaborative Filtering (Item-Based)
Instead of comparing users, we compare items rated by the same users:
1. **User-Item Matrix & Center Correction**: Create a ratings matrix and mean-center rating vectors per user to adjust for user bias (optimistic vs. pessimistic raters):
   $$\bar{R}_{u, i} = R_{u, i} - \mu_u$$
2. **Item-Item Cosine Similarity**: Calculate similarity matrix between item columns.
3. **Rating Prediction**: Predict rating $\hat{R}_{u, i}$ for an unrated movie $i$ using a similarity-weighted average of ratings the user has given:
   $$\hat{R}_{u, i} = \frac{\sum_{j \in I_u} S_{i, j} \cdot R_{u, j}}{\sum_{j \in I_u} |S_{i, j}|}$$
   *(where $I_u$ is the set of items rated by user $u$ with positive similarity $S_{i, j} > 0$)*

---

## 📂 Project Structure

```text
Task-04-Recommendation-System/
│
├── data/                       # Directory containing generated CSV datasets
│   ├── movies.csv              # Movies dataset (metadata, genres, overview)
│   └── ratings.csv             # User ratings dataset
│
├── app.py                      # Main Streamlit web application (dashboard)
├── recommender.py              # Recommendation Engine algorithms
├── data_loader.py              # Dataset loading & synthetic data generator
├── run_cli.py                  # Interactive CLI runner
├── test_recommender.py         # Verification test script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```
