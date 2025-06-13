import streamlit as st
from src.jikan_client import (
    search_anime_by_title,
    get_anime_recommendations,
    get_anime_details_by_id,
    search_anime_by_genre,
    get_genre_id_map
)

# --- Jikan Integration & Helper Functions ---
@st.cache_data(ttl=3600) # Cache for 1 hour
def fetch_genre_map_from_api():
    """Fetches and caches the genre map from Jikan API."""
    print("Fetching genre map from Jikan API...")
    # No st.error here, return None to handle it in main UI
    return get_genre_id_map()

GENRE_ID_MAP = fetch_genre_map_from_api()
if GENRE_ID_MAP is None: # Check if fetch failed
    GENRE_ID_MAP = {} # Use empty map to prevent errors later, UI will show error message
AVAILABLE_GENRES_FROM_API = sorted(GENRE_ID_MAP.keys())


def format_anime_data_from_jikan(jikan_anime_data):
    if not jikan_anime_data:
        return None
    images = jikan_anime_data.get('images', {})
    jpg_images = images.get('jpg', {}) if isinstance(images, dict) else {}
    image_url = jpg_images.get('large_image_url', jpg_images.get('image_url', None)) if isinstance(jpg_images, dict) else None
    genres_list = [g['name'] for g in jikan_anime_data.get('genres', []) if isinstance(g, dict) and 'name' in g]
    # theme_names, studio_names, producer_names might be pre-populated by get_anime_details_by_id
    # or need to be extracted if the raw Jikan object is passed.
    # For now, format_anime_data_from_jikan will primarily rely on these being top-level keys
    # if they were added by get_anime_details_by_id.
    # If raw search results are passed, these might not be directly available in the same way.
    # This function should consistently return these keys, defaulting to empty lists if not found.

    formatted_data = {
        'mal_id': jikan_anime_data.get('mal_id'),
        'title': jikan_anime_data.get('title', 'N/A'),
        'score': jikan_anime_data.get('score'),
        'synopsis': jikan_anime_data.get('synopsis', 'No synopsis available.'),
        'image_url': image_url,
        'genres_list': genres_list,
        'theme_names': jikan_anime_data.get('theme_names', [t['name'] for t in jikan_anime_data.get('themes', []) if isinstance(t, dict) and 'name' in t]),
        'studio_names': jikan_anime_data.get('studio_names', [s['name'] for s in jikan_anime_data.get('studios', []) if isinstance(s, dict) and 'name' in s]),
        'producer_names': jikan_anime_data.get('producer_names', [p['name'] for p in jikan_anime_data.get('producers', []) if isinstance(p, dict) and 'name' in p])
    }
    return formatted_data

def recommend_similar_anime(favorite_anime_title: str, top_n: int = 5) -> list:
    """
    Hybrid recommendation:
    Phase 1: Fetch direct Jikan recommendations.
    Phase 2: If needed, augment with targeted keyword searches based on favorite's themes/studios.
    Phase 3 (Next subtask): Score, merge, deduplicate, and rank all candidates.
    """
    print(f"Hybrid Phase 1&2 for: {favorite_anime_title}")
    st.session_state.jikan_error_displayed = False # Reset error flag

    # --- Phase 1: Initial Jikan Recommendations & Favorite Anime Details ---
    with st.spinner(f"Searching for '{favorite_anime_title}'..."):
        searched_anime_list = search_anime_by_title(favorite_anime_title)
    if not searched_anime_list:
        st.error(f"Could not find '{favorite_anime_title}' on MyAnimeList. Please check the spelling or try another title.")
        st.session_state.jikan_error_displayed = True
        return []

    favorite_anime_mal_id = searched_anime_list[0].get('mal_id')
    if not favorite_anime_mal_id:
        st.error("Failed to get MAL ID for the searched anime. API data might be incomplete.")
        st.session_state.jikan_error_displayed = True
        return []

    with st.spinner(f"Fetching details for '{searched_anime_list[0].get('title', 'anime')}'..."):
        favorite_anime_details = get_anime_details_by_id(favorite_anime_mal_id)

    if not favorite_anime_details:
        st.error(f"Could not fetch full details for '{searched_anime_list[0].get('title', 'anime')}' from MyAnimeList.")
        st.session_state.jikan_error_displayed = True
        return []

    # Ensure favorite_anime_details is also formatted for consistency, especially for genre_names
    # Note: get_anime_details_by_id already adds theme_names, studio_names, producer_names.
    # format_anime_data_from_jikan will ensure genres_list is also present.
    favorite_anime_formatted_details = format_anime_data_from_jikan(favorite_anime_details)
    if not favorite_anime_formatted_details: # Should not happen if details were fetched
        st.error("Failed to format details for the favorite anime.")
        st.session_state.jikan_error_displayed = True
        return []


    with st.spinner(f"Fetching direct recommendations for '{favorite_anime_formatted_details['title']}'..."):
        direct_jikan_recs_raw = get_anime_recommendations(favorite_anime_mal_id)

    direct_jikan_recs_formatted = []
    if direct_jikan_recs_raw:
        for rec_raw in direct_jikan_recs_raw:
            formatted_rec = format_anime_data_from_jikan(rec_raw)
            if formatted_rec and formatted_rec.get('mal_id') != favorite_anime_mal_id:
                direct_jikan_recs_formatted.append(formatted_rec)

    print(f"Found {len(direct_jikan_recs_formatted)} direct Jikan recommendations.")

    # --- Phase 2: Augmentation via Targeted Search (Conditional & Simplified) ---
    augmented_recs_formatted = []
    if len(direct_jikan_recs_formatted) < top_n:
        print("Direct recommendations less than top_n. Attempting augmentation...")

        fav_genres = favorite_anime_formatted_details.get('genres_list', [])
        fav_themes = favorite_anime_formatted_details.get('theme_names', [])
        fav_studios = favorite_anime_formatted_details.get('studio_names', [])

        # Strategy 1: Top Theme + Top Genre
        if fav_themes and fav_genres:
            query1 = f"{fav_themes[0]} {fav_genres[0]}"
            print(f"Augmentation query 1: {query1}")
            with st.spinner(f"Augmenting with search: '{query1}'..."):
                results_q1_raw = search_anime_by_title(query1)
            if results_q1_raw:
                for res_raw in results_q1_raw:
                    formatted_res = format_anime_data_from_jikan(res_raw)
                    if formatted_res and formatted_res.get('mal_id') != favorite_anime_mal_id:
                        augmented_recs_formatted.append(formatted_res)

        # Strategy 2: Top Studio + Top Genre
        if fav_studios and fav_genres and (len(direct_jikan_recs_formatted) + len(augmented_recs_formatted)) < top_n * 1.5 : # Avoid too many API calls if already close
            query2 = f"{fav_studios[0]} {fav_genres[0]}"
            print(f"Augmentation query 2: {query2}")
            with st.spinner(f"Augmenting with search: '{query2}'..."):
                results_q2_raw = search_anime_by_title(query2)
            if results_q2_raw:
                for res_raw in results_q2_raw:
                    formatted_res = format_anime_data_from_jikan(res_raw)
                    if formatted_res and formatted_res.get('mal_id') != favorite_anime_mal_id:
                        augmented_recs_formatted.append(formatted_res)

        print(f"Found {len(augmented_recs_formatted)} potential augmented recommendations.")

    # --- Phase 3: Combine, Score, and Rank ---

    # Add is_direct_jikan_rec flag and initialize local_score
    for rec in direct_jikan_recs_formatted:
        rec['is_direct_jikan_rec'] = True
        rec['local_score'] = 0
    for rec in augmented_recs_formatted:
        rec['is_direct_jikan_rec'] = False # Came from augmented search
        rec['local_score'] = 0

    # Combine and Deduplicate
    all_candidates = {} # Use dict for deduplication based on mal_id
    for rec in direct_jikan_recs_formatted + augmented_recs_formatted:
        if rec.get('mal_id') and rec.get('mal_id') != favorite_anime_mal_id: # Exclude favorite itself
            # If duplicate, direct Jikan rec takes precedence if it was already there
            # or if the current one is direct and the existing one in all_candidates isn't.
            if rec['mal_id'] not in all_candidates or \
               (rec['is_direct_jikan_rec'] and not all_candidates[rec['mal_id']]['is_direct_jikan_rec']):
                all_candidates[rec['mal_id']] = rec

    unique_candidates = list(all_candidates.values())

    # Calculate local_score for all unique candidates
    fav_genres_set = set(g.lower() for g in favorite_anime_formatted_details.get('genres_list', []))
    fav_themes_set = set(t.lower() for t in favorite_anime_formatted_details.get('theme_names', []))
    fav_studios_set = set(s.lower() for s in favorite_anime_formatted_details.get('studio_names', []))

    for candidate in unique_candidates:
        candidate_genres_set = set(g.lower() for g in candidate.get('genres_list', []))
        candidate_themes_set = set(t.lower() for t in candidate.get('theme_names', []))
        candidate_studios_set = set(s.lower() for s in candidate.get('studio_names', []))

        score = 0
        score += len(fav_genres_set.intersection(candidate_genres_set)) * 2
        score += len(fav_themes_set.intersection(candidate_themes_set)) * 1
        score += len(fav_studios_set.intersection(candidate_studios_set)) * 3
        candidate['local_score'] = score

    # Sort unique candidates: Direct Jikan recs first, then by Jikan score, then by local_score
    unique_candidates.sort(key=lambda x: (
        x.get('is_direct_jikan_rec', False),
        x.get('score') or 0,  # Jikan's original score
        x.get('local_score', 0)
    ), reverse=True) # True for direct recs, higher scores = better

    final_recommendations = unique_candidates[:top_n]

    if not final_recommendations and not st.session_state.jikan_error_displayed:
        st.info(f"No recommendations could be compiled for '{favorite_anime_title}' after filtering and scoring.")
        st.session_state.jikan_error_displayed = True

    # Phase 4: Formatting - is largely handled by format_anime_data_from_jikan
    # and the structure built. Ensure all needed fields are present.
    # The fields 'is_direct_jikan_rec' and 'local_score' can remain for debugging or future UI enhancements.

    return final_recommendations


def recommend_by_genre(genre_name: str, genre_id_map: dict, n: int = 3) -> list:
    genre_id = genre_id_map.get(genre_name.lower())
    if not genre_id:
        st.error(f"Genre ID for '{genre_name}' not found. Cannot fetch recommendations.")
        st.session_state.jikan_error_displayed = True
        return []

    anime_list_from_jikan = search_anime_by_genre(genre_id, limit=n * 2 + 5) # Fetch more to ensure we get N unique ones

    seen_mal_ids = set()
    formatted_recommendations = []
    if anime_list_from_jikan:
        for anime_data in anime_list_from_jikan:
            formatted_rec = format_anime_data_from_jikan(anime_data)
            if formatted_rec and formatted_rec.get('mal_id') not in seen_mal_ids:
                formatted_recommendations.append(formatted_rec)
                seen_mal_ids.add(formatted_rec['mal_id'])
                if len(formatted_recommendations) >= n:
                    break

    if not formatted_recommendations:
        st.info(f"No anime found for genre '{genre_name}' on MyAnimeList currently.")
        st.session_state.jikan_error_displayed = True
        return []

    return formatted_recommendations # Already limited to N by the loop logic

# --- Streamlit UI ---
st.title('Anime Recommendation System')
st.write('Welcome to the Anime Recommendation System! Discover anime based on your favorites or explore genres if you\'re new!')

if 'genre_recommendations' not in st.session_state:
    st.session_state.genre_recommendations = None
if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = None
if 'jikan_error_displayed' not in st.session_state:
    st.session_state.jikan_error_displayed = False


st.header('Recommend Based on Your Favorite Anime')
anime_name_input = st.text_input('Enter your favorite anime title here:', key='favorite_anime_input')

if st.button('Recommend Similar Anime', key='recommend_similar_btn'):
    st.session_state.genre_recommendations = None
    st.session_state.selected_genre = None
    st.session_state.jikan_error_displayed = False

    if anime_name_input:
        with st.spinner(f"Fetching recommendations similar to '{anime_name_input}'..."):
            recommendations = recommend_similar_anime(anime_name_input, top_n=5)

        if recommendations:
            st.subheader(f"Recommendations similar to '{anime_name_input}':")
            for i, rec in enumerate(recommendations):
                with st.expander(f"{i+1}. {rec['title']} (Score: {rec.get('score', 'N/A')})"):
                    if rec.get('image_url') and isinstance(rec.get('image_url'), str) and rec.get('image_url').strip():
                        st.image(rec['image_url'], width=150)
                    else:
                        st.caption("No image available")
                    st.write(f"**Genres:** {', '.join(rec.get('genres_list', ['N/A']))}")
                    if rec.get('theme_names'):
                        st.markdown(f"**Themes:** {', '.join(rec['theme_names'])}")
                    if rec.get('studio_names'):
                        st.markdown(f"**Studios:** {', '.join(rec['studio_names'])}")
                    # Producers can be added similarly if desired:
                    # if rec.get('producer_names'):
                    #    st.markdown(f"**Producers:** {', '.join(rec['producer_names'])}")
                    synopsis = rec.get('synopsis', 'N/A')
                    st.caption(f"**Synopsis:** {synopsis[:250] + '...' if synopsis and len(synopsis) > 250 else synopsis}")
                    if rec.get('mal_id'):
                        st.markdown(f"[View on MyAnimeList](https://myanimelist.net/anime/{rec['mal_id']})")
        elif not st.session_state.jikan_error_displayed:
            st.info(f"No recommendations found for '{anime_name_input}'.")
    else:
        st.error("Please enter an anime title.")

st.header('New to Anime? Explore by Genre!')

if not GENRE_ID_MAP:
    st.error("Failed to load anime genres from the API. Genre recommendations are unavailable.")
else:
    genres_for_buttons = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror",
                          "Mystery", "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural"]
    actual_genres_to_show = [g for g in genres_for_buttons if g.lower() in GENRE_ID_MAP]

    if not actual_genres_to_show:
        st.info("Could not identify common genres from the loaded Jikan genre list to display as buttons.")
    else:
        cols = st.columns(3)
        current_col = 0
        for genre_display_name in actual_genres_to_show:
            button_label = f"Show {genre_display_name}"
            genre_key_name = genre_display_name.replace(" ", "_").replace("-", "_").lower()
            if cols[current_col].button(button_label, key=f"genre_btn_{genre_key_name}"):
                st.session_state.selected_genre = genre_display_name
                st.session_state.jikan_error_displayed = False
                with st.spinner(f"Fetching recommendations for '{genre_display_name}'..."):
                    recommendations = recommend_by_genre(genre_display_name, GENRE_ID_MAP, n=3)

                if recommendations:
                    st.session_state.genre_recommendations = recommendations
                else:
                    st.session_state.genre_recommendations = []
            current_col = (current_col + 1) % 3

        if st.session_state.selected_genre and st.session_state.genre_recommendations is not None:
            st.subheader(f"Top 3 {st.session_state.selected_genre} Anime Recommendations (from Jikan API):")
            if st.session_state.genre_recommendations:
                for i, rec in enumerate(st.session_state.genre_recommendations):
                    with st.expander(f"{i+1}. {rec['title']} (Score: {rec.get('score', 'N/A')})"):
                        if rec.get('image_url') and isinstance(rec.get('image_url'), str) and rec.get('image_url').strip():
                            st.image(rec['image_url'], width=150)
                        else:
                            st.caption("No image available")
                        st.write(f"**Genres:** {', '.join(rec.get('genres_list', ['N/A']))}")
                        synopsis = rec.get('synopsis', 'N/A')
                        st.caption(f"**Synopsis:** {synopsis[:250] + '...' if synopsis and len(synopsis) > 250 else synopsis}")
                        if rec.get('mal_id'):
                             st.markdown(f"[View on MyAnimeList](https://myanimelist.net/anime/{rec['mal_id']})")
            elif not st.session_state.jikan_error_displayed:
                 st.info(f"No recommendations found for {st.session_state.selected_genre} via Jikan API at the moment.")


with st.sidebar:
    st.title('Anime Recommendation System🤖')
    st.write('This is a simple Anime Recommendation System that recommends you some similar anime based on your favorite anime.')
    st.write('Please enter your favorite anime in the text box above and click on the "Recommend" button to get the recommendations.')
    st.write('Enjoy!😊')
