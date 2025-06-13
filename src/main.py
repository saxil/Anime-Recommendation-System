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
    return get_genre_id_map()

GENRE_ID_MAP = fetch_genre_map_from_api()
if GENRE_ID_MAP is None:
    GENRE_ID_MAP = {}
AVAILABLE_GENRES_FROM_API = sorted(GENRE_ID_MAP.keys())


def format_anime_data_from_jikan(jikan_anime_data):
    if not jikan_anime_data:
        return None
    images = jikan_anime_data.get('images', {})
    jpg_images = images.get('jpg', {}) if isinstance(images, dict) else {}
    image_url = jpg_images.get('large_image_url', jpg_images.get('image_url', None)) if isinstance(jpg_images, dict) else None
    genres_list = [g['name'] for g in jikan_anime_data.get('genres', []) if isinstance(g, dict) and 'name' in g]

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
    print(f"Hybrid Phase 1&2 for: {favorite_anime_title}")
    st.session_state.jikan_error_displayed = False

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

    favorite_anime_formatted_details = format_anime_data_from_jikan(favorite_anime_details)
    if not favorite_anime_formatted_details:
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

    augmented_recs_formatted = []
    if len(direct_jikan_recs_formatted) < top_n:
        fav_genres = favorite_anime_formatted_details.get('genres_list', [])
        fav_themes = favorite_anime_formatted_details.get('theme_names', [])
        fav_studios = favorite_anime_formatted_details.get('studio_names', [])

        if fav_themes and fav_genres:
            query1 = f"{fav_themes[0]} {fav_genres[0]}"
            with st.spinner(f"Augmenting with search: '{query1}'..."):
                results_q1_raw = search_anime_by_title(query1)
            if results_q1_raw:
                for res_raw in results_q1_raw:
                    formatted_res = format_anime_data_from_jikan(res_raw)
                    if formatted_res and formatted_res.get('mal_id') != favorite_anime_mal_id:
                        augmented_recs_formatted.append(formatted_res)

        if fav_studios and fav_genres and (len(direct_jikan_recs_formatted) + len(augmented_recs_formatted)) < top_n * 1.5 :
            query2 = f"{fav_studios[0]} {fav_genres[0]}"
            with st.spinner(f"Augmenting with search: '{query2}'..."):
                results_q2_raw = search_anime_by_title(query2)
            if results_q2_raw:
                for res_raw in results_q2_raw:
                    formatted_res = format_anime_data_from_jikan(res_raw)
                    if formatted_res and formatted_res.get('mal_id') != favorite_anime_mal_id:
                        augmented_recs_formatted.append(formatted_res)

    for rec in direct_jikan_recs_formatted:
        rec['is_direct_jikan_rec'] = True
        rec['local_score'] = 0
    for rec in augmented_recs_formatted:
        rec['is_direct_jikan_rec'] = False
        rec['local_score'] = 0

    all_candidates = {}
    for rec in direct_jikan_recs_formatted + augmented_recs_formatted:
        if rec.get('mal_id') and rec.get('mal_id') != favorite_anime_mal_id:
            if rec['mal_id'] not in all_candidates or \
               (rec['is_direct_jikan_rec'] and not all_candidates[rec['mal_id']]['is_direct_jikan_rec']):
                all_candidates[rec['mal_id']] = rec

    unique_candidates = list(all_candidates.values())
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

    unique_candidates.sort(key=lambda x: (
        x.get('is_direct_jikan_rec', False),
        x.get('score') or 0,
        x.get('local_score', 0)
    ), reverse=True)

    final_recommendations = unique_candidates[:top_n]

    if not final_recommendations and not st.session_state.jikan_error_displayed:
        st.info(f"No recommendations could be compiled for '{favorite_anime_title}' after filtering and scoring.")
        st.session_state.jikan_error_displayed = True
    return final_recommendations

# --- Streamlit UI ---
st.set_page_config(layout="wide") # Use wide layout for better grid display
st.title('Anime Recommendation System')
st.write('Welcome to the Anime Recommendation System! Discover anime based on your favorites or explore genres if you\'re new!')

# Initialize session state variables
if 'genre_recommendations' not in st.session_state:
    st.session_state.genre_recommendations = None
if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = None
if 'jikan_error_displayed' not in st.session_state:
    st.session_state.jikan_error_displayed = False
if 'genre_page' not in st.session_state:
    st.session_state.genre_page = 1
if 'genre_last_page' not in st.session_state:
    st.session_state.genre_last_page = 1
if 'genre_has_next_page' not in st.session_state:
    st.session_state.genre_has_next_page = False

# --- Helper function for displaying an anime item in a column ---
def display_anime_card(anime_rec, col):
    with col:
        with st.expander(f"{anime_rec['title']} (Score: {anime_rec.get('score', 'N/A')})", expanded=True):
            if anime_rec.get('image_url') and isinstance(anime_rec.get('image_url'), str) and anime_rec.get('image_url').strip():
                st.image(anime_rec['image_url'], use_column_width='auto')
            else:
                st.caption("No image available")

            genres_str = ", ".join(anime_rec.get('genres_list', []))
            if genres_str: st.markdown(f"**Genres:** {genres_str}")

            themes_str = ", ".join(anime_rec.get('theme_names', []))
            if themes_str: st.markdown(f"**Themes:** {themes_str}")

            studios_str = ", ".join(anime_rec.get('studio_names', []))
            if studios_str: st.markdown(f"**Studios:** {studios_str}")

            synopsis = anime_rec.get('synopsis', 'N/A')
            if synopsis and synopsis != 'No synopsis available.':
                 st.caption(f"**Synopsis:** {synopsis[:150] + '...' if len(synopsis) > 150 else synopsis}")

            if anime_rec.get('mal_id'):
                st.markdown(f"[View on MyAnimeList](https://myanimelist.net/anime/{anime_rec['mal_id']})", unsafe_allow_html=True)


st.header('Recommend Based on Your Favorite Anime')
anime_name_input = st.text_input('Enter your favorite anime title here:', key='favorite_anime_input')

if st.button('Recommend Similar Anime', key='recommend_similar_btn'):
    st.session_state.genre_recommendations = None
    st.session_state.selected_genre = None
    st.session_state.jikan_error_displayed = False

    if anime_name_input:
        with st.spinner(f"Fetching recommendations similar to '{anime_name_input}'..."):
            recommendations = recommend_similar_anime(anime_name_input, top_n=6) # Fetch 6 for 2 rows of 3

        if recommendations:
            st.subheader(f"Recommendations similar to '{anime_name_input}':")
            num_columns = 3
            for i in range(0, len(recommendations), num_columns):
                cols = st.columns(num_columns)
                for j, rec in enumerate(recommendations[i : i + num_columns]):
                    display_anime_card(rec, cols[j])
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
        # --- Genre Button Selection ---
        button_cols = st.columns(6) # More columns for genre buttons
        col_idx = 0
        for genre_display_name in actual_genres_to_show:
            button_label = f"{genre_display_name}" # Shorter labels
            genre_key_name = genre_display_name.replace(" ", "_").replace("-", "_").lower()
            if button_cols[col_idx % 6].button(button_label, key=f"genre_btn_{genre_key_name}"):
                if st.session_state.selected_genre != genre_display_name:
                    st.session_state.selected_genre = genre_display_name
                    st.session_state.genre_page = 1
                    st.session_state.genre_recommendations = None
                st.session_state.jikan_error_displayed = False
                st.experimental_rerun()
            col_idx +=1

    # --- Data Fetching and Display for Selected Genre ---
    if st.session_state.selected_genre:
        st.subheader(f"Exploring {st.session_state.selected_genre} Anime (Page {st.session_state.genre_page})")
        genre_id = GENRE_ID_MAP.get(st.session_state.selected_genre.lower())

        if not genre_id:
            st.error(f"Cannot find ID for genre '{st.session_state.selected_genre}'.")
            st.session_state.jikan_error_displayed = True
        else:
            items_per_page = 9
            with st.spinner(f"Fetching {st.session_state.selected_genre} anime (Page {st.session_state.genre_page})..."):
                anime_list_raw, pagination_info = search_anime_by_genre(
                    genre_id,
                    page=st.session_state.genre_page,
                    limit=items_per_page
                )

            if pagination_info:
                st.session_state.genre_last_page = pagination_info.get('last_visible_page', st.session_state.genre_page)
                st.session_state.genre_has_next_page = pagination_info.get('has_next_page', False)
            else:
                st.session_state.genre_last_page = st.session_state.genre_page
                st.session_state.genre_has_next_page = False

            formatted_recommendations = []
            if anime_list_raw:
                for anime_data in anime_list_raw:
                    formatted = format_anime_data_from_jikan(anime_data)
                    if formatted:
                        formatted_recommendations.append(formatted)
            st.session_state.genre_recommendations = formatted_recommendations

            if not st.session_state.genre_recommendations and not st.session_state.jikan_error_displayed:
                st.info(f"No anime found for {st.session_state.selected_genre} on this page.")

    # --- Display Fetched Genre Recommendations in a Grid ---
    if st.session_state.selected_genre and st.session_state.genre_recommendations:
        num_columns_genre = 3
        for i in range(0, len(st.session_state.genre_recommendations), num_columns_genre):
            cols_genre = st.columns(num_columns_genre)
            for j, rec in enumerate(st.session_state.genre_recommendations[i : i + num_columns_genre]):
                 display_anime_card(rec, cols_genre[j])

    # --- Pagination Controls ---
    if st.session_state.selected_genre:
        pg_col1, pg_col2, pg_col3 = st.columns([2, 3, 2]) # Adjusted column ratios
        with pg_col1:
            if st.button("⬅️ Previous Page", disabled=(st.session_state.genre_page <= 1), use_container_width=True):
                st.session_state.genre_page -= 1
                st.experimental_rerun()
        with pg_col2:
            if st.session_state.genre_last_page > 0 :
                 st.markdown(f"<p style='text-align: center; font-weight: bold;'>Page {st.session_state.genre_page} of {st.session_state.genre_last_page}</p>", unsafe_allow_html=True)
            else:
                 st.markdown(f"<p style='text-align: center; font-weight: bold;'>Page {st.session_state.genre_page}</p>", unsafe_allow_html=True)

        with pg_col3:
            if st.button("Next Page ➡️", disabled=(not st.session_state.genre_has_next_page or st.session_state.genre_page >= st.session_state.genre_last_page), use_container_width=True):
                st.session_state.genre_page += 1
                st.experimental_rerun()

with st.sidebar:
    st.title('Anime Recommendation System🤖')
    st.write('This is a simple Anime Recommendation System that recommends you some similar anime based on your favorite anime.')
    st.write('Please enter your favorite anime in the text box above and click on the "Recommend" button to get the recommendations.')
    st.write('Enjoy!😊')
