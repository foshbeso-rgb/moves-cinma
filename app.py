from flask import send_from_directory
import traceback
import os
from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory
from markupsafe import Markup
import tmdb
import sections as s
import requests
import config

template_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(template_dir, 'templates'), static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dakhlin_secret_key_123')

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = os.environ.get('TMDB_API_KEY')

def count_visitors():
    file_path = os.path.join(template_dir, 'visitors.txt')
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f: f.write('0')
        with open(file_path, 'r') as f: count = int(f.read())
    except:
        count = 0
    count += 1
    try:
        with open(file_path, 'w') as f: f.write(str(count))
    except:
        pass
    return count

@app.route('/googleccfb7f75048a906c.html')
def google_verify():
    return send_from_directory('static', 'googleccfb7f75048a906c.html')

@app.route("/")
def index():
    trending, _ = tmdb.get_trending()
    trending = trending[:15]

    top_rated_movies, _ = tmdb.discover_movies('en', None, 1, 'vote_average.desc')
    top_rated_movies = top_rated_movies[:20]

    upcoming, _ = tmdb.get_upcoming()
    upcoming = upcoming[:20]

    anime, _ = tmdb.discover_shows('ja', 16)
    anime = anime[:15]
    soccer_anime = [x for x in anime if 'كورة' in x.get('name','') or 'football' in x.get('name','').lower() or 'captain' in x.get('name','').lower()][:20]
    if not soccer_anime:
        soccer_anime = [x for x in anime if 16 in x.get('genre_ids', [])][:20]

    # التعديل هنا 👇 ضفنا with_origin_country و with_original_language
    us_action, _ = tmdb.discover_movies('en', 28, 1, 'popularity.desc', with_origin_country='US'); us_action = us_action[:20]
    us_comedy, _ = tmdb.discover_movies('en', 35, 1, 'popularity.desc', with_origin_country='US'); us_comedy = us_comedy[:20]
    arabic_movies, _ = tmdb.discover_movies('ar', None, 1, 'popularity.desc', with_original_language='ar'); arabic_movies = arabic_movies[:20]

    us_drama_shows, _ = tmdb.discover_shows('en', 18); us_drama_shows = us_drama_shows[:20]
    k_drama, _ = tmdb.get_popular_by_lang('ko', 'tv'); k_drama = k_drama[:20]

    hero = s.get_hero(trending[0] if trending else None)
    content = hero

    content += s.get_cards(trending, "all", "🔥 الاكثر رواجاً", scroll=True)
    content += s.get_cards(top_rated_movies, "movie", "⭐ الاعلى تقييماً", scroll=True)
    content += s.get_cards(upcoming, "movie", "🎬 قريبا في السينما", scroll=True)
    content += s.get_cards(soccer_anime, "tv", "⚽ انمي كورة", scroll=True)
    content += s.get_cards(us_action, "movie", "🇺🇸 افلام اكشن امريكي", scroll=True)
    content += s.get_cards(us_comedy, "movie", "🇺🇸 افلام كوميدي امريكي", scroll=True)
    content += s.get_cards(arabic_movies, "movie", "🇪🇬 افلام عربي", scroll=True)
    content += s.get_cards(us_drama_shows, "tv", "🇺🇸 مسلسلات دراما امريكي", scroll=True)
    content += s.get_cards(k_drama, "tv", "🇰🇷 مسلسلات كوري", scroll=True)

    visitors = count_visitors()
    return s.base(content, "الرئيسية", visitors=visitors)

@app.route('/about')
def about():
    content = Markup(f"""... كودك زي ما هو... """)
    visitors = count_visitors()
    return s.base(content, "من نحن", visitors=visitors)

@app.route('/contact')
def contact():
    content = Markup(f"""... كودك زي ما هو... """)
    visitors = count_visitors()
    return s.base(content, "اتصل بنا", visitors=visitors)

@app.route('/privacy')
def privacy():
    content = Markup(f"""... كودك زي ما هو... """)
    visitors = count_visitors()
    return s.base(content, "سياسة الخصوصية", visitors=visitors)

@app.route('/trending')
def trending_page():
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.get_trending(page=page)
    content = s.get_cards(results, 'all', '🔥 الاكثر رواجاً', scroll=False)
    pagination = s.get_pagination(page, total_pages, '/trending')
    visitors = count_visitors()
    return s.base(content + pagination, "الاكثر رواجاً", visitors=visitors)

@app.route('/top-rated')
def top_rated_page():
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.discover_movies('en', None, page, 'vote_average.desc')
    content = s.get_cards(results, 'movie', '⭐ الأعلى تقييماً', scroll=False)
    pagination = s.get_pagination(page, total_pages, '/top-rated')
    visitors = count_visitors()
    return s.base(content + pagination, 'الأعلى تقييماً', visitors=visitors)

@app.route('/upcoming')
def upcoming_page():
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.get_upcoming(page=page)
    content = s.get_cards(results, 'movie', '🎬 قريباً في السينما', scroll=False)
    pagination = s.get_pagination(page, total_pages, '/upcoming')
    visitors = count_visitors()
    return s.base(content + pagination, 'قريباً في السينما', visitors=visitors)

@app.route("/search")
def search():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.search(q, page)
    content = s.get_cards(results, "all", f'نتائج البحث عن: {q}')
    content += s.get_pagination(page, total_pages, f"/search?q={q}")
    visitors = count_visitors() # ضفتها
    return s.base(content, f'بحث: {q}', visitors=visitors)

@app.route("/genre/<int:genre_id>")
def genre_page(genre_id):
    page = request.args.get('page', 1, type=int)
    movies, total_pages = tmdb.discover_movies('en', genre_id, page)
    genre_names = {28:'اكشن', 35:'كوميدي', 18:'دراما', 27:'رعب', 878:'خيال علمي', 16:'انمي'}
    title = genre_names.get(genre_id, 'افلام')
    content = s.get_cards(movies, "movie", f"افلام {title}")
    content += s.get_pagination(page, total_pages, f"/genre/{genre_id}")

    arabic_movies, _ = tmdb.discover_movies('ar', None, 1, 'popularity.desc', with_original_language='ar') # عدلتها
    content += s.get_cards(arabic_movies, "movie", "🇪🇬 افلام عربي", scroll=True)

    korean_movies, _ = tmdb.discover_movies('ko', None, 1, 'popularity.desc', with_origin_country='KR') # عدلتها
    content += s.get_cards(korean_movies, "movie", "🇰🇷 افلام كوري", scroll=True)

    japan_movies, _ = tmdb.discover_movies('ja', None, 1, 'popularity.desc', with_origin_country='JP') # عدلتها
    content += s.get_cards(japan_movies, "movie", "🇯🇵 افلام ياباني", scroll=True)

    india_movies, _ = tmdb.discover_movies('hi', None, 1, 'popularity.desc', with_origin_country='IN') # عدلتها
    content += s.get_cards(india_movies, "movie", "🇮🇳 افلام هندي", scroll=True)

    visitors = count_visitors() # ضفتها
    return s.base(content, f"افلام {title}", visitors=visitors)

# باقي الروتات بتاعتك... اهم حاجة زود visitors=visitors في كل return s.base
# مثال:
@app.route("/favorites")
def favorites_page():
    content = s.get_favorites()
    visitors = count_visitors()
    return s.base(content, "المفضلة", visitors=visitors)

@app.route("/watch/movie/<int:id>")
def watch_movie(id):
    try:
        details = tmdb.get_movie_details(id)
        servers = s.get_servers(id, 'movie')
        similar = tmdb.get_similar(id, 'movie')[:20]
        for item in similar: item['media_type'] = 'movie'
        content = s.get_hero(details)
        content += s.get_player(s.get_servers_html(servers, id, 'movie'))
        content += s.get_cast(details.get('credits', {}).get('cast', []))
        content += s.get_cards(similar, 'movie', "افلام مشابهه")
        visitors = count_visitors() # ضفتها
        return s.base(content, details.get('title'), visitors=visitors)
    except Exception as e:
        visitors = count_visitors()
        return s.base(f"<h2>خطأ: {e}</h2>", "خطأ", visitors=visitors)
        
# 3. ده عشان زرار التشغيل في الهيرو
@app.route("/watch/<string:media_type>/<int:id>")
def watch_redirect(media_type, id):
    if media_type == 'tv':
        return redirect(f"/watch/tv/{id}/1/1")
    else:
        return redirect(f"/watch/movie/{id}")

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_files():
    return send_from_directory(os.getcwd(), request.path[1:])

@app.route("/discover/movie")
def discover_movies_page():
    try:
        lang = request.args.get('with_original_language', 'ar')
        page = int(request.args.get('page', 1))
        results, total_pages = tmdb.discover_movies(with_original_language=lang, page=page)
        
        title = "🇪🇬 افلام عربي" if lang == 'ar' else "افلام"
        content = s.get_cards(results, "movie", title, scroll=False)
        content += s.get_pagination(page, total_pages, f"/discover/movie?with_original_language={lang}")
        return s.base(content, title, visitors=s.count_visitors())
    except Exception as e:
        return f"Error: {e}"


@app.route("/discover/tv")
def discover_tv_page():
    try:
        genre = request.args.get('with_genres', '')
        country = request.args.get('with_origin_country', '')
        page = int(request.args.get('page', 1))
        
        if genre == '16': # انمي كورة
            results, total_pages = tmdb.discover_shows(genre=16, page=page)
            title = "⚽ انمي كورة"
            
        elif country == 'KR': # كوري - هنا التعديل
            results, total_pages = tmdb.discover_shows(page=page)
            # فلتر المسلسلات اللي فيها كوريا في origin_country
            results = [r for r in results if 'KR' in r.get('origin_country', [])]
            title = "🇰🇷 مسلسلات كوري"
            
        else:
            results, total_pages = tmdb.discover_shows(page=page)
            title = "مسلسلات"
        
        content = s.get_cards(results, "tv", title, scroll=False)
        content += s.get_pagination(page, 10, f"/discover/tv?with_origin_country={country}&with_genres={genre}") # خليت total_pages = 10 عشان الفلتر
        return s.base(content, title, visitors=s.count_visitors())
    except Exception as e:
        return f"Error: {e}"


@app.route("/tv/genre/<int:genre_id>")
def tv_genre_page(genre_id):
    try:
        page = int(request.args.get('page', 1))
        results, total_pages = tmdb.discover_shows(genre=genre_id, page=page)
        content = s.get_cards(results, "tv", "🇺🇸 مسلسلات دراما امريكي", scroll=False)
        content += s.get_pagination(page, total_pages, f"/tv/genre/{genre_id}")
        return s.base(content, "مسلسلات دراما امريكي", visitors=s.count_visitors())
    except Exception as e:
        return f"Error: {e}"


@app.route("/genre/<int:genre_id>")
def movie_genre_page(genre_id):
    try:
        page = int(request.args.get('page', 1))
        results, total_pages = tmdb.discover_movies(genre=genre_id, page=page)
        content = s.get_cards(results, "movie", "افلام", scroll=False)
        content += s.get_pagination(page, total_pages, f"/genre/{genre_id}")
        return s.base(content, "افلام", visitors=s.count_visitors())
    except Exception as e:
        return f"Error: {e}"


