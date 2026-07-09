import requests

API_KEY = "0e113d4271ad8489ce86ee83c8eb1908"
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/"

def _make_request(endpoint, params={}):
    params['api_key'] = API_KEY
    params['language'] = params.get('language', 'ar-EG') # خليتها ديناميك
    try:
        r = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error in _make_request: {e}")
        return {}

def get_trending(time_window='week', page=1):
    data = _make_request(f'trending/all/{time_window}', {'page': page})
    return data.get('results', []), data.get('total_pages', 1) 

def get_top_rated(page=1):
    data = _make_request('movie/top_rated', {'page': page})
    return data.get('results', []), data.get('total_pages', 1)

def get_movie_details(movie_id):
    return _make_request(f'movie/{movie_id}', {'append_to_response': 'credits,videos'})

def get_show_details(show_id):
    return _make_request(f'tv/{show_id}', {'append_to_response': 'credits,videos'})

def get_episodes(show_id, season):
    data = _make_request(f'tv/{show_id}/season/{season}')
    return data.get('episodes', [])

def get_season_details(show_id, season_number):
    return _make_request(f'tv/{show_id}/season/{season_number}')

def search(query, page=1):
    params = {'query': query, 'page': page, 'language':'ar-EG'}
    data = _make_request('search/multi', params)
    return data.get('results', []), data.get('total_pages', 1)

def discover_movies(language='en', genre=None, page=1, sort_by='popularity.desc', with_original_language=None, with_origin_country=None):
    params = {'sort_by': sort_by, 'page': page, 'vote_count.gte': 100} # زودت التصويت عشان النتايج تبقى نضيفة
    if language: params['with_original_language'] = language
    if genre: params['with_genres'] = genre
    if with_original_language: params['with_original_language'] = with_original_language # للعربي
    if with_origin_country: params['with_origin_country'] = with_origin_country # للامريكي
    
    data = _make_request('discover/movie', params)
    return data.get('results', []), data.get('total_pages', 1)

def discover_shows(language='en', genre=None, page=1, with_origin_country=None):
    params = {'sort_by': 'popularity.desc', 'page': page, 'vote_count.gte': 20}
    if language: params['with_original_language'] = language
    if genre: params['with_genres'] = genre
    if with_origin_country: params['with_origin_country'] = with_origin_country # ضيف دي
    data = _make_request('discover/tv', params)
    return data.get('results', []), data.get('total_pages', 1)

def get_airing_today():
    data = _make_request('tv/airing_today', {'language':'ar-EG'})
    return data.get('results', [])

def get_popular_by_lang(lang, media_type):
    data = _make_request(f'discover/{media_type}', {'with_original_language': lang, 'sort_by': 'popularity.desc', 'page': 1})
    return data.get('results', []), data.get('total_pages', 1)

def get_similar(id, media_type):
    data = _make_request(f'{media_type}/{id}/similar', {'page': 1})
    return data.get("results", [])

def get_upcoming(page=1):
    data = _make_request('movie/upcoming', {'page': page, 'region': 'EG'}) # ضفت المنطقة
    return data.get('results', []), data.get('total_pages', 1)

def get_details(id, media_type):
    return _make_request(f'{media_type}/{id}', {'append_to_response': 'credits'})
