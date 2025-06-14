# Anime Recommendation System

This Streamlit application provides dynamic anime recommendations by leveraging the **Jikan API**, an unofficial MyAnimeList API. It allows users to discover new anime by finding titles similar to their favorites or by exploring recommendations within specific genres, with all data fetched live.

## Features

*   **Dynamic Anime Recommendations:** Suggests anime similar to a user's favorite using a sophisticated hybrid approach. This combines direct recommendations from the Jikan API with results from targeted keyword searches, which are then scored and ranked based on relevance.
*   **Genre-Based Exploration with Pagination:** Allows users to explore a wide range of anime by selecting a genre. Results are fetched live from the Jikan API and presented with intuitive pagination controls to navigate through multiple pages.
*   **Detailed Information Display:** Shows rich details for each recommended anime, including its official MyAnimeList score, cover image, a concise synopsis, and lists of associated genres, themes, and studios. A direct link to the anime's MyAnimeList page is also provided.
*   **Responsive Grid Layout:** Presents recommendations in a user-friendly 3-column grid that dynamically adapts to different screen widths, enhancing the browsing experience.
*   **User-Friendly Interface:** Built with Streamlit, the application features clear loading indicators during API calls and informative error messages to guide the user.
*   **Efficient Data Handling:** Caches essential data like the genre map fetched from the Jikan API to improve performance and minimize redundant API requests.

## How It Works

The application is a web app built with Streamlit, designed to provide relevant anime recommendations by dynamically interacting with the Jikan API (v4).

### API Interaction Module (`src/jikan_client.py`)
A dedicated client module, `src/jikan_client.py`, manages all communications with the Jikan API. Its primary functions include:
*   Constructing API request URLs for various Jikan v4 endpoints (e.g., `/anime` for search, `/anime/{id}/full` for details, `/anime/{id}/recommendations`, `/genres/anime`).
*   Executing HTTP GET requests.
*   Parsing JSON responses returned by the API.
*   Implementing basic error handling for API calls, such as network issues or non-200 status codes.
*   Incorporating a mandatory delay (`time.sleep(0.5)`) between API calls to comply with Jikan's rate limiting policies.
*   Extracting and returning both the core data (e.g., list of anime) and pagination details from API responses where applicable.

### Core Feature: Similar Anime Recommendations (Hybrid Approach)
When a user enters their favorite anime title to find similar ones:
1.  **Initial Search & Detail Fetch:** The system first queries the Jikan API via `search_anime_by_title` to identify the specific MyAnimeList ID (MAL ID) for the entered title. It then uses `get_anime_details_by_id` to retrieve the full details of this favorite anime, including its genres, themes, and studios.
2.  **Direct Jikan Recommendations:** Using the MAL ID, the app calls `get_anime_recommendations` to fetch a list of anime directly recommended by MyAnimeList users (via the Jikan API).
3.  **Augmentation Strategy (Conditional):** If the number of direct Jikan recommendations is below a predefined threshold (e.g., 5), the system attempts to augment these results. It forms new search queries based on combinations of the favorite anime's primary attributes (e.g., "Top Theme + Top Genre" or "Top Studio + Top Genre") and uses `search_anime_by_title` (which also functions as a keyword search) to find additional candidates.
4.  **Consolidation, Scoring & Ranking:**
    *   All potential recommendations (direct and augmented) are combined.
    *   Duplicate entries are removed based on their MAL ID, with a preference given to anime that appeared in the direct Jikan recommendations list.
    *   Each unique candidate is assigned a `local_score` based on its similarity to the user's favorite anime. This score is calculated by comparing shared genres (higher weight), themes (medium weight), and studios (higher weight).
    *   The consolidated list is then sorted using a multi-level key:
        1.  Primary sort: Direct Jikan recommendations first.
        2.  Secondary sort: The anime's original score on MyAnimeList (descending).
        3.  Tertiary sort: The calculated `local_score` (descending).
5.  **Display:** The top N (typically 5 or 6) highest-ranked anime are presented to the user in a responsive grid layout, each with detailed information.

### Core Feature: Explore by Genre (with Pagination)
When a user opts to explore anime by genre:
1.  **Genre Selection:** The user selects a genre from a list of common anime genres (the underlying genre-to-ID mapping is fetched from Jikan and cached).
2.  **Paginated API Fetch:** The application calls `search_anime_by_genre` in the `jikan_client`, requesting a specific page of anime for the selected genre ID (e.g., 9 items per page). The Jikan API typically returns these results sorted by score or popularity.
3.  **Display & Navigation:** The fetched anime are displayed in a 3-column grid. "⬅️ Previous Page" and "Next Page ➡️" buttons allow the user to navigate through the paginated results. The current page number and total available pages (if provided by the API) are also shown.
4.  **State Management:** Streamlit's `st.session_state` is utilized to maintain the current page number and the selected genre, ensuring a consistent user experience during navigation.

### Data Formatting and Presentation
A utility function, `format_anime_data_from_jikan` (located in `src/main.py`), plays a crucial role in standardizing the raw data obtained from various Jikan API endpoints. It ensures that all anime information (title, MAL ID, score, image URL, synopsis, and lists of genres, themes, and studios) is processed into a consistent dictionary format, ready for clean and uniform display in the Streamlit UI.

### Caching Strategy
To enhance performance and minimize API load, the application caches the genre-to-ID mapping fetched from Jikan's `/genres/anime` endpoint. This is achieved using Streamlit's `@st.cache_data` decorator, meaning this information is typically fetched only once when the app starts or if the cache expires (e.g., after 1 hour).

## API Usage: Jikan API

*   **Data Source:** This application relies on the **Jikan API (v4)**, accessible at `https://api.jikan.moe/v4/`. Jikan serves as an unofficial REST API for MyAnimeList, offering extensive anime and manga data.
*   **Dependency:** The application's functionality is entirely dependent on the Jikan API's availability and performance.
*   **Rate Limiting:** The Jikan API enforces rate limits. The application includes a built-in delay (`time.sleep(0.5)`) in its API client (`src/jikan_client.py`) for each request to help mitigate issues. However, very rapid or extensive use might still encounter API rate limits.
*   **Unofficial Status:** Users should be aware that Jikan is an unofficial API. Changes to MyAnimeList's website or structure could potentially affect Jikan's data availability or accuracy.

## How to Run

1.  **Prerequisites:**
    *   Python 3.7+
    *   Key Python libraries: Streamlit, Requests (for API calls), Pandas (for data handling).

2.  **Installation:**
    *   Clone this repository to your local machine.
    *   Navigate to the project's root directory in your terminal.
    *   Install all necessary dependencies using the `requirements.txt` file:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Running the Application:**
    *   Ensure you are in the project's root directory.
    *   Execute the following command in your terminal:
        ```bash
        streamlit run src/main.py
        ```
    *   Streamlit will start the application and typically open it automatically in your default web browser.

## Contributing (Future)

Contributions that improve the UI/UX, enhance recommendation logic (e.g., advanced filtering, alternative recommendation sources), or add new features are welcome. Please refer to future contribution guidelines when available.
