import requests
import time

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"

def search_anime_by_title(title: str) -> list:
    """Searches for anime by title using the Jikan API."""
    url = f"{JIKAN_API_BASE_URL}/anime?q={title}&limit=5&sfw=true"
    try:
        response = requests.get(url)
        time.sleep(0.5) # Respect basic rate limits
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"Error searching anime by title '{title}': Status code {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error searching anime by title '{title}': {e}")
        return []

def get_anime_details_by_id(mal_id: int) -> dict | None:
    """Fetches detailed information for a specific anime by its MyAnimeList ID."""
    url = f"{JIKAN_API_BASE_URL}/anime/{mal_id}/full"
    try:
        response = requests.get(url)
        time.sleep(0.5) # Respect basic rate limits
        if response.status_code == 200:
            return response.json().get('data', None)
        else:
            print(f"Error fetching anime details for ID {mal_id}: Status code {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching anime details for ID {mal_id}: {e}")
        return None

def search_anime_by_genre(genre_id: int, page: int = 1, limit: int = 10) -> list:
    """Searches for anime by genre ID using the Jikan API.
    Orders by score descending and filters for SFW (Safe For Work) content.
    """
    url = f"{JIKAN_API_BASE_URL}/anime?genres={genre_id}&page={page}&limit={limit}&sfw=true&order_by=score&sort=desc"
    try:
        response = requests.get(url)
        time.sleep(0.5) # Respect basic rate limits
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"Error searching anime by genre ID {genre_id}: Status code {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error searching anime by genre ID {genre_id}: {e}")
        return []

def get_anime_recommendations(mal_id: int) -> list:
    """Fetches anime recommendations for a given anime ID from the Jikan API."""
    url = f"{JIKAN_API_BASE_URL}/anime/{mal_id}/recommendations"
    try:
        response = requests.get(url)
        time.sleep(0.5) # Respect basic rate limits
        if response.status_code == 200:
            # The recommendations are a list of entries, each containing an 'entry' key with anime details
            recommended_entries = response.json().get('data', [])
            # We want to return a list of anime objects, similar to what other search functions return
            return [rec.get('entry') for rec in recommended_entries if rec.get('entry')]
        else:
            print(f"Error fetching recommendations for anime ID {mal_id}: Status code {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recommendations for anime ID {mal_id}: {e}")
        return []

def get_genre_id_map() -> dict:
    """Fetches the mapping of anime genre names to their MAL IDs."""
    url = f"{JIKAN_API_BASE_URL}/genres/anime"
    genre_map = {}
    try:
        response = requests.get(url)
        time.sleep(0.5) # Respect basic rate limits
        if response.status_code == 200:
            genres_data = response.json().get('data', [])
            for genre_info in genres_data:
                if isinstance(genre_info, dict) and 'mal_id' in genre_info and 'name' in genre_info:
                    genre_map[genre_info['name'].lower()] = genre_info['mal_id']
            return genre_map
        else:
            print(f"Error fetching anime genres: Status code {response.status_code} - {response.text}")
            return genre_map # Return empty or partially filled map
    except requests.exceptions.RequestException as e:
        print(f"Error fetching anime genres: {e}")
        return genre_map # Return empty or partially filled map
