from flask import send_from_directory
import traceback
import os
from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory
from markupsafe import Markup
import tmdb
import sections as s
import requests
import config

template_dir = os.path.dirname(os.path.abspath(__file__)) # 1. لازم يبقى فوق
app = Flask(__name__, template_folder=os.path.join(template_dir, 'templates'), static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dakhlin_secret_key_123')

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = os.environ.get('TMDB_API_KEY')

# 2. دالة العداد
def count_visitors():
    file_path = os.path.join(template_dir, 'visitors.txt')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f: f.write('0')
    with open(file_path, 'r') as f: count = int(f.read())
    count += 1
    with open(file_path, 'w') as f: f.write(str(count))
    return count

@app.route('/googleccfb7f75048a906c.html')
def google_verify():
    return send_from_directory('static', 'googleccfb7f75048a906c.html')

@app.route("/")
def index():
    print("API_KEY:", API_KEY)
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

    us_action, _ = tmdb.discover_movies('en', 28); us_action = us_action[:20]
    us_comedy, _ = tmdb.discover_movies('en', 35); us_comedy = us_comedy[:20]
    arabic_movies, _ = tmdb.discover_movies('ar'); arabic_movies = arabic_movies[:20]
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

    visitors = count_visitors() # 3. نعد الزوار

    return s.base(content, "الرئيسية", visitors=visitors) # 4. نبعت العدد

# امسح فانكشن home_page كلها عشان عاملة تعارض

    upcoming, _ = tmdb.get_upcoming()
    upcoming = upcoming[:20]

    anime, _ = tmdb.discover_shows('ja', 16)
    anime = anime[:15]
    soccer_anime = [x for x in anime if 'كورة' in x.get('name','') or 'football' in x.get('name','').lower() or 'captain' in x.get('name','').lower()][:20]
    if not soccer_anime:
        soccer_anime = [x for x in anime if 16 in x.get('genre_ids', [])][:20]

    us_action, _ = tmdb.discover_movies('en', 28); us_action = us_action[:20]
    us_comedy, _ = tmdb.discover_movies('en', 35); us_comedy = us_comedy[:20]
    arabic_movies, _ = tmdb.discover_movies('ar'); arabic_movies = arabic_movies[:20]
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

    return s.base(content, "الرئيسية")

@app.route('/about')
def about():
    content = Markup(f"""
    <div style="min-height:80vh; padding:80px 20px; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1478720568477-152d9b164e26?q=80&w=2070') center/cover no-repeat fixed; color:#ddd;">
        <div style="max-width:900px; margin:auto; text-align:right; line-height:1.9; background:rgba(10,10,10,0.92); backdrop-filter: blur(3px); padding:40px; border-radius:12px; font-weight:500;">
            <h1 style="color:#e50914; margin-bottom:30px; font-size:32px; text-align:center;">من نحن</h1>
            <p>
                {config.SITE_NAME} هو موقع عربي متخصص في عرض الافلام والمسلسلات اونلاين بجودة عالية.
                هدفنا توفير افضل تجربة مشاهدة للجميع مجاناً.
                نحن لا نستضيف اي ملفات على سيرفراتنا وجميع الروابط من مصادر خارجية.
            </p>
        </div>
    </div>
    """)
    return s.base(content, "من نحن")

@app.route('/contact')
def contact():
    content = Markup(f"""
    <div style="min-height:80vh; padding:80px 20px; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1478720568477-152d9b164e26?q=80&w=2070') center/cover no-repeat fixed; color:#ddd;">
        <div style="max-width:700px; margin:auto; text-align:right; line-height:1.9; background:rgba(10,10,10,0.92); backdrop-filter: blur(3px); padding:40px; border-radius:12px; font-weight:500;">
            <h1 style="color:#e50914; margin-bottom:30px; font-size:32px; text-align:center;">اتصل بنا</h1>
            <p style="font-size:18px; margin-bottom:20px;">لو عندك اقتراح او فيلم/مسلسل ناقص او واجهتك اي مشكلة في الموقع تقدر تتواصل معانا</p>
            <h2 style="color:#e50914; margin-top:30px; font-size:22px;">الايميل</h2>
            <p>foshbeso@gmail.com</p>
            <h2 style="color:#e50914; margin-top:20px; font-size:22px;">صفحاتنا</h2>
            <p>تابعنا على فيسبوك وتليجرام عشان يوصلك كل جديد</p>
        </div>
    </div>
    """)
    return s.base(content, "اتصل بنا")

@app.route('/privacy')
def privacy():
    content = Markup(f"""
    <div style="min-height:80vh; padding:80px 20px; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1478720568477-152d9b164e26?q=80&w=2070') center/cover no-repeat fixed; color:#ddd;">
        <div style="max-width:900px; margin:auto; text-align:right; line-height:1.9; background:rgba(10,10,10,0.92); backdrop-filter: blur(3px); padding:40px; border-radius:12px; font-weight:500;">
            <h1 style="color:#e50914; margin-bottom:30px; font-size:32px; text-align:center;">سياسة الخصوصية</h1>
            <p>نحن في <b style="color:#fff;">داخلين سينما</b> نحترم خصوصيتك.</p>
            <h2 style="color:#e50914; margin-top:30px; font-size:22px;">ملفات الكوكيز</h2>
            <p>نستخدم الكوكيز لتحسين تجربتك في الموقع. يمكنك تعطيلها من المتصفح.</p>
            <h2 style="color:#e50914; margin-top:20px; font-size:22px;">اعلانات جوجل</h2>
            <p>يستخدم موقعنا اعلانات جوجل ادسنس. جوجل قد تستخدم ملفات تعريف الارتباط لعرض اعلانات مناسبة لك.</p>
            <h2 style="color:#e50914; margin-top:20px; font-size:22px;">الروابط الخارجية</h2>
            <p>نحن غير مسؤولين عن محتوى المواقع الخارجية التي يتم التحويل اليها.</p>

            <h2 style="color:#e50914; margin-top:20px; font-size:22px;">للتواصل</h2>
            <p>لو عندك اي استفسار بخصوص سياسة الخصوصية تقدر تتواصل معانا على:
            <a href="mailto:foshbeso@gmail.com" style="color:#e50914; text-decoration:none;">foshbeso@gmail.com</a></p>
        </div>
    </div>
    """)

    return s.base(content, "سياسة الخصوصية")

@app.route('/trending')
def trending_page():
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.get_trending(page=page)
    content = s.get_cards(results, 'all', '🔥 الاكثر رواجاً', scroll=False)
    pagination = s.get_pagination(page, total_pages, '/trending')
    return s.base(content + pagination, "الاكثر رواجاً")


@app.route('/')
def home_page():
    featured_ids = [
        533535,  # Deadpool & Wolverine
        1022796, # Inside Out 2  
        519182,  # Despicable Me 4
        573435,  # Bad Boys: Ride or Die
        614479,  # Kingdom of the Planet of the Apes
        945961,  # A Quiet Place: Day One
        1023545, # Twisters
    ]
    
    results = []
    for movie_id in featured_ids:
        try: # لفيناه عشان لو فيلم وقع ميوقعش الموقع كله
            movie = tmdb.get_movie_details(movie_id)
            if movie and movie.get('title') and movie.get('poster_path'): # زودنا تشيك البوستر
                results.append(movie)
        except:
            print(f"Error in movie id: {movie_id}") # هيطبع في logs
    
    if not results:
        content = "<h2 style='text-align:center; padding:50px;'>في مشكلة في تحميل الافلام حاول تاني</h2>"
    else:
        content = s.get_cards(results, 'movie', '🔥 افلام اليوم', scroll=True)
    
    trending_link = '<div style="text-align:center; margin:20px;"><a href="/trending" class="btn">عرض المزيد 🔥</a></div>'
    
    return s.base(content + trending_link, "داخلين سينما")


@app.route('/top-rated')
def top_rated_page():
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.get_top_rated(page=page)
    content = s.get_cards(results, 'all', '⭐ الأعلى تقييماً', scroll=False)
    pagination = s.get_pagination(page, total_pages, '/top-rated')
    return s.base(content + pagination, 'الأعلى تقييماً')

@app.route('/upcoming')
def upcoming_page():
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.get_upcoming(page=page)
    content = s.get_cards(results, 'movie', '🎬 قريباً في السينما', scroll=False)
    pagination = s.get_pagination(page, total_pages, '/upcoming')
    return s.base(content + pagination, 'قريباً في السينما')

@app.route("/search")
def search():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    results, total_pages = tmdb.search(q, page)
    content = s.get_cards(results, "all", f'نتائج البحث عن: {q}')
    content += s.get_pagination(page, total_pages, f"/search?q={q}")
    return s.base(content, f'بحث: {q}')

@app.route("/genre/<int:genre_id>")
def genre_page(genre_id):
    page = request.args.get('page', 1, type=int)
    movies, total_pages = tmdb.discover_movies('en', genre_id, page)
    genre_names = {28:'اكشن', 35:'كوميدي', 18:'دراما', 27:'رعب', 878:'خيال علمي', 16:'انمي'}
    title = genre_names.get(genre_id, 'افلام')
    content = s.get_cards(movies, "movie", f"افلام {title}")
    content += s.get_pagination(page, total_pages, f"/genre/{genre_id}")
     # افلام عربي
    arabic_movies = tmdb.discover_movies(with_original_language='ar', sort_by='popularity.desc')
    content += s.get_cards(arabic_movies, "movie", "🇪🇬 افلام عربي", scroll=True)

    # افلام كوري
    korean_movies = tmdb.discover_movies(with_origin_country='KR', sort_by='popularity.desc')
    content += s.get_cards(korean_movies, "movie", "🇰🇷 افلام كوري", scroll=True)

# افلام ياباني
    japan_movies = tmdb.discover_movies(with_origin_country='JP', sort_by='popularity.desc')
    content += s.get_cards(japan_movies, "movie", "🇯🇵 افلام ياباني", scroll=True)

# افلام هندي
    india_movies = tmdb.discover_movies(with_origin_country='IN', sort_by='popularity.desc')
    content += s.get_cards(india_movies, "movie", "🇮🇳 افلام هندي", scroll=True)
    
    return s.base(content, f"افلام {title}")
    

@app.route('/discover/<media_type>')
def discover(media_type):
    country = request.args.get('with_origin_country', '')
    genre = request.args.get('with_genres', '')
    page = int(request.args.get('page', 1))

    country_names = {'KR': 'كوري', 'CN': 'صيني', 'JP': 'ياباني'}
    genre_names = {'16': 'انمي', '': 'دراما'}

    params = {'page': page, 'sort_by': 'popularity.desc', 'language': 'ar-EG'}
    if country: params['with_origin_country'] = country
    if genre: params['with_genres'] = genre

    if media_type == 'tv':
        data = tmdb._make_request('discover/tv', params)
        title = f"{genre_names.get(genre, 'مسلسلات')} {country_names.get(country, '')}"
    else:
        data = tmdb._make_request('discover/movie', params)
        title = f"افلام {country_names.get(country, '')}"

    items = data.get('results', [])
    total_pages = data.get('total_pages', 1)

    content = s.get_cards(items, media_type, title)
    pagination = s.get_pagination(page, total_pages, f"/discover/{media_type}?with_origin_country={country}&with_genres={genre}")
    return s.base(content + pagination, title)

@app.route('/tv/genre/<int:genre_id>')
def tv_by_genre(genre_id):
    page = int(request.args.get('page', 1))
    genre_names = {18: 'دراما', 35: 'كوميدي', 10759: 'اكشن ومغامرة', 10765: 'خيال و فانتازيا', 80: 'جريمة', 16: 'كرتون'}
    data = tmdb._make_request('discover/tv', {'page': page, 'with_genres': genre_id, 'sort_by': 'popularity.desc', 'language': 'ar-EG'})
    items = data.get('results', [])
    total_pages = data.get('total_pages', 1)
    title = f"مسلسلات {genre_names.get(genre_id, '')}"
    content = s.get_cards(items, 'tv', title)
    pagination = s.get_pagination(page, total_pages, f"/tv/genre/{genre_id}")
    return s.base(content + pagination, title)

@app.route('/tv/country/<country_code>')
def tv_by_country(country_code):
    page = int(request.args.get('page', 1))
    country_names = {'EG': 'مصري', 'SA': 'خليجي', 'SY': 'سوري'}
    data = tmdb._make_request('discover/tv', {'page': page, 'with_original_language': 'ar', 'sort_by': 'popularity.desc', 'language': 'ar-EG'})
    items = data.get('results', [])
    if country_code == 'EG':
        items = [x for x in items if any(word in (x.get('name','') + x.get('overview','')) for word in ['مصر', 'القاهرة', 'رمضان'])]
    total_pages = data.get('total_pages', 1)
    title = f"مسلسلات {country_names.get(country_code, '')}"
    content = s.get_cards(items, 'tv', title)
    pagination = s.get_pagination(page, total_pages, f"/tv/country/{country_code}")
    return s.base(content + pagination, title)

def get_ramadan_shows(year=2027):
    from datetime import datetime
    import requests
    if year == 2027:
        start_date = "2027-03-10"
        end_date = "2027-04-10"
    else:
        start_date = f"{year}-03-01"
        end_date = f"{year}-04-30"

    url = f"https://api.themoviedb.org/3/discover/tv"
    params = {"api_key": API_KEY, "language": "ar-EG", "sort_by": "popularity.desc", "first_air_date.gte": start_date, "first_air_date.lte": end_date, "with_origin_country": "EG", "page": 1}
    try:
        res = requests.get(url, params=params)
        data = res.json()
        return data.get("results", [])
    except:
        return []

@app.route("/add_favorite/<media_type>/<int:id>")
def add_favorite(media_type, id):
    favorites = session.get('favorites', [])
    item = {'id': id, 'type': media_type}
    if item in favorites:
        favorites.remove(item)
        session['favorites'] = favorites
        return jsonify({'status': 'removed'})
    else:
        favorites.append(item)
        session['favorites'] = favorites
        return jsonify({'status': 'added'})

@app.route("/remove_favorite/<media_type>/<int:id>")
def remove_favorite(media_type, id):
    favorites = session.get('favorites', [])
    favorites = [f for f in favorites if not (f['id'] == id and f['type'] == media_type)]
    session['favorites'] = favorites
    return jsonify({'status': 'removed'})

@app.route("/api/favorites")
def api_favorites():
    favorites = session.get('favorites', [])
    movies = []
    for fav in favorites:
        details = tmdb.get_details(fav['id'], fav['type'])
        if details:
            details['media_type'] = fav['type']
            movies.append(details)
    return jsonify(movies)

@app.route("/favorites")
def favorites_page():
    content = s.get_favorites()
    return s.base(content, "المفضلة")

# روت الافلام
@app.route("/watch/movie/<int:id>")
def watch_movie(id):
    try:
        details = tmdb.get_movie_details(id)
        servers = s.get_servers(id, 'movie')
        similar = tmdb.get_similar(id, 'movie')[:20]
        for item in similar: item['media_type'] = 'movie'

        content = s.get_hero(details)
        content += s.get_player(s.get_servers_html(servers, id, 'movie')) # <-- عدلت هنا
        content += s.get_cast(details.get('credits', {}).get('cast', []))
        content += s.get_cards(similar, 'movie', "افلام مشابهه")
        return s.base(content, details.get('title'))
    except Exception as e:
        return s.base(f"<h2>خطأ: {e}</h2>", "خطأ")


# روت المسلسلات
@app.route("/watch/tv/<int:show_id>/<int:season>/<int:episode>")
def watch_tv(show_id, season, episode):
    try:
        details = tmdb.get_show_details(show_id)
        servers = s.get_servers(show_id, 'tv', season, episode)
        seasons = details.get('seasons', [])
        similar = tmdb.get_similar(show_id, 'tv')[:20]
        for item in similar: item['media_type'] = 'tv'

        content = s.get_hero(details)
        content += s.get_episodes(seasons, show_id, season, episode)
        content += s.get_player(s.get_servers_html(servers, show_id, 'tv', season, episode)) # <-- عدلت هنا
        content += s.get_cast(details.get('credits', {}).get('cast', []))
        content += s.get_cards(similar, 'tv', "مسلسلات مشابهه")
        return s.base(content, details.get('name'))
    except Exception as e:
        return s.base(f"<h2>خطأ: {e}</h2>", "خطأ")
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


