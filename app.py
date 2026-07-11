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

    us_action, _ = tmdb.discover_movies('en', 28, 1, 'popularity.desc', with_origin_country='US'); us_action = us_action[:20]
    us_comedy, _ = tmdb.discover_movies('en', 35, 1, 'popularity.desc', with_origin_country='US'); us_comedy = us_comedy[:20]

    arabic_movies, _ = tmdb.discover_movies('ar', None, 1, 'release_date.desc', with_original_language='ar'); arabic_movies = arabic_movies[:20]

    us_drama_shows, _ = tmdb.discover_shows('en', 18); us_drama_shows = us_drama_shows[:20]
    k_drama, _ = tmdb.get_popular_by_lang('ko', 'tv'); k_drama = k_drama[:20]
    c_drama, _ = tmdb.discover_shows('zh', None, 1); c_drama = c_drama[:20]
    jp_drama, _ = tmdb.discover_shows('ja', None, 1); jp_drama = jp_drama[:20]
    tr_drama, _ = tmdb.discover_shows('tr', None, 1); tr_drama = tr_drama[:20]
    ar_shows, _ = tmdb.discover_shows('ar', None, 1); ar_shows = ar_shows[:20]

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

    # حطيت if عشان ميوقعش لو فاضي
    if c_drama: content += s.get_cards(c_drama, "tv", "🇨🇳 مسلسلات صيني", scroll=True)
    if jp_drama: content += s.get_cards(jp_drama, "tv", "🇯🇵 مسلسلات ياباني", scroll=True)
    if tr_drama: content += s.get_cards(tr_drama, "tv", "🇹🇷 مسلسلات تركي", scroll=True)
    if ar_shows: content += s.get_cards(ar_shows, "tv", "🇪🇬 مسلسلات عربي", scroll=True)

    visitors = count_visitors()
    return s.base(content, "الرئيسية", visitors=visitors)

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
    visitors = count_visitors()
    return s.base(content, f'بحث: {q}', visitors=visitors)

@app.route("/genre/<int:genre_id>")
def genre_page(genre_id):
    page = request.args.get('page', 1, type=int)
    movies, total_pages = tmdb.discover_movies('en', genre_id, page)
    genre_names = {28:'اكشن', 35:'كوميدي', 18:'دراما', 27:'رعب', 878:'خيال علمي', 16:'انمي'}
    title = genre_names.get(genre_id, 'افلام')
    content = s.get_cards(movies, "movie", f"افلام {title}")
    content += s.get_pagination(page, total_pages, f"/genre/{genre_id}")
    visitors = count_visitors()
    return s.base(content, f"افلام {title}", visitors=visitors)

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
        visitors = count_visitors()
        return s.base(content, details.get('title'), visitors=visitors)
    except Exception as e:
        visitors = count_visitors()
        return s.base(f"<h2>خطأ: {e}</h2>", "خطأ", visitors=visitors)

@app.route("/watch/tv/<int:id>/<int:season>/<int:episode>")
def watch_tv(id, season, episode):
    try:
        details = tmdb.get_show_details(id)
        seasons = details.get('seasons', [])
        servers = s.get_servers(id, 'tv', season, episode)
        similar = tmdb.get_similar(id, 'tv')[:20]
        for item in similar: item['media_type'] = 'tv'

        content = s.get_hero(details)
        content += s.get_player(s.get_servers_html(servers, id, 'tv', season, episode))
        content += s.get_episodes(seasons, id, season, episode)
        content += s.get_cast(details.get('credits', {}).get('cast', []))
        content += s.get_cards(similar, 'tv', "مسلسلات مشابهه")

        visitors = count_visitors()
        return s.base(content, details.get('name'), visitors=visitors)

    except Exception as e:
        visitors = count_visitors()
        return s.base(f"<h2>خطأ: {e}</h2><p>{request.url}</p>", "خطأ", visitors=visitors)

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
        visitors = count_visitors()
        return s.base(content, title, visitors=visitors)
    except Exception as e:
        visitors = count_visitors()
        return s.base(f"Error: {e}", "خطأ", visitors=visitors)

@app.route("/discover/tv")
def discover_tv_page():
    try:
        genre = request.args.get('with_genres', '')
        language = request.args.get('with_original_language', '') # غيرت دي
        page = int(request.args.get('page', 1))

        if genre == '16':
            results, total_pages = tmdb.discover_shows(genre=16, language='ja', page=page)
            title = "⚽ انمي كورة"
            pagination_link = f"/discover/tv?with_genres=16"

        elif language == 'ko': # كوري
            results, total_pages = tmdb.discover_shows(language='ko', page=page)
            title = "🇰🇷 مسلسلات كوري"
            pagination_link = f"/discover/tv?with_original_language=ko"

        elif language == 'zh': # صيني جديد
            results, total_pages = tmdb.discover_shows(language='zh', page=page)
            title = "🇨🇳 مسلسلات صيني"
            pagination_link = f"/discover/tv?with_original_language=zh"

        elif language == 'ja': # ياباني جديد
            results, total_pages = tmdb.discover_shows(language='ja', page=page)
            title = "🇯🇵 مسلسلات ياباني"
            pagination_link = f"/discover/tv?with_original_language=ja"

        elif language == 'tr': # تركي جديد
            results, total_pages = tmdb.discover_shows(language='tr', page=page)
            title = "🇹🇷 مسلسلات تركي"
            pagination_link = f"/discover/tv?with_original_language=tr"

        elif language == 'ar': # عربي جديد
            results, total_pages = tmdb.discover_shows(language='ar', page=page)
            title = "🇪🇬 مسلسلات عربي"
            pagination_link = f"/discover/tv?with_original_language=ar"

        else: # الافتراضي
            results, total_pages = tmdb.discover_shows(language='en', page=page)
            title = "🇺🇸 مسلسلات اجنبي"
            pagination_link = f"/discover/tv"

        content = s.get_cards(results, "tv", title, scroll=False)
        content += s.get_pagination(page, total_pages, pagination_link)
        visitors = count_visitors()
        return s.base(content, title, visitors=visitors)

    except Exception as e:
        visitors = count_visitors()
        return s.base(f"<h1>Error</h1><p>{e}</p><p>URL: {request.url}</p>", "خطأ", visitors=visitors)

@app.route("/tv/genre/<int:genre_id>")
def tv_genre_page(genre_id):
    try:
        page = int(request.args.get('page', 1))
        results, total_pages = tmdb.discover_shows(genre=genre_id, page=page)
        content = s.get_cards(results, "tv", "🇺🇸 مسلسلات دراما امريكي", scroll=False)
        content += s.get_pagination(page, total_pages, f"/tv/genre/{genre_id}")
        visitors = count_visitors()
        return s.base(content, "مسلسلات دراما امريكي", visitors=visitors)
    except Exception as e:
        visitors = count_visitors()
        return s.base(f"Error: {e}", "خطأ", visitors=visitors)

if __name__ == '__main__':
    app.run(debug=True)
