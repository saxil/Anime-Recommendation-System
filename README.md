# Anime Recommendation System

This Streamlit application provides dynamic anime recommendations by leveraging the **Jikan API**, an unofficial MyAnimeList API. It allows users to discover new anime by finding titles similar to their favorites or by exploring recommendations within specific genres, with all data fetched live.

## Features

*   **Recommend Similar Anime:**
    *   Users enter the title of an anime they enjoy.
    *   The system queries the Jikan API to find the MyAnimeList ID of the input anime.
    *   It then fetches direct recommendations for that anime from Jikan, which are often curated by MyAnimeList users.
    *   Results are displayed with details like score, image, genres, a synopsis snippet, and a direct link to the anime's MyAnimeList page.

*   **Explore by Genre (For New Watchers):**
    *   Users can select from a list of popular genres (e.g., Action, Comedy, Fantasy, Sci-Fi, etc.), dynamically sourced from the Jikan API's genre list.
    *   The application then queries the Jikan API for popular anime within the selected genre.
    *   A few sample anime are displayed with their score, image, genres, synopsis, and a link to their MyAnimeList page.

## How It Works

The application's core logic relies on real-time interactions with the Jikan API:

1.  **Fetching Anime Data:** When a user searches for an anime or requests recommendations by genre, the application makes HTTP GET requests to specific Jikan API endpoints.
2.  **Similar Anime Logic:**
    *   The input title is used to search for the anime on MyAnimeList via the Jikan API to retrieve its unique MAL ID.
    *   This MAL ID is then used to fetch user-generated recommendations for that specific anime directly from Jikan.
3.  **Genre Exploration Logic:**
    *   The application first fetches a list of available anime genres and their IDs from Jikan.
    *   When a user selects a genre, the system queries Jikan for top-scoring or popular anime within that genre.
4.  **Data Presentation:** All anime information, including titles, scores, synopses, images, and genre lists, is parsed from the Jikan API responses and formatted for display in the Streamlit UI.

## API Usage: Jikan API

*   **Data Source:** This application uses the **Jikan API (v4)**, available at `https://api.jikan.moe/v4/`. Jikan is an unofficial, free, and open-source REST API for MyAnimeList, providing access to a wide range of anime and manga data.
*   **Dependency:** The functionality and availability of this recommendation system are directly dependent on the Jikan API.
*   **Rate Limiting:** The Jikan API has rate limits to prevent abuse. This application attempts to respect these by including small delays (`time.sleep(0.5)`) between API calls made by the `jikan_client.py` module. Frequent or rapid use might still lead to temporary blocks by the API.
*   **Unofficial Nature:** As Jikan is an unofficial API, its data accuracy and availability are tied to MyAnimeList's own structure and any changes MyAnimeList might make.

## How to Run

1.  **Prerequisites:**
    *   Python 3.7+
    *   Streamlit
    *   Requests (Python HTTP library)
2.  **Installation:**
    *   If you haven't already, install Streamlit and Requests:
        ```bash
        pip install streamlit requests
        ```
3.  **Running the Application:**
    *   Navigate to the project's root directory in your terminal.
    *   Execute the following command:
        ```bash
        streamlit run src/main.py
        ```
    *   Streamlit will typically open the application automatically in your default web browser.

## Contributing (Future)

Contributions that improve the UI/UX, enhance recommendation logic (e.g., advanced filtering, alternative recommendation sources), or add new features are welcome. Please refer to future contribution guidelines when available.
