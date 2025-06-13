# Anime Recommendation System

This Streamlit application provides anime recommendations based on user preferences. It uses an internal structured dataset of anime information and offers two main ways to discover new anime: by finding titles similar to a user's favorite, or by exploring recommendations within specific genres.

## Features

*   **Recommend Similar Anime:**
    *   Users can enter the title of an anime they enjoy.
    *   The system analyzes the input anime's genres and description keywords.
    *   It then suggests a list of other anime from its dataset that have the highest similarity based on shared genres and common keywords.

*   **Explore by Genre (For New Watchers):**
    *   Users looking to start watching anime or explore new categories can select from a predefined list of popular genres (e.g., Rom-Com, Action, Thriller, Sci-Fi, Fantasy, Slice of Life).
    *   The application will display a few sample anime titles belonging to the selected genre, along with their ratings, full genre list, and descriptions. These selections are randomized from the available anime in that genre.

## How It Works

The recommendation logic is based on:

1.  **Content-Based Filtering:** For similar anime recommendations, the system calculates a similarity score between the user's favorite anime and others in the dataset. This score is determined by:
    *   Matching genres (higher weight).
    *   Common keywords extracted from the anime descriptions (lower weight). Stop words are removed, and descriptions are processed to identify significant terms.
2.  **Genre-Based Random Sampling:** For genre exploration, the system filters its dataset for anime matching the chosen genre and then randomly selects a few titles to present.

## Data Source

Currently, this application uses a limited, manually curated dataset (`ANIME_DATA` within `src/main.py`) for demonstration purposes. This dataset includes around 30 diverse anime entries with titles, genres, descriptions, and ratings.

**Future Enhancement:** A planned improvement is to integrate a comprehensive external anime API (e.g., Jikan API for MyAnimeList data) to provide a much wider range of anime and more up-to-date information.

## How to Run

1.  Ensure you have Python and Streamlit installed.
    ```bash
    pip install streamlit
    ```
2.  Navigate to the project's root directory.
3.  Run the Streamlit application using the following command:
    ```bash
    streamlit run src/main.py
    ```
    This will open the application in your default web browser.

## Contributing (Future)

Contributions that enhance the dataset, improve the recommendation algorithms, or integrate external APIs are welcome. Please refer to future contribution guidelines when available.
