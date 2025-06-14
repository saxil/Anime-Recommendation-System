import streamlit as st
import random # Keep for now, might be used by older recommend_by_genre
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Placeholder for ANIME_DATA - In a real scenario on the feat/non-api-tfidf branch,
# this would be the large, locally defined list of anime dictionaries.
# For this operation, we'll define a minimal version to make the script runnable,
# but the actual TF-IDF will operate on the full ANIME_DATA from that branch.
ANIME_DATA = [
    {
        'title': 'Attack on Titan',
        'genre': ['Action', 'Dark Fantasy', 'Post-apocalyptic'],
        'description': 'In a world where humanity resides within enormous walled cities to protect themselves from giant humanoid Titans, Eren Yeager vows to exterminate the Titans after they bring about the destruction of his hometown and the death of his mother. The story follows Eren, his adoptive sister Mikasa Ackerman, and their friend Armin Arlert, as they join the military to fight the Titans and uncover the mysteries of their world.',
        'rating': 9.0
    },
    {
        'title': 'Death Note',
        'genre': ['Thriller', 'Supernatural', 'Mystery'],
        'description': 'A brilliant high school student named Light Yagami discovers a mysterious notebook called the Death Note, which grants its user the ability to kill anyone whose name and face they know. Light decides to use the Death Note to rid the world of criminals, but his actions attract the attention of a brilliant detective known only as L. A deadly game of cat and mouse ensues as Light tries to create his ideal world while evading L.',
        'rating': 8.6
    },
    {
        'title': 'Naruto',
        'genre': ['Action', 'Adventure', 'Fantasy'],
        'description': 'Naruto Uzumaki, a young ninja who seeks recognition from his peers and dreams of becoming the Hokage, the leader of his village. The story is told in two parts – the first set in Naruto\'s pre-teen years, and the second in his teens. Naruto is an orphaned ninja from the Hidden Leaf Village, who is ostracized by the villagers because he is the host of the Nine-Tailed Fox, a powerful creature that attacked the village years ago.',
        'rating': 8.4
    },
    # Add more diverse entries to make TF-IDF meaningful
    {
        'title': 'Kaguya-sama: Love is War',
        'genre': ['Rom-Com', 'Psychological', 'Slice of Life'],
        'description': 'At the prestigious Shuchiin Academy, student council president Miyuki Shirogane and vice-president Kaguya Shinomiya are considered the perfect couple. However, despite having feelings for each other, they are too proud to confess, leading to a series of elaborate schemes and mind games to try and make the other confess first. Their daily interactions become a battle of wits and romance.',
        'rating': 8.5
    },
    {
        'title': 'Steins;Gate',
        'genre': ['Thriller', 'Sci-Fi', 'Psychological', 'Drama'],
        'description': 'Rintaro Okabe, a self-proclaimed "mad scientist," runs a "Future Gadget Laboratory" in Akihabara with his friends. While attempting to create a time machine by modifying a microwave oven, they discover that they can send text messages to the past. Their experiments soon attract the attention of a mysterious organization called SERN.',
        'rating': 9.1
    },
    {
        'title': 'Violet Evergarden',
        'genre': ['Slice of Life', 'Drama', 'Fantasy'],
        'description': 'The Great War has ended, and Violet Evergarden, a young former soldier, takes up a job as an Auto Memory Doll, transcribing people\'s thoughts and feelings into letters. Through her work, Violet embarks on a journey of self-discovery, learning about human emotions and the meaning of love.',
        'rating': 8.6
    }
]

# --- TF-IDF Computation ---
@st.cache_data
def compute_anime_similarity_matrices():
    """
    Computes TF-IDF vectors and cosine similarity matrix for anime descriptions.
    Relies on a globally available ANIME_DATA list of dictionaries.
    """
    print("Computing TF-IDF and Cosine Similarity Matrices...") # For console verification
    if not ANIME_DATA:
        st.error("ANIME_DATA is empty. Cannot compute similarity matrices.")
        # Return empty structures that won't break downstream code expecting these types
        return pd.DataFrame(), None

    anime_df = pd.DataFrame(ANIME_DATA)
    anime_df['description'] = anime_df['description'].fillna('') # Handle missing descriptions

    # Ensure titles are unique for mapping, or handle duplicates if necessary
    # For now, assuming titles are unique enough to serve as identifiers or using index.
    if anime_df['title'].duplicated().any():
        print("Warning: Duplicate titles found in ANIME_DATA. This might affect recommendation by title if titles are used as primary keys.")
        # Consider resetting index to ensure unique IDs if titles are not reliable
        # anime_df = anime_df.reset_index()
        # and then use 'index' for mapping if titles are problematic.

    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2), # Include unigrams and bigrams
        min_df=2,           # Ignore terms that appear in only one document
        max_df=0.85         # Ignore terms that are too frequent (in >85% of docs)
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(anime_df['description'])
        cosine_sim_matrix = cosine_similarity(tfidf_matrix)
        print(f"Cosine similarity matrix shape: {cosine_sim_matrix.shape}")
        # Store titles or original indices for mapping if anime_df is not returned directly
        # For now, returning anime_df is convenient.
        return cosine_sim_matrix, anime_df
    except ValueError as e:
        # This can happen if, after filtering (min_df, max_df), the vocabulary is empty.
        # Especially with very small ANIME_DATA or non-diverse descriptions.
        st.error(f"Failed to compute TF-IDF matrix, possibly due to an empty vocabulary after filtering: {e}")
        print(f"ValueError during TF-IDF: {e}")
        return pd.DataFrame(), None # Return empty structures

# Compute matrices at app start
# These will be globally available for the recommendation functions.
COSINE_SIM_MATRIX, ANIME_DF_PROCESSED = compute_anime_similarity_matrices()


# --- TF-IDF Based Recommendation Function ---
def recommend_similar_anime_tfidf(favorite_anime_title: str, anime_df: pd.DataFrame, similarity_matrix: pd.DataFrame, top_n: int = 5) -> list[str]:
    """
    Recommends anime similar to the favorite_anime_title using the precomputed
    TF-IDF cosine similarity matrix.
    Returns a list of anime titles.
    """
    if anime_df.empty or similarity_matrix is None or similarity_matrix.empty:
        st.error("Similarity data is not available. Cannot provide TF-IDF recommendations.")
        return []

    try:
        # Ensure anime_df index matches the matrix dimensions if titles are not unique,
        # or if anime_df was reset_indexed during compute_anime_similarity_matrices.
        # For now, assume 'title' is unique enough or that anime_df.index aligns with matrix.
        if 'title' not in anime_df.columns:
            st.error("DataFrame does not contain 'title' column.")
            return []

        # Find the index of the favorite anime
        # Using .iloc[0] assumes the title is unique and present.
        # A more robust way might involve checking if the series is empty.
        idx_series = anime_df[anime_df['title'] == favorite_anime_title].index
        if idx_series.empty:
            st.error(f"Anime '{favorite_anime_title}' not found in the processed dataset.")
            return []
        favorite_anime_index = idx_series[0]

    except IndexError:
        st.error(f"Anime '{favorite_anime_title}' not found in the dataset.")
        return []
    except Exception as e:
        st.error(f"An error occurred while finding the anime: {e}")
        return []

    # Get similarity scores for the favorite anime
    try:
        sim_scores_for_favorite = list(enumerate(similarity_matrix[favorite_anime_index]))
    except IndexError:
        st.error(f"Could not retrieve similarity scores for index {favorite_anime_index}. Matrix shape: {similarity_matrix.shape}")
        return []


    # Sort anime based on similarity scores
    # Skip the favorite anime itself (score will be 1.0 with itself)
    sorted_similar_anime_indices = sorted(sim_scores_for_favorite, key=lambda x: x[1], reverse=True)

    # Get titles of the top_n most similar anime
    recommended_anime_titles = []
    for i, score in sorted_similar_anime_indices:
        if i == favorite_anime_index:
            continue # Skip the favorite anime itself
        if len(recommended_anime_titles) < top_n:
            try:
                recommended_anime_titles.append(anime_df['title'].iloc[i])
            except IndexError:
                st.warning(f"Index {i} out of bounds for anime_df titles. Skipping.")
        else:
            break

    return recommended_anime_titles

# --- Legacy Recommendation Logic (Kept for genre recommendations for now) ---
STOP_WORDS_LEGACY = set(['a', 'an', 'the', 'is', 'in', 'of', 'to', 'and']) # Example

def extract_keywords_legacy(description_text):
    if not isinstance(description_text, str): return set()
    words = description_text.lower().split()
    return set(word for word in words if word.isalnum() and word not in STOP_WORDS_LEGACY)

# recommend_similar_anime_legacy is now replaced by recommend_similar_anime_tfidf
# def recommend_similar_anime_legacy(favorite_anime_title, anime_data_list, top_n=5): ...

def recommend_by_genre_legacy(genre_name, anime_data_list, n=3):
    print(f"Legacy genre recommendation for {genre_name}")
    genre_anime = [
        anime for anime in anime_data_list
        if genre_name.lower() in [g.lower() for g in anime['genre']]
    ]
    if not genre_anime: return []
    if len(genre_anime) <= n: return genre_anime
    return random.sample(genre_anime, n)


# --- Streamlit UI (Simplified structure from a potential non-API version) ---
st.set_page_config(layout="wide")
st.title('Anime Recommendation System (TF-IDF Branch)')

# Helper function for displaying an anime item (can be adapted)
def display_anime_card(anime_rec, col, source_note=""):
    with col:
        with st.expander(f"{anime_rec['title']} (Rating: {anime_rec.get('rating', 'N/A')}) {source_note}", expanded=True):
            # Image display would need image URLs in ANIME_DATA or a placeholder
            # st.image(anime_rec.get('image_url', 'https://via.placeholder.com/150'), use_column_width='auto')
            st.caption("Image placeholder")

            genres_str = ", ".join(anime_rec.get('genre', []))
            if genres_str: st.markdown(f"**Genres:** {genres_str}")

            description = anime_rec.get('description', 'N/A')
            if description and description != 'N/A':
                 st.caption(f"**Description:** {description[:150] + '...' if len(description) > 150 else description}")

# Section 1: Recommend based on favorite anime
st.header('Recommend Based on Your Favorite Anime')
# Create a selectbox with anime titles from ANIME_DF_PROCESSED if available
if ANIME_DF_PROCESSED is not None and not ANIME_DF_PROCESSED.empty:
    anime_titles = ANIME_DF_PROCESSED['title'].tolist()
    anime_name_input = st.selectbox('Select your favorite anime:', options=[""] + anime_titles, key='favorite_anime_input')
else:
    anime_name_input = st.text_input('Enter your favorite anime title here (TF-IDF disabled):', key='favorite_anime_input_disabled')


if st.button('Recommend Similar Anime', key='recommend_similar_btn'):
    if COSINE_SIM_MATRIX is None or ANIME_DF_PROCESSED.empty:
        st.error("TF-IDF data not available. Cannot provide recommendations.")
    elif anime_name_input:
        with st.spinner(f"Fetching recommendations similar to '{anime_name_input}' using TF-IDF..."):
            recommendations_titles = recommend_similar_anime_tfidf(
                anime_name_input,
                ANIME_DF_PROCESSED,
                COSINE_SIM_MATRIX,
                top_n=6 # Fetch 6 for 2 rows of 3
            )

        if recommendations_titles:
            st.subheader(f"TF-IDF Recommendations similar to '{anime_name_input}':")
            # Since recommend_similar_anime_tfidf returns titles, we fetch details for display
            recommendations_details = []
            for title in recommendations_titles:
                detail = ANIME_DF_PROCESSED[ANIME_DF_PROCESSED['title'] == title].iloc[0].to_dict()
                recommendations_details.append(detail)

            num_columns = 3
            for i in range(0, len(recommendations_details), num_columns):
                cols = st.columns(num_columns)
                for j, rec_detail in enumerate(recommendations_details[i : i + num_columns]):
                    display_anime_card(rec_detail, cols[j], source_note="(TF-IDF)")
        else:
            # Error messages are now typically handled inside recommend_similar_anime_tfidf
            if not st.session_state.get('tfidf_error_displayed', False): # Check if specific error was already shown
                 st.info(f"No TF-IDF recommendations found for '{anime_name_input}'.")
            st.session_state.tfidf_error_displayed = False # Reset flag
    else:
        st.error("Please select or enter an anime title.")

# Section 2: Recommendations for new watchers by genre (using legacy for now)
st.header('New to Anime? Explore by Genre!')
genres_for_buttons = ["Action", "Comedy", "Drama", "Fantasy", "Romance", "Sci-Fi"]
actual_genres_to_show = genres_for_buttons # Simplified for this non-API version

if actual_genres_to_show:
    button_cols = st.columns(len(actual_genres_to_show))
    for idx, genre_display_name in enumerate(actual_genres_to_show):
        if button_cols[idx].button(genre_display_name, key=f"genre_btn_{genre_display_name.lower()}"):
            st.session_state.selected_genre_legacy = genre_display_name

if 'selected_genre_legacy' in st.session_state and st.session_state.selected_genre_legacy:
    st.subheader(f"Exploring {st.session_state.selected_genre_legacy} Anime (Legacy)")
    with st.spinner(f"Fetching {st.session_state.selected_genre_legacy} anime..."):
        genre_recommendations = recommend_by_genre_legacy(st.session_state.selected_genre_legacy, ANIME_DATA, n=3)

    if genre_recommendations:
        num_columns_genre = 3
        for i in range(0, len(genre_recommendations), num_columns_genre):
            cols_genre = st.columns(num_columns_genre)
            for j, rec in enumerate(genre_recommendations[i : i + num_columns_genre]):
                 display_anime_card(rec, cols_genre[j], source_note="(Legacy/Genre)")
    else:
        st.info(f"No anime found for {st.session_state.selected_genre_legacy} in the local data.")

with st.sidebar:
    st.title('Anime RecSys')
    st.write("TF-IDF Branch")
    if COSINE_SIM_MATRIX is not None and ANIME_DF_PROCESSED is not None:
        st.success(f"TF-IDF Matrix: {COSINE_SIM_MATRIX.shape}")
        st.info(f"Anime DataFrame: {ANIME_DF_PROCESSED.shape[0]} entries")
    else:
        st.error("TF-IDF data failed to load.")
