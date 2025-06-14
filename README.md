# Anime Recommendation System (Local Data & TF-IDF Version)

This Streamlit application provides anime recommendations based on a **locally stored dataset**. It allows users to discover new anime by finding titles similar to their favorites (using TF-IDF on descriptions) or by exploring anime within specific genres.

## Features

*   **Recommend Similar Anime (TF-IDF Based):**
    *   Users select an anime title they enjoy from the local dataset.
    *   The system utilizes **Term Frequency-Inverse Document Frequency (TF-IDF)** to analyze the textual content of anime descriptions. This method vectorizes descriptions, giving more weight to terms that are significant for a particular anime description in the context of all descriptions. It considers unigrams and bigrams (sequences of one and two words) and filters out common English stop words and terms that are too rare or too frequent across the dataset.
    *   **Cosine Similarity** is then computed on these TF-IDF vectors to find anime with the most similar description content.
    *   The top N most similar anime titles are then recommended to the user.

*   **Explore by Genre:**
    *   Users can select from a predefined list of popular genres.
    *   The application filters the local `ANIME_DATA` to find anime tagged with the selected genre.
    *   A sample of anime from that genre is displayed.

## How It Works

1.  **Data Loading & Preprocessing:**
    *   The application loads anime information from a Python list of dictionaries (`ANIME_DATA`) defined within `src/main.py`.
    *   On startup, it processes this data:
        *   Anime descriptions are vectorized using TF-IDF.
        *   A cosine similarity matrix is pre-computed for all pairs of anime based on their description vectors. This matrix is cached for efficiency.
2.  **Similarity-Based Recommendations:**
    *   When a user selects a favorite anime, its corresponding row in the cosine similarity matrix is used to find other anime with the highest similarity scores.
3.  **Genre-Based Recommendations:**
    *   This feature performs a simple filter on the `ANIME_DATA` based on the genre strings associated with each anime.

## Data Source

This version of the application relies exclusively on a **manually curated, local dataset** (`ANIME_DATA` list within `src/main.py`). It does **not** connect to any external APIs for fetching anime data or recommendations.

## Dependencies & Setup

To run this application, you'll need Python and the following libraries:

*   Streamlit
*   Pandas
*   Scikit-learn

You can install them using pip:
```bash
pip install streamlit pandas scikit-learn
```

## How to Run

1.  Ensure all dependencies listed above are installed.
2.  Navigate to the project's root directory in your terminal.
3.  Execute the Streamlit application using:
    ```bash
    streamlit run src/main.py
    ```
    This will typically open the application in your default web browser.

## Note

This version is specifically designed to demonstrate content-based filtering using TF-IDF on a local dataset. For a version that uses a live external API (Jikan API for MyAnimeList data), please refer to other branches or versions of this project.
