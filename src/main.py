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
    return {
        'mal_id': jikan_anime_data.get('mal_id'),
        'title': jikan_anime_data.get('title', 'N/A'),
        'score': jikan_anime_data.get('score'),
        'synopsis': jikan_anime_data.get('synopsis', 'No synopsis available.'),
        'image_url': image_url,
        'genres_list': genres_list
    }

def recommend_similar_anime(favorite_anime_title: str, top_n: int = 5) -> list:
    print(f"Starting Jikan recommendation for: {favorite_anime_title}")

    searched_anime_list = search_anime_by_title(favorite_anime_title)
    if not searched_anime_list:
        st.error(f"Could not find '{favorite_anime_title}' on MyAnimeList. Please check the spelling or try another title.")
        st.session_state.jikan_error_displayed = True
        return []

    favorite_anime_summary = searched_anime_list[0]
    favorite_anime_mal_id = favorite_anime_summary.get('mal_id')

    if not favorite_anime_mal_id:
        st.error("Failed to get MAL ID for the selected anime. The API data might be incomplete.")
        st.session_state.jikan_error_displayed = True
        return []

    jikan_recommendations = get_anime_recommendations(favorite_anime_mal_id)
    formatted_recommendations = []

    if jikan_recommendations:
        for rec_entry in jikan_recommendations:
            formatted_rec = format_anime_data_from_jikan(rec_entry)
            if formatted_rec and formatted_rec.get('mal_id') and formatted_rec['mal_id'] != favorite_anime_mal_id:
                formatted_recommendations.append(formatted_rec)
        if not formatted_recommendations and len(jikan_recommendations) > 0 : # Had recommendations, but all were self or unformattable
             st.info(f"Found '{favorite_anime_title}' on MyAnimeList, but it has no other distinct anime recommendations listed there at the moment.")
             st.session_state.jikan_error_displayed = True

    # This part handles when jikan_recommendations itself is empty or None
    if not jikan_recommendations:
        source_anime_details = get_anime_details_by_id(favorite_anime_mal_id)
        if source_anime_details:
             st.info(f"Found '{favorite_anime_title}' on MyAnimeList, but it doesn't have direct recommendations there. You could try exploring by genre instead!")
             st.session_state.jikan_error_displayed = True
        else:
            st.error(f"Could not fetch details for '{favorite_anime_title}' after finding it. API might be unstable.")
            st.session_state.jikan_error_displayed = True

    formatted_recommendations.sort(key=lambda x: x.get('score') or 0, reverse=True)
    return formatted_recommendations[:top_n]

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
